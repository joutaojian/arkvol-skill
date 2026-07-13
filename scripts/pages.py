# coding: utf-8

PAGE_DEFINITIONS = {
    'alla': {
        'title': 'A股聚合市场情绪数据',
        'route': '/alla',
        'endpoint': '/api/data/alla',
        'description': 'A股宽基、市值层级及相关市场情绪结构',
        'keywords': ['A股', '大盘', '沪深', '上证', '深证', '全A', '两市', 'A股情绪'],
    },
    'alla-tech': {
        'title': 'AI硬件科技板块聚合情绪数据',
        'route': '/alla-tech',
        'endpoint': '/api/data/alla-tech',
        'description': 'AI、半导体、芯片和科技硬件板块情绪',
        'keywords': ['科技', 'AI', '半导体', 'TMT', '科创板', '芯片', '科技情绪'],
    },
    'funds-greed': {
        'title': 'A股基金市场情绪数据',
        'route': '/funds-greed',
        'endpoint': '/api/data/funds-greed',
        'description': '基金、ETF、宽基和板块贪婪指数',
        'keywords': ['基金', 'ETF', '宽基', '指数基金', '基民', 'LOF', '基金情绪'],
    },
    'gll': {
        'title': 'A股ETF乖离率数据',
        'route': '/gll',
        'endpoint': '/api/data/gll',
        'description': 'A股ETF乖离率及全球、港股、海外相关ETF',
        'keywords': ['港股', '恒生', '恒指', '全球', '海外', '全球市场', '乖离率', 'GLL'],
    },
    'greed-mid-term': {
        'title': '美股中期市场情绪数据',
        'route': '/greed/mid-term',
        'endpoint': '/api/data/greed/mid-term',
        'description': '美股贪婪指数和中期市场情绪观察',
        'keywords': ['美股', '美股贪婪', '恐慌贪婪', '中期情绪', '美股情绪'],
    },
    'us7-rotation': {
        'title': '美股七巨头历史相对表现数据',
        'route': '/us7-rotation',
        'endpoint': '/api/data/us7-rotation',
        'description': '美股七巨头和Mag7历史相对表现数据',
        'keywords': ['七巨头', '七姐妹', 'Mag7', '科技七雄'],
    },
}

_EXPLICIT_US7 = ['美股七巨头', '美股七姐妹', '七巨头', '七姐妹', 'mag7', '科技七雄']
_EXPLICIT_MID_TERM = ['美股贪婪', '恐慌贪婪', '美股中期', '美股情绪', '美股']


def core_pages():
    return [{'page': page_id, **definition} for page_id, definition in PAGE_DEFINITIONS.items()]


def match_page(query):
    text = (query or '').strip()
    if not text:
        raise ValueError('请输入要查询的市场或页面关键词')
    lowered = ''.join(text.lower().split())

    if any(''.join(keyword.lower().split()) in lowered for keyword in _EXPLICIT_US7):
        return _match_result('us7-rotation', '命中七巨头或 Mag7 优先规则')
    if any(''.join(keyword.lower().split()) in lowered for keyword in _EXPLICIT_MID_TERM):
        return _match_result('greed-mid-term', '命中美股贪婪或中期情绪优先规则')

    matches = []
    for page_id, definition in PAGE_DEFINITIONS.items():
        found = [keyword for keyword in definition['keywords'] if ''.join(keyword.lower().split()) in lowered]
        if found:
            matches.append((len(found), max(len(keyword) for keyword in found), page_id, found))
    if not matches:
        raise ValueError('未识别查询页面，请明确说明 A股、科技、基金、乖离率、美股中期情绪或七巨头历史表现')
    matches.sort(reverse=True)
    _, _, page_id, found = matches[0]
    return _match_result(page_id, f"命中关键词：{', '.join(found)}")


def validate_page(page_id):
    if page_id not in PAGE_DEFINITIONS:
        allowed = ', '.join(PAGE_DEFINITIONS)
        raise ValueError(f'未知页面 {page_id}，可选值：{allowed}')
    return page_id


def _match_result(page_id, reason):
    return {'page': page_id, **PAGE_DEFINITIONS[page_id], 'reason': reason}
