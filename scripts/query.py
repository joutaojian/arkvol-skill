# coding: utf-8
import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from client import ArkvolClient, ArkvolClientError
from config import ArkvolConfigError, get_api_key
from pages import PAGE_DEFINITIONS, match_page, validate_page


COMPLIANCE_NOTICE = '仅作非个性化市场数据说明，不构成任何投资建议。'
QUERY_REJECTION = (
    '此工具仅提供非个性化、描述性市场数据，不提供证券、基金或 ETF 的推荐、'
    '买卖、持有、仓位、时点、目标价、收益预测或投资组合建议。'
)

_ACTIONABLE_QUERY_PATTERNS = (
    r'荐股|潜力股|牛股|黑马股|金股|推荐.{0,8}(股票|个股|基金|etf|标的|板块)|'
    r'(买入|卖出|持有|加仓|减仓|补仓|建仓|清仓|满仓|空仓|重仓|轻仓|抄底|止盈|止损|仓位|目标价|择时|交易信号|投资组合|资产配置)|'
    r'(操作建议|投资建议|理财建议|怎么投|如何投|怎么配置|如何配置)|'
    r'(排名|排行|排序|筛选|优选|首选|最好|最强|最优|值得关注)|'
    r'(根据|结合).{0,12}(我的|本人).{0,12}(持仓|本金|资金|账户|风险偏好|亏损)|'
    r'(能买吗|能不能买|可不可以买|该买吗|要买吗|适合买|值得买|值得投资|什么时候买|什么时候卖)|'
    r'(哪个|哪只|哪支|哪种).{0,12}(股票|个股|基金|etf|标的|板块).{0,8}(好|强|优|买|选)|'
    r'(看涨|看跌|看多|看空|做多|做空|定投|短线|长线|回本|轮动策略|轮动信号)|'
    r'(会涨|会跌|涨吗|跌吗|未来.{0,8}(走势|价格|收益|涨|跌))|'
    r'(收益率|回报率).{0,8}(最高|更高|排名|排行)|'
    r'(预测|预判).{0,8}(涨跌|走势|价格|收益)|收益预测|涨跌概率|'
    r'(which|what).{0,20}(stock|fund|etf).{0,20}(buy|pick|choose)|'
    r'(should i|what should i).{0,20}(buy|sell|invest)|'
    r'\b(buy|sell|hold|recommend|portfolio|allocation)\b|'
    r'(target price|stop loss|take profit|position sizing|return forecast)',
)

def build_parser():
    parser = argparse.ArgumentParser(description='查询 Arkvol 市场情绪数据')
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument('--page', choices=PAGE_DEFINITIONS.keys())
    selector.add_argument('--query', help='用于匹配页面的自然语言问题')
    parser.add_argument('--api-key', help='临时覆盖配置文件中的 API Key')
    parser.add_argument('--config', help='API Key 配置文件路径，默认使用 ~/.arkvol/arkvol-entry.json')
    parser.add_argument('--base-url', default='https://arkvol.com')
    parser.add_argument('--json', action='store_true', dest='as_json', help='输出合规字段白名单 JSON')
    return parser


def run(args, client_class=ArkvolClient):
    if args.query and is_actionable_query(args.query):
        raise ValueError(QUERY_REJECTION)
    page_id = validate_page(args.page) if args.page else match_page(args.query)['page']
    api_key = get_api_key(args.api_key, config_path=args.config)
    payload = client_class(base_url=args.base_url, api_key=api_key).fetch_page(page_id)
    view = build_compliance_view(payload, page_id)
    if args.as_json:
        return json.dumps(view, ensure_ascii=False, indent=2)
    return format_readable(view)


def is_actionable_query(query):
    text = (query or '').strip()
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in _ACTIONABLE_QUERY_PATTERNS)


def build_compliance_view(payload, page_id):
    data = payload.get('data') if isinstance(payload, dict) else None
    if not isinstance(data, dict):
        raise ArkvolClientError('Arkvol 返回格式错误')

    view = {
        'source': 'Arkvol',
        'page': page_id,
        'title': PAGE_DEFINITIONS[page_id]['title'],
        'limitations': [
            '情绪指标仅描述历史或当期市场状态，不代表交易信号。',
            '不得据此预测收益、涨跌方向或作出投资决策。',
        ],
        'notice': COMPLIANCE_NOTICE,
    }

    as_of = data.get('as_of')
    if isinstance(as_of, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}(?:[ T][0-9:.+Z-]+)?', as_of.strip()):
        view['as_of'] = as_of.strip()

    score = data.get('sentiment_score')
    if isinstance(score, (int, float)) and not isinstance(score, bool) and 0 <= score <= 100:
        view['sentiment_score'] = float(score)
        view['sentiment_label'] = sentiment_label(score)
        view['metric_definitions'] = [{
            'name': '市场情绪分数',
            'description': '0至100的聚合状态指标，仅描述历史或当期市场情绪。',
        }]
    return view


def sentiment_label(score):
    if score < 20:
        return '极度恐慌'
    if score < 40:
        return '恐慌'
    if score < 60:
        return '中性'
    if score < 80:
        return '贪婪'
    return '极度贪婪'


def format_readable(view):
    lines = [view['title'], f"数据来源：{view['source']}"]
    lines.append(f"数据日期：{view.get('as_of') or '未提供'}")
    if view.get('sentiment_score') is not None:
        lines.append(f"市场情绪：{view['sentiment_label']}（{view['sentiment_score']:.1f}/100）")
    definitions = view.get('metric_definitions', [])
    if definitions:
        lines.append('指标说明：' + '；'.join(f"{item['name']}：{item['description']}" for item in definitions))
    lines.extend(f"局限：{item}" for item in view['limitations'])
    lines.append(f"说明：{view['notice']}")
    return '\n'.join(lines)


def main(argv=None):
    try:
        print(run(build_parser().parse_args(argv)))
        return 0
    except (ArkvolConfigError, ArkvolClientError, ValueError) as exc:
        print(f'错误：{exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
