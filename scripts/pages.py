# coding: utf-8

PAGE_DEFINITIONS = {
    'alla': {
        'title': 'A股箱格贪婪分析',
        'route': '/alla',
        'endpoint': '/api/data/alla',
        'description': 'A股宽基、市值层级及相关市场情绪结构',
        'keywords': ['A股', '大盘', '沪深', '上证', '深证', '全A', '两市', 'A股情绪'],
    },
    'alla-tech': {
        'title': 'AI硬件科技板块箱格贪婪分析',
        'route': '/alla-tech',
        'endpoint': '/api/data/alla-tech',
        'description': 'AI、半导体、芯片和科技硬件板块情绪',
        'keywords': ['科技', 'AI', '半导体', 'TMT', '科创板', '芯片', '科技情绪'],
    },
    'funds-greed': {
        'title': 'A股基金贪婪指数',
        'route': '/funds-greed',
        'endpoint': '/api/data/funds-greed',
        'description': '基金、ETF、宽基和板块贪婪指数',
        'keywords': ['基金', 'ETF', '宽基', '指数基金', '基民', 'LOF', '基金情绪'],
    },
    'gll': {
        'title': 'A股ETF乖离率分析',
        'route': '/gll',
        'endpoint': '/api/data/gll',
        'description': 'A股ETF乖离率及全球、港股、海外相关ETF',
        'keywords': ['港股', '恒生', '恒指', '全球', '海外', '全球市场', '乖离率', 'GLL'],
    },
    'greed-mid-term': {
        'title': '美股中期贪婪指数',
        'route': '/greed/mid-term',
        'endpoint': '/api/data/greed/mid-term',
        'description': '美股贪婪指数、中期趋势和中线信号',
        'keywords': ['美股贪婪', '恐慌贪婪', '中期', '中线', '趋势', '走势', '中期信号'],
    },
    'us7-rotation': {
        'title': '美股七姐妹长投轮动策略',
        'route': '/us7-rotation',
        'endpoint': '/api/data/us7-rotation',
        'description': '美股七巨头、Mag7估值与轮动',
        'keywords': ['美股', '纳斯达克', '七巨头', '七姐妹', 'Mag7', '科技七雄', '轮动', '标普'],
    },
    'global-capital-flow': {
        'title': '全球资金流蛋糕模型',
        'route': '/global-capital-flow',
        'endpoint': '/api/data/global-capital-flow',
        'description': '五个市场的风险偏好代理、相对份额和美元美债流动性闸门',
        'keywords': ['全球资金流', '全球资金轮动', '资金蛋糕', '全球轮动', '市场轮动', '风险偏好', '流动性闸门', '美元美债'],
    },
    'debt': {
        'title': '中国国债温度',
        'route': '/debt-temp',
        'endpoint': '/api/data/debt',
        'description': '中国 30 年期国债收益率和债券价格温度',
        'keywords': ['国债', '债券', '债市', '30年期', '国债收益率', '国债温度'],
    },
    'low-52w-leverage': {
        'title': '52 周低位杠杆样本统计',
        'route': '/52-week-low-leverage',
        'endpoint': '/api/data/low-52w-leverage',
        'description': 'GGBL 样本的 52 周价格位置聚合统计',
        'keywords': ['52周低位', '52周最低', '52周低点', '低位杠杆', '杠杆模型', 'GGBL'],
    },
}

