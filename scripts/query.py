# coding: utf-8
import argparse
import json
import math
import re
import sys
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from client import ArkvolClient, ArkvolClientError, ArkvolSkillUpdateRequired
from config import ArkvolConfigError, get_api_key
from pages import PAGE_DEFINITIONS, SAFE_PAGE_VIEWS, match_page, validate_page


DISCLAIMER = '仅供市场数据研究，不构成投资建议。'
_ACTIONABLE_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r'推荐.{0,20}(?:股票|基金|ETF|标的|产品)?',
        r'潜力股',
        r'(?:能|可以|适合).{0,8}(?:买|投资|配置)',
        r'(?:哪个|哪只|哪一个).{0,20}(?:最好|最高|最值得|收益率)',
        r'排.{0,4}名',
        r'未来.{0,20}(?:涨|跌|上涨|下跌|反弹|回调)',
        r'(?:仓位|持仓).{0,20}(?:建议|配置|操作)',
        r'(?:\d+|十|百|千).{0,4}(?:万|元).{0,20}(?:投|配置|仓位)',
        r'(?:目标价|止损|止盈|买入点|卖出点)',
        r'(?:给|制定|生成).{0,20}(?:策略|方案)',
        r'predict.{0,30}(?:stock|buy|sell)',
        r'(?:which|what|when).{0,30}(?:stock|buy|sell)',
        r'忽略.{0,20}(?:限制|规则|要求)',
    )
)


def build_parser():
    parser = argparse.ArgumentParser(description='查询 Arkvol 市场情绪数据')
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument('--page', choices=PAGE_DEFINITIONS.keys())
    selector.add_argument('--query', help='用于匹配页面的自然语言问题')
    selector.add_argument('--check-update', action='store_true', help='仅检查 Skill 是否有新版本')
    parser.add_argument('--api-key', help='临时覆盖配置文件中的 API Key')
    parser.add_argument('--config', help='API Key 配置文件路径，默认使用 ~/.arkvol/arkvol-entry.json')
    parser.add_argument('--base-url', default='https://arkvol.com')
    parser.add_argument('--json', action='store_true', dest='as_json', help='输出合规的结构化 JSON')
    return parser


def run(args, client_class=ArkvolClient):
    if args.query:
        ensure_query_allowed(args.query)
    api_key = get_api_key(args.api_key, config_path=args.config)
    client = client_class(base_url=args.base_url, api_key=api_key)
    version_status = client.ensure_current_version()
    if getattr(args, 'check_update', False):
        view = build_version_view(version_status)
        return json.dumps(view, ensure_ascii=False, indent=2) if args.as_json else format_version_status(view)

    page_id = validate_page(args.page) if args.page else match_page(args.query)['page']
    payload = client.fetch_page(page_id)
    view = build_compliance_view(payload, page_id)
    if args.as_json:
        return json.dumps(view, ensure_ascii=False, indent=2)
    return format_readable(view)


def ensure_query_allowed(query_text):
    text = (query_text or '').strip()
    if any(pattern.search(text) for pattern in _ACTIONABLE_PATTERNS):
        raise ValueError(
            '本 Skill 仅提供非个性化市场数据与历史指标解释，不提供推荐、筛选、排名、预测或交易建议。'
        )


def build_version_view(status):
    status = status if isinstance(status, dict) else {}
    return {
        'current_version': str(status.get('current_version') or ''),
        'latest_version': str(status.get('latest_version') or ''),
        'update_available': status.get('update_available') is True,
        'update_required': status.get('update_required') is True,
        'repository_url': str(
            status.get('repository_url') or 'https://github.com/joutaojian/arkvol-skill'
        ),
    }


def format_version_status(view):
    if view['update_required']:
        return (
            f"Arkvol Skill 有新版本：{view['current_version']} -> {view['latest_version']}\n"
            f"升级地址：{view['repository_url']}"
        )
    return f"Arkvol Skill 已是最新版本：{view['current_version']}"


