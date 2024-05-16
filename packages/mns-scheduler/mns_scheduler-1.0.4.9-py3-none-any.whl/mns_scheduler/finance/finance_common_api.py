import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)

import mns_common.component.common_service_fun_api as common_service_fun_api
from mns_common.db.MongodbUtil import MongodbUtil
import mns_common.constant.db_name_constant as db_name_constant

mongodb_util = MongodbUtil('27017')


def get_sec_code(symbol):
    classification = common_service_fun_api.classify_symbol_one(symbol)
    if classification in ['K', 'H']:
        return 'SH' + symbol
    elif classification in ['C', 'S']:
        return 'SZ' + symbol
    else:
        return 'BJ' + symbol


# 查询利润表数据
def find_profit_report(period_time):
    query = {"REPORT_DATE": period_time}
    return mongodb_util.find_query_data(db_name_constant.EM_STOCK_PROFIT, query)


# 查询资产表
def find_asset_liability_report(period_time):
    query = {"REPORT_DATE": period_time}
    return mongodb_util.find_query_data(db_name_constant.EM_STOCK_ASSET_LIABILITY, query)
