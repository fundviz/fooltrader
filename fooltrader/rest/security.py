# -*- coding: utf-8 -*-
from flask import request, Blueprint

from fooltrader.consts import CRYPTOCURRENCY_PAIR, SECURITY_TYPE_MAP_EXCHANGES
from fooltrader.domain.data.es_quote import CryptocurrencyMeta
from fooltrader.rest.common import success

security_rest = Blueprint('security', __name__,
                          template_folder='templates')


@security_rest.route('/security', methods=['GET'])
def get_security():
    security_type = request.args.get('securityType')
    exchange = request.args.get('exchange')

    if not exchange:
        exchange = SECURITY_TYPE_MAP_EXCHANGES[security_type]
    else:
        exchange = [exchange]

    if security_type == 'cryptocurrency':
        doc_type = CryptocurrencyMeta

    s = doc_type().search()
    s = s.filter('terms', exchange=exchange).filter('terms', name=CRYPTOCURRENCY_PAIR)

    results = s.execute()

    return success(results['hits'].to_dict())
