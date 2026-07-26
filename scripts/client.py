# coding: utf-8
import json
import re
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from pages import PAGE_DEFINITIONS, validate_page


class ArkvolClientError(RuntimeError):
    pass


class ArkvolSkillUpdateRequired(ArkvolClientError):
    def __init__(self, status):
        self.status = status
        latest = status.get('latest_version') or '未知'
        current = status.get('current_version') or '未知'
        repository_url = status.get('repository_url') or 'https://github.com/joutaojian/arkvol-skill'
        super().__init__(
            f'检测到 Arkvol Skill 新版本 {latest}（当前 {current}）。'
            f'请先从 {repository_url} 升级 Skill，再重新查询。'
        )


def installed_skill_version(version_path=None):
    path = Path(version_path) if version_path else Path(__file__).resolve().parents[1] / 'VERSION'
    try:
        version = path.read_text(encoding='utf-8').strip()
    except OSError as exc:
        raise ArkvolClientError(f'无法读取 Skill VERSION：{path}') from exc
    if not re.fullmatch(r'(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)', version):
        raise ArkvolClientError(f'Skill VERSION 格式无效：{version or "空值"}')
    return version


class ArkvolClient:
    def __init__(self, base_url='https://arkvol.com', api_key=None, timeout=30, opener=None,
                 skill_version=None):
        self.base_url = (base_url or 'https://arkvol.com').rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self._opener = opener or urlopen
        self.skill_version = skill_version or installed_skill_version()

    def check_skill_version(self):
        payload = self._request_json('/api/data/skill-version', allow_missing_endpoint=True)
        status = payload.get('data') if isinstance(payload, dict) else None
        if not isinstance(status, dict):
            raise ArkvolClientError('Arkvol 版本检查返回格式错误')
        return status

    def ensure_current_version(self):
        status = self.check_skill_version()
        if status.get('update_required') is True:
            raise ArkvolSkillUpdateRequired(status)
        return status

    def fetch_page(self, page_id, view='full'):
        validate_page(page_id)
        if view not in {'summary', 'full'}:
            raise ArkvolClientError('view 必须是 summary 或 full')
        payload = self._request_json(f"{PAGE_DEFINITIONS[page_id]['endpoint']}?view={view}")
        update = payload.get('data', {}).get('skill_update') if isinstance(payload.get('data'), dict) else None
        if isinstance(update, dict) and update.get('update_required') is True:
            raise ArkvolSkillUpdateRequired(update)
        return payload

    def _request_json(self, path, allow_missing_endpoint=False):
        if not self.api_key:
            raise ArkvolClientError('缺少 API Key')
        url = f'{self.base_url}{path}'
        request = Request(url, headers={
            'X-API-Key': self.api_key,
            'X-Arkvol-Skill-Version': self.skill_version,
            'Accept': 'application/json',
        }, method='GET')
        try:
            with self._opener(request, timeout=self.timeout) as response:
                payload = json.loads(response.read().decode('utf-8'))
        except HTTPError as exc:
            if allow_missing_endpoint and exc.code == 404:
                return {
                    'code': 0,
                    'data': {
                        'current_version': self.skill_version,
                        'latest_version': self.skill_version,
                        'update_available': False,
                        'update_required': False,
                        'check_supported': False,
                    },
                    'msg': '',
                }
            payload = _read_error_payload(exc)
            if exc.code == 426:
                data = payload.get('data') if isinstance(payload, dict) else None
                status = data.get('skill_update') if isinstance(data, dict) else None
                if isinstance(status, dict):
                    raise ArkvolSkillUpdateRequired(status) from exc
                raise ArkvolClientError(
                    payload.get('msg') or 'Arkvol Skill 版本过旧，必须升级后重试'
                ) from exc
            message = payload.get('msg') if isinstance(payload, dict) else None
            if exc.code == 401:
                raise ArkvolClientError(message or 'API Key 无效或缺失') from exc
            if exc.code == 403:
                raise ArkvolClientError(message or 'API Key 已禁用或账户无权访问') from exc
            raise ArkvolClientError(message or f'Arkvol 服务返回 HTTP {exc.code}') from exc
        except URLError as exc:
            raise ArkvolClientError(f'无法连接 Arkvol：{exc.reason}') from exc
        except (ValueError, UnicodeDecodeError) as exc:
            raise ArkvolClientError('Arkvol 返回了无法解析的数据') from exc

        if not isinstance(payload, dict):
            raise ArkvolClientError('Arkvol 返回格式错误')
        if payload.get('code') != 0:
            raise ArkvolClientError(payload.get('msg') or 'Arkvol 数据查询失败')
        return payload


def _read_error_payload(error):
    try:
        return json.loads(error.read().decode('utf-8'))
    except Exception:
        return {}


__all__ = [
    'ArkvolClient',
    'ArkvolClientError',
    'ArkvolSkillUpdateRequired',
    'installed_skill_version',
]
