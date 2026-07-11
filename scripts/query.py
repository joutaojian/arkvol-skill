# coding: utf-8
import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from client import ArkvolClient, ArkvolClientError
from config import ArkvolConfigError, get_api_key
from pages import PAGE_DEFINITIONS, match_page, validate_page


def build_parser():
    parser = argparse.ArgumentParser(description='查询 Arkvol 市场情绪数据')
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument('--page', choices=PAGE_DEFINITIONS.keys())
    selector.add_argument('--query', help='用于匹配页面的自然语言问题')
    parser.add_argument('--api-key', help='临时覆盖配置文件中的 API Key')
    parser.add_argument('--config', help='API Key 配置文件路径，默认使用 ~/.arkvol/arkvol-entry.json')
    parser.add_argument('--base-url', default='https://arkvol.com')
    parser.add_argument('--json', action='store_true', dest='as_json', help='输出完整聚合 JSON')
    return parser


def run(args, client_class=ArkvolClient):
    page_id = validate_page(args.page) if args.page else match_page(args.query)['page']
    api_key = get_api_key(args.api_key, config_path=args.config)
    payload = client_class(base_url=args.base_url, api_key=api_key).fetch_page(page_id)
    if args.as_json:
        return json.dumps(payload, ensure_ascii=False, indent=2)
    return format_readable(payload)


def format_readable(payload):
    data = payload['data']
    lines = [data.get('title') or data.get('page', 'Arkvol 数据')]
    if data.get('as_of'):
        lines.append(f"数据日期：{data['as_of']}")
    if data.get('sentiment_score') is not None:
        lines.append(f"情绪：{data.get('sentiment_label') or '-'}（{data['sentiment_score']:.1f}/100）")
    lines.append(f"结论：{data.get('summary') or '暂无结论'}")
    definitions = data.get('page_text', {}).get('metric_definitions', [])
    if definitions:
        lines.append('指标说明：' + '；'.join(f"{item.get('name')}：{item.get('description')}" for item in definitions[:3]))
    notes = data.get('page_text', {}).get('notes', [])
    if notes:
        lines.append('提示：' + notes[0])
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
