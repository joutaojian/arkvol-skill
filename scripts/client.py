# coding: utf-8
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from pages import PAGE_DEFINITIONS, validate_page


class ArkvolClientError(RuntimeError):
    pass


class ArkvolClient:
    def __init__(self, base_url='https://arkvol.com', api_key=None, timeout=30, opener=None):
        self.base_url = (base_url or 'https://arkvol.com').rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self._opener = opener or urlopen

    def fetch_page(self, page_id):
        validate_page(page_id)
        if not self.api_key:
            raise ArkvolClientError('缺少 API Key')
        url = f"{self.base_url}{PAGE_DEFINITIONS[page_id]['endpoint']}"
        request = Request(url, headers={'X-API-Key': self.api_key, 'Accept': 'application/json'}, method='GET')
        try:
            with self._opener(request, timeout=self.timeout) as response:
                payload = json.loads(response.read().decode('utf-8'))
        except HTTPError as exc:
            payload = _read_error_payload(exc)
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


__all__ = ['ArkvolClient', 'ArkvolClientError']
