# coding: utf-8
import json
import os
from pathlib import Path


class ArkvolConfigError(ValueError):
    pass


def bundled_config_path():
    return Path(__file__).resolve().parents[1] / 'shared' / 'arkvol-entry.json'


def user_config_path(home=None):
    return Path(home).expanduser() / '.arkvol' / 'arkvol-entry.json' if home else Path.home() / '.arkvol' / 'arkvol-entry.json'


def default_config_path():
    return user_config_path()


def get_api_key(cli_api_key=None, env=None, config_path=None, home=None):
    if cli_api_key and cli_api_key.strip():
        return cli_api_key.strip()

    paths = (
        [Path(config_path).expanduser()]
        if config_path
        else [user_config_path(home), bundled_config_path()]
    )
    for path in paths:
        if not path.is_file():
            continue
        try:
            payload = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc:
            raise ArkvolConfigError(f'无法读取 Arkvol 配置文件 {path}：{exc}') from exc
        file_key = payload.get('api_key') if isinstance(payload, dict) else None
        if file_key and str(file_key).strip():
            return str(file_key).strip()
        raise ArkvolConfigError(f'Arkvol 配置文件 {path} 缺少有效的 api_key')

    env = os.environ if env is None else env
    env_key = env.get('ARKVOL_API_KEY')
    if env_key and env_key.strip():
        return env_key.strip()

    recommended_path = paths[0]
    raise ArkvolConfigError(
        '未配置 Arkvol API Key。\n'
        '1. 前往 https://arkvol.com 注册或登录。\n'
        '2. 点击右上角头像，进入“API Key”页面并创建 Key。\n'
        f'3. 将 Key 写入 {recommended_path} 的 api_key 字段。\n'
        '也可以使用 --config 指定其他配置文件，或设置 ARKVOL_API_KEY。'
    )


__all__ = [
    'ArkvolConfigError',
    'bundled_config_path',
    'default_config_path',
    'get_api_key',
    'user_config_path',
]
