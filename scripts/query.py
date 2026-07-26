# coding: utf-8
import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from client import ArkvolClient, ArkvolClientError, ArkvolSkillUpdateRequired
from config import ArkvolConfigError, get_api_key
from pages import PAGE_DEFINITIONS, match_page, validate_page


_STOCK_RECOMMENDATION_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r'(?:荐股|股票推荐|个股推荐|基金推荐|ETF推荐|标的推荐)',
        r'推荐.{0,16}(?:股票|个股|基金|ETF|标的|证券|产品)',
        r'(?:股票|个股|基金|ETF|标的|证券|产品).{0,16}推荐',
        r'(?:给我|帮我|请).{0,12}(?:挑出|选出|挑选).{0,8}(?:股票|个股|基金|ETF|标的)',
        r'(?:买|卖)(?:哪|什么).{0,8}(?:股票|个股|基金|ETF|标的|证券)?',
        r'(?:哪|什么).{0,8}(?:股票|个股|基金|ETF|标的|证券).{0,12}(?:买|卖)',
        r'(?:能|可以|适合|值得|应该)(?:买|卖)(?:吗|么|嘛)?',
        r'(?:潜力股|牛股|必涨股)',
        r'recommend.{0,24}(?:stock|fund|etf|security)',
        r'which.{0,24}(?:stock|fund|etf|security).{0,24}(?:buy|sell)',
    )
)


def build_parser():
    parser = argparse.ArgumentParser(description='查询并深度分析 Arkvol 多市场金融数据')
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument('--page', choices=PAGE_DEFINITIONS.keys())
    selector.add_argument('--query', help='用于匹配页面的自然语言问题')
    selector.add_argument('--check-update', action='store_true', help='仅检查 Skill 是否有新版本')
    parser.add_argument('--api-key', help='临时覆盖配置文件中的 API Key')
    parser.add_argument('--config', help='API Key 配置文件路径，默认使用 ~/.arkvol/arkvol-entry.json')
    parser.add_argument('--base-url', default='https://arkvol.com')
    parser.add_argument('--view', choices=('summary', 'full'), default='full', help='数据视图，默认返回完整数据')
    parser.add_argument('--json', action='store_true', dest='as_json', help='输出完整原始 JSON')
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
    payload = client.fetch_page(page_id, view=getattr(args, 'view', 'full'))
    if args.as_json:
        return json.dumps(payload, ensure_ascii=False, indent=2)
    return format_readable(payload)


def ensure_query_allowed(query_text):
    text = (query_text or '').strip()
    if any(pattern.search(text) for pattern in _STOCK_RECOMMENDATION_PATTERNS):
        raise ValueError(
            '本 Skill 不提供具体证券的买入/卖出推荐或荐股名单；'
            '可以继续提供完整数据、筛选、排名、预测、估值、目标价和策略分析。'
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


def format_readable(payload):
    data = payload.get('data') if isinstance(payload, dict) else None
    if not isinstance(data, dict):
        raise ArkvolClientError('Arkvol 返回格式错误：缺少 data 对象')

    lines = [data.get('title') or data.get('page') or 'Arkvol 数据']
    if data.get('as_of'):
        lines.append(f"数据日期：{data['as_of']}")
    if data.get('sentiment_score') is not None:
        label = data.get('sentiment_label') or '-'
        lines.append(f"聚合分数：{data['sentiment_score']}（{label}）")
    if data.get('summary'):
        lines.append(f"结论：{data['summary']}")

    labels = {
        'metrics': '指标',
        'page_text': '页面解释',
        'items': '明细',
        'series': '时间序列',
        'original_page_data': '原始页面数据',
        'source_page_apis': '数据来源接口',
    }
    for field, label in labels.items():
        value = data.get(field)
        if value not in (None, {}, []):
            lines.append(f'{label}：{json.dumps(value, ensure_ascii=False, default=str)}')
    return '\n'.join(lines)


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