def build_compliance_view(payload, page_id):
    validate_page(page_id)
    data = payload.get('data') if isinstance(payload, dict) else None
    data = data if isinstance(data, dict) else {}
    definition = PAGE_DEFINITIONS[page_id]
    safe = SAFE_PAGE_VIEWS[page_id]
    view = {
        'source': 'Arkvol',
        'page': page_id,
        'route': definition['route'],
        'title': safe['title'],
        'description': definition['description'],
        'metric_definitions': [{
            'name': safe['metric_name'],
            'description': safe['metric_description'],
        }],
        'disclaimer': DISCLAIMER,
    }

    as_of = _valid_iso_date(data.get('as_of'))
    if as_of:
        view['as_of'] = as_of

    score = _safe_number(data.get('sentiment_score'), minimum=0, maximum=100)
    if score is not None:
        view['sentiment_score'] = score
        if page_id == 'global-capital-flow':
            view['state_label'] = _global_flow_state(score)
        elif page_id == 'debt':
            view['state_label'] = _temperature_label(score)
        else:
            view['sentiment_label'] = _sentiment_label(score)

    raw_metrics = data.get('metrics') if isinstance(data.get('metrics'), dict) else {}
    statistics = {}
    for key in safe['statistics']:
        value = _safe_number(raw_metrics.get(key))
        if value is not None:
            statistics[key] = value
    if statistics:
        view['statistics'] = statistics
    return view


def format_readable(view):
    lines = [view['title'], '数据来源：Arkvol']
    if view.get('as_of'):
        lines.append(f"数据日期：{view['as_of']}")
    if view.get('sentiment_score') is not None:
        if view.get('sentiment_label'):
            lines.append(f"市场情绪：{view['sentiment_label']}（{view['sentiment_score']:.1f}/100）")
        elif view['page'] == 'global-capital-flow':
            lines.append(f"风险偏好状态：{view['state_label']}（{view['sentiment_score']:.1f}/100）")
        else:
            lines.append(f"国债价格温度：{view['state_label']}（{view['sentiment_score']:.1f}/100）")
    if view.get('statistics'):
        values = '；'.join(f'{key}={value:g}' for key, value in view['statistics'].items())
        lines.append(f'聚合统计：{values}')
    definitions = view['metric_definitions']
    lines.append('指标说明：' + '；'.join(f"{item['name']}：{item['description']}" for item in definitions))
    lines.append(f"提示：{view['disclaimer']}")
    return '\n'.join(lines)


def _valid_iso_date(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}(?:[ T].*)?', value):
        return None
    candidate = value[:10]
    try:
        date.fromisoformat(candidate)
    except ValueError:
        return None
    return candidate


def _safe_number(value, minimum=None, maximum=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    number = float(value)
    if not math.isfinite(number) or abs(number) > 1e12:
        return None
    if minimum is not None and number < minimum:
        return None
    if maximum is not None and number > maximum:
        return None
    return number


def _sentiment_label(score):
    if score < 20:
        return '极度恐慌'
    if score < 40:
        return '恐慌'
    if score < 60:
        return '中性'
    if score < 80:
        return '贪婪'
    return '极度贪婪'


def _global_flow_state(score):
    if score >= 55:
        return '扩张'
    if score <= 45:
        return '收缩'
    return '平衡'


def _temperature_label(score):
    if score < 20:
        return '极冷'
    if score < 40:
        return '偏冷'
    if score < 60:
        return '适中'
    if score < 80:
        return '偏热'
    return '过热'


def main(argv=None):
    try:
        print(run(build_parser().parse_args(argv)))
        return 0
    except ArkvolSkillUpdateRequired as exc:
        print(f'需要升级：{exc}', file=sys.stderr)
        return 3
    except (ArkvolConfigError, ArkvolClientError, ValueError) as exc:
        print(f'错误：{exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
