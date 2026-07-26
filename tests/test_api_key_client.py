import json
import sys
import tempfile
import unittest
from pathlib import Path


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

    def test_all_supported_pages_use_api_key_header_and_summary_view(self):
        requests = []

        def opener(request, timeout):
            requests.append((request, timeout))
            return FakeResponse()

        client = ArkvolClient(base_url='https://example.test', api_key='secret-key', opener=opener)
        for page_id, definition in PAGE_DEFINITIONS.items():
            with self.subTest(page=page_id):
                self.assertEqual(client.fetch_page(page_id)['code'], 0)
                request, timeout = requests[-1]
                self.assertEqual(request.full_url, f"https://example.test{definition['endpoint']}?view=summary")
                self.assertEqual(request.get_header('X-api-key'), 'secret-key')
                self.assertEqual(request.get_header('X-arkvol-skill-version'), '0.3.0')
                self.assertEqual(timeout, 30)

        self.assertEqual(len(requests), 9)

    def test_reads_installed_version_file(self):
        self.assertEqual(installed_skill_version(), '0.3.0')

    def test_update_check_blocks_older_skill(self):
        status = {
            'current_version': '0.3.0',
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
