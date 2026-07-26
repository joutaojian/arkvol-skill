import argparse
import json
import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1] / 'scripts'
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import query


def args(query_text=None, page=None, as_json=False, check_update=False, view='full'):
    return argparse.Namespace(
        query=query_text,
        page=page,
        api_key='test-key',
        config=None,
        base_url='https://example.test',
        view=view,
        as_json=as_json,
        check_update=check_update,
    )


class FakeClient:
    calls = 0
    version_checks = 0
    requested_views = []

    def __init__(self, **_kwargs):
        pass

    def ensure_current_version(self):
        type(self).version_checks += 1
        return {
            'current_version': '0.3.1',
            'latest_version': '0.3.1',
            'update_available': False,
            'update_required': False,
            'repository_url': 'https://github.com/joutaojian/arkvol-skill',
        }

    def fetch_page(self, page_id, view='full'):
        type(self).calls += 1
        type(self).requested_views.append(view)
        return {
            'code': 0,
            'data': {
                'page': page_id,
                'title': 'Arkvol 深度分析数据',
                'as_of': '2026-07-26',
                'sentiment_score': 72,
                'sentiment_label': '贪婪',
                'summary': '估值、动量与波动分析已完成。',
                'metrics': {'target_price': 100, 'upside_pct': 18.5},
                'items': [{'ticker': 'TEST', 'rank': 1, 'signal': 'observe'}],
                'series': [{'ticker': 'TEST', 'values': [80, 90, 95]}],
                'original_page_data': {'valuation': {'TEST': 12.5}},
                'source_page_apis': [{'id': 'ranking', 'path': '/api/ranking'}],
                'page_text': {
                    'metric_definitions': [
                        {'name': '估值排名', 'description': '比较观察标的的相对估值。'},
                    ],
                    'interpretation_guides': ['结合估值、动量和波动分析。'],
                    'notes': ['可用于筛选、排名、预测和策略研究。'],
                },
            },
            'msg': '',
        }


class AnalysisBoundaryTests(unittest.TestCase):
    def setUp(self):
        FakeClient.calls = 0
        FakeClient.version_checks = 0
        FakeClient.requested_views = []

    def test_specific_security_recommendations_are_rejected_before_api_call(self):
        prompts = [
            '推荐三只股票',
            '给我一份ETF推荐名单',
            '这个 ETF 值得买吗',
            '现在应该买哪只基金',
            '帮我挑选三只潜力股',
            'recommend three stocks to buy',
            'which ETF should I buy',
        ]
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                with self.assertRaisesRegex(ValueError, '不提供具体证券'):
                    query.run(args(query_text=prompt), client_class=FakeClient)
        self.assertEqual(FakeClient.calls, 0)
        self.assertEqual(FakeClient.version_checks, 0)

    def test_screening_ranking_prediction_and_strategy_queries_are_allowed(self):
        prompts = [
            '按估值和动量给七巨头排名',
            '筛选52周低位标的并列出客观条件',
            '预测美股未来走势',
            '测算七巨头目标价和止损位',
            '制定美股中期交易策略',
            '哪个基金收益率最高',
            '美股十万元怎么配置仓位',
        ]
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                output = query.run(args(query_text=prompt), client_class=FakeClient)
                self.assertIn('估值、动量与波动分析已完成', output)
        self.assertEqual(FakeClient.calls, len(prompts))
        self.assertEqual(FakeClient.version_checks, len(prompts))

    def test_default_full_view_exposes_all_analysis_fields(self):
        output = query.run(args(page='us7-rotation', as_json=True), client_class=FakeClient)
        payload = json.loads(output)

        self.assertEqual(payload['data']['metrics']['target_price'], 100)
        self.assertEqual(payload['data']['items'][0]['rank'], 1)
        self.assertEqual(payload['data']['series'][0]['values'], [80, 90, 95])
        self.assertEqual(payload['data']['original_page_data']['valuation']['TEST'], 12.5)
        self.assertEqual(FakeClient.requested_views, ['full'])

    def test_readable_output_includes_full_analysis_context(self):
        output = query.run(args(page='us7-rotation'), client_class=FakeClient)

        self.assertIn('"target_price": 100', output)
        self.assertIn('"rank": 1', output)
        self.assertIn('时间序列', output)
        self.assertIn('原始页面数据', output)

    def test_summary_view_remains_available(self):
        query.run(args(page='alla', as_json=True, view='summary'), client_class=FakeClient)
        self.assertEqual(FakeClient.requested_views, ['summary'])

    def test_new_market_modules_are_matched(self):
        cases = {
            '全球资金轮动如何': 'global-capital-flow',
            '中国国债温度是多少': 'debt',
            '52周低位杠杆模型有多少样本': 'low-52w-leverage',
        }
        for prompt, expected in cases.items():
            with self.subTest(prompt=prompt):
                self.assertEqual(query.match_page(prompt)['page'], expected)

    def test_check_update_can_run_without_market_page(self):
        output = query.run(args(check_update=True, as_json=True), client_class=FakeClient)
        payload = json.loads(output)
        self.assertEqual(payload['current_version'], '0.3.1')
        self.assertFalse(payload['update_required'])
        self.assertEqual(FakeClient.calls, 0)

    def test_required_update_stops_before_market_request(self):
        class FutureVersionClient(FakeClient):
            def ensure_current_version(self):
                raise query.ArkvolSkillUpdateRequired({
                    'current_version': '0.3.1',
                    'latest_version': '0.4.0',
                    'repository_url': 'https://github.com/joutaojian/arkvol-skill',
                })

        with self.assertRaises(query.ArkvolSkillUpdateRequired):
            query.run(args(page='alla'), client_class=FutureVersionClient)
        self.assertEqual(FutureVersionClient.calls, 0)


if __name__ == '__main__':
    unittest.main()