SAFE_PAGE_VIEWS = {
    'alla': {
        'title': 'A 股市场情绪数据',
        'metric_name': '市场情绪分数',
        'metric_description': '0至100的聚合状态指标，仅描述历史或当期市场情绪。',
        'statistics': ('tracked_etfs',),
    },
    'alla-tech': {
        'title': 'A 股科技板块市场情绪数据',
        'metric_name': '科技板块情绪分数',
        'metric_description': '0至100的聚合状态指标，仅描述科技 ETF 的当期市场情绪。',
        'statistics': ('tracked_etfs', 'low_sentiment_count'),
    },
    'funds-greed': {
        'title': 'A 股基金市场情绪数据',
        'metric_name': '基金板块情绪分数',
        'metric_description': '0至100的聚合状态指标，仅描述基金板块的当期市场情绪。',
        'statistics': ('sector_count', 'fund_count'),
    },
    'gll': {
        'title': 'A 股 ETF 乖离率统计',
        'metric_name': '聚合市场情绪分数',
        'metric_description': '如有值，仅用于描述当期聚合市场状态。',
        'statistics': ('etf_count', 'average_liability_rate'),
    },
    'greed-mid-term': {
        'title': '美股中期市场情绪数据',
        'metric_name': '美股中期情绪分数',
        'metric_description': '0至100的聚合状态指标，仅描述美股观察样本的当期市场情绪。',
        'statistics': ('tracked_tickers', 'custom_tickers'),
    },
    'us7-rotation': {
        'title': '美股七姐妹市场状态数据',
        'metric_name': '七姐妹聚合情绪分数',
        'metric_description': '0至100的聚合状态指标，仅描述观察样本的当期市场情绪。',
        'statistics': ('stock_count', 'low_valuation_count'),
    },
    'global-capital-flow': {
        'title': '全球市场风险偏好统计',
        'metric_name': '全球风险偏好分数',
        'metric_description': '0至100的五市场风险偏好代理；大于等于55为扩张，小于等于45为收缩，其余为平衡。',
        'statistics': ('cake_index', 'market_count', 'eligible_market_count', 'macro_pressure_score'),
    },
    'debt': {
        'title': '中国国债温度数据',
        'metric_name': '国债价格温度',
        'metric_description': '0至100的30年期国债收益率逆向分位温度；收益率越低，价格温度越高，并按极冷至过热分档。',
        'statistics': ('current_rate_30y', 'range_min_rate', 'range_max_rate', 'history_points'),
    },
    'low-52w-leverage': {
        'title': '52 周低位样本聚合统计',
        'metric_name': '聚合市场情绪分数',
        'metric_description': '如有值，仅用于描述当期聚合市场状态。',
        'statistics': ('threshold_pct', 'scanned_count', 'matched_count', 'stale_count'),
    },
}

_EXPLICIT_GLOBAL_FLOW = ['全球资金流', '全球资金轮动', '资金蛋糕', '全球轮动', '市场轮动', '流动性闸门', '美元美债']
_EXPLICIT_US7 = ['美股七巨头', '美股七姐妹', '七巨头', '七姐妹', 'mag7', '科技七雄', '轮动']
_EXPLICIT_MID_TERM = ['美股贪婪', '恐慌贪婪', '中期', '中线', '中期信号']
_GENERAL_US = ['美股', '纳指', '纳斯达克', '标普']


def core_pages():
    return [{'page': page_id, **definition} for page_id, definition in PAGE_DEFINITIONS.items()]


def match_page(query):
    text = (query or '').strip()
    if not text:
        raise ValueError('请输入要查询的市场或页面关键词')
    lowered = ''.join(text.lower().split())

    if any(''.join(keyword.lower().split()) in lowered for keyword in _EXPLICIT_GLOBAL_FLOW):
        return _match_result('global-capital-flow', '命中全球资金流、资金蛋糕或流动性闸门优先规则')
    if any(''.join(keyword.lower().split()) in lowered for keyword in _EXPLICIT_US7):
        return _match_result('us7-rotation', '命中七巨头、Mag7 或轮动优先规则')
    if any(''.join(keyword.lower().split()) in lowered for keyword in _EXPLICIT_MID_TERM):
        return _match_result('greed-mid-term', '命中美股贪婪或中期趋势优先规则')
    if any(''.join(keyword.lower().split()) in lowered for keyword in _GENERAL_US):
        return _match_result('greed-mid-term', '通用美股市场查询使用中期聚合情绪页')

    matches = []
    for page_id, definition in PAGE_DEFINITIONS.items():
        found = [keyword for keyword in definition['keywords'] if ''.join(keyword.lower().split()) in lowered]
        if found:
            matches.append((len(found), max(len(keyword) for keyword in found), page_id, found))
    if not matches:
        raise ValueError('未识别查询页面，请明确说明 A股、科技、基金、乖离率、美股中期、七巨头、全球资金流、国债或 52 周低位')
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
