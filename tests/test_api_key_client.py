import json
import sys
import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError


SCRIPT_DIR = Path(__file__).resolve().parents[1] / 'scripts'
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from client import (
    ArkvolClient,
    ArkvolSkillUpdateRequired,
    installed_skill_version,
)
from config import ArkvolConfigError, get_api_key
from pages import PAGE_DEFINITIONS


class FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return b'{"code": 0, "data": {}, "msg": ""}'


class ApiKeyClientTests(unittest.TestCase):
    def test_api_key_precedence_and_environment_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / 'arkvol-entry.json'
            config_path.write_text(json.dumps({'api_key': 'file-key'}), encoding='utf-8')

            self.assertEqual(
                get_api_key('cli-key', env={'ARKVOL_API_KEY': 'env-key'}, config_path=config_path),
                'cli-key',
            )
            self.assertEqual(
                get_api_key(env={'ARKVOL_API_KEY': 'env-key'}, config_path=config_path),
                'file-key',
            )
            self.assertEqual(
                get_api_key(
                    env={'ARKVOL_API_KEY': 'env-key'},
                    config_path=Path(directory) / 'missing.json',
                ),
                'env-key',
            )

    def test_missing_key_has_actionable_setup_message(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ArkvolConfigError, 'arkvol.com'):
                get_api_key(env={}, config_path=Path(directory) / 'missing.json')

    def test_all_supported_pages_use_api_key_header_and_full_view(self):
        requests = []

        def opener(request, timeout):
            requests.append((request, timeout))
            return FakeResponse()

        client = ArkvolClient(base_url='https://example.test', api_key='secret-key', opener=opener)
        for page_id, definition in PAGE_DEFINITIONS.items():
            with self.subTest(page=page_id):
                self.assertEqual(client.fetch_page(page_id)['code'], 0)
                request, timeout = requests[-1]
                self.assertEqual(request.full_url, f"https://example.test{definition['endpoint']}?view=full")
                self.assertEqual(request.get_header('X-api-key'), 'secret-key')
                self.assertEqual(request.get_header('X-arkvol-skill-version'), '0.3.1')
                self.assertEqual(timeout, 30)

        self.assertEqual(len(requests), 9)

    def test_reads_installed_version_file(self):
        self.assertEqual(installed_skill_version(), '0.3.1')

    def test_summary_view_can_be_requested_explicitly(self):
        requests = []

        def opener(request, timeout):
            requests.append((request, timeout))
            return FakeResponse()

        client = ArkvolClient(base_url='https://example.test', api_key='secret-key', opener=opener)
        client.fetch_page('alla', view='summary')
        self.assertTrue(requests[0][0].full_url.endswith('/api/data/alla?view=summary'))

    def test_upgrade_required_response_raises_version_exception(self):
        status = {
            'current_version': '0.2.0',
            'latest_version': '0.3.1',
            'update_available': True,
            'update_required': True,
            'repository_url': 'https://github.com/joutaojian/arkvol-skill',
        }
        body = json.dumps({
            'code': 426,
            'data': {'skill_update': status},
            'msg': 'ARKVOL_SKILL_UPDATE_REQUIRED',
        }).encode('utf-8')

        def opener(request, timeout):
            raise HTTPError(request.full_url, 426, 'Upgrade Required', {}, BytesIO(body))

        client = ArkvolClient(base_url='https://example.test', api_key='secret-key', opener=opener)
        with self.assertRaisesRegex(ArkvolSkillUpdateRequired, '0.3.1'):
            client.fetch_page('alla')

    def test_update_check_blocks_older_skill(self):
        status = {
            'current_version': '0.3.1',
            'latest_version': '0.4.0',
            'update_available': True,
            'update_required': True,
            'repository_url': 'https://github.com/joutaojian/arkvol-skill',
        }

        class VersionResponse(FakeResponse):
            def read(self):
                return json.dumps({'code': 0, 'data': status, 'msg': ''}).encode('utf-8')

        client = ArkvolClient(
            base_url='https://example.test',
            api_key='secret-key',
            opener=lambda _request, timeout: VersionResponse(),
        )
        with self.assertRaisesRegex(ArkvolSkillUpdateRequired, '0.4.0'):
            client.ensure_current_version()


if __name__ == '__main__':
    unittest.main()
