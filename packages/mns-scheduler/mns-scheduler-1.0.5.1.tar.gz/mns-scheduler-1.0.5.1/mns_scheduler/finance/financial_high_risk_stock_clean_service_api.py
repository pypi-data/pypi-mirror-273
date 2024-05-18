import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
from datetime import datetime
import mns_common.component.self_choose.black_list_service_api as black_list_service_api
import mns_scheduler.finance.finance_common_api as finance_common_api
from loguru import logger
import mns_common.constant.db_name_constant as db_name_constant
from mns_common.db.MongodbUtil import MongodbUtil
import mns_common.component.trade_date.trade_date_common_service_api as trade_date_common_service_api
import mns_common.component.common_service_fun_api as common_service_fun_api
import pandas as pd

# 1.无保留意见/标准报告：报告没问题。（没有发现造假，但也不能保证为真）
#
# 2.带强调事项段的无保留意见：报告没问题，但是有亏损获对其可持续经营有重大疑虑（可能造假，至少是在粉饰报表）
#
# 3.保留意见报告：有问题，财务造假
#
# 4.否定意见报告：有很大问题
#
# 5.无法表示意见报告：不让查
#

mongodb_util = MongodbUtil('27017')
# 审核标准意见
OPINION_TYPE = "标准无保留意见"

# 利润为负的时候最小营业收入 主板 3.2亿
MIN_INCOME_MAIN = 320000000
# 利润为负的时候最小营业收入 科创 创业 1.2亿
MIN_INCOME_SUB = 120000000
# 最大负债比
MAX_LIABILITY_RATIO = 90
# 负载超过90%时候最小净资产
MIN_NET_ASSET = 1000000000
# 排除校验负债比的行业
EXCLUDE_INDUSTRY = ['保险', '银行', '证券']

# 最迟出报告的天数
LATE_REPORT_DAYS = 3


#### 退市新规 ####
# 1 股价类:连续20个交易日估价低于1元
# 2 市值类: 主板小于5亿、创业板3亿
# 3 财务类: (1) 利润总额 净利润 扣非净利润三者最小值为负 且营业收入小于3亿 创业板营业收入小于1元
#          (2) 资不抵债

# 财报审核
def financial_report_check(new_report_df, period_time, period, report_type):
    if period == 4:
        # 年报异常审核
        year_report_exception_check(new_report_df, period_time, report_type)
    # 负债过高
    liability_ratio_check(report_type, new_report_df, period_time)


# 年报审核异常
def year_report_exception_check(new_report_df, period_time, report_type):
    new_report_one_df = new_report_df.loc[new_report_df['REPORT_DATE'] == period_time]
    # 审核意见
    opinion_type = list(new_report_one_df['OPINION_TYPE'])[0]
    symbol = list(new_report_one_df['SECURITY_CODE'])[0]
    name = list(new_report_one_df['SECURITY_NAME_ABBR'])[0]
    now_date = datetime.now()
    str_day = now_date.strftime('%Y-%m-%d')
    str_now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')

    # 年报有问题
    if opinion_type != OPINION_TYPE:
        id_key = symbol + "_" + period_time + "_" + black_list_service_api.FINANCIAL_PROBLEM_ANNUAL_REPORT
        black_list_service_api.save_black_stock(id_key,
                                                symbol,
                                                name,
                                                str_day,
                                                str_now_date,
                                                '年报审计有问题:' + "[" + str(opinion_type) + "]",
                                                '年报审计有问题',
                                                '',
                                                black_list_service_api.FINANCIAL_PROBLEM_ANNUAL_REPORT)

    if report_type == db_name_constant.EM_STOCK_PROFIT:
        # 利润总额  净利润 扣除非经常性损益后的净利润  三者最小为负
        # 利润总额
        total_profit = list(new_report_one_df['TOTAL_PROFIT'])[0]
        #  净利润
        net_profit = list(new_report_one_df['NETPROFIT'])[0]
        # 营业利润
        operate_profit = list(new_report_one_df['OPERATE_PROFIT'])[0]
        # 持续经营净利润
        continued_profit = list(new_report_one_df['CONTINUED_NETPROFIT'])[0]
        # 归属于母公司股东的净利润
        parent_profit = list(new_report_one_df['PARENT_NETPROFIT'])[0]
        # 扣除非经常性损益后的净利润
        deduct_parent_profit = list(new_report_one_df['DEDUCT_PARENT_NETPROFIT'])[0]
        # 营业总收入
        total_operate_income = list(new_report_one_df['TOTAL_OPERATE_INCOME'])[0]
        if total_operate_income == 0:
            #  营业收入
            total_operate_income = list(new_report_one_df['OPERATE_INCOME'])[0]

            # 最小利润收入
        min_profit = min(total_profit, net_profit, operate_profit,
                         continued_profit, parent_profit, deduct_parent_profit)
        if min_profit < 0:

            classification = common_service_fun_api.classify_symbol_one(symbol)
            if ((classification in ['S', 'H'] and total_operate_income < MIN_INCOME_MAIN)
                    | (classification in ['K', 'C'] and total_operate_income < MIN_INCOME_SUB)):
                id_key = symbol + "_" + period_time + "_" + black_list_service_api.FINANCIAL_PROBLEM_PROFIT
                min_profit = round(min_profit / common_service_fun_api.TEN_THOUSAND, 1)
                total_operate_income = round(total_operate_income / common_service_fun_api.HUNDRED_MILLION, 1)

                black_list_service_api.save_black_stock(id_key,
                                                        symbol,
                                                        name,
                                                        str_day,
                                                        str_now_date,
                                                        '年报:利润:' + '[' + str(min_profit) + '万]' + '收入:' + str(
                                                            total_operate_income) + '[' + '亿元]--' + '触发退市风险',
                                                        '年报:利润:' + '[' + str(min_profit) + '万]' + '收入:' + str(
                                                            total_operate_income) + '[' + '亿元]--' + '触发退市风险',
                                                        '',
                                                        black_list_service_api.FINANCIAL_PROBLEM_PROFIT)


# 负债比校验
def liability_ratio_check(report_type, new_report_df, period_time):
    if report_type == db_name_constant.EM_STOCK_ASSET_LIABILITY:
        new_report_df = new_report_df.sort_values(by=['REPORT_DATE'], ascending=False)
        new_report_one_df = new_report_df.iloc[0:1]
        # 负债比
        liability_ratio = list(new_report_one_df['liability_ratio'])[0]
        # 净资产
        net_asset = round(list(new_report_one_df['TOTAL_ASSETS'])[0] - list(new_report_one_df['TOTAL_LIABILITIES'])[0],
                          2)

        symbol = list(new_report_one_df['SECURITY_CODE'])[0]
        name = list(new_report_one_df['SECURITY_NAME_ABBR'])[0]
        now_date = datetime.now()
        str_day = now_date.strftime('%Y-%m-%d')
        str_now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
        id_key = symbol + "_" + period_time + "_" + black_list_service_api.FINANCIAL_PROBLEM_DEBT

        query_company = {'_id': symbol, 'industry': {'$in': EXCLUDE_INDUSTRY}}
        if mongodb_util.exist_data_query(db_name_constant.COMPANY_INFO, query_company):
            return None

        if liability_ratio >= MAX_LIABILITY_RATIO:
            black_list_service_api.save_black_stock(id_key,
                                                    symbol,
                                                    name,
                                                    str_day,
                                                    str_now_date,
                                                    '负债过高:' + "[" + str(
                                                        liability_ratio) + "]" + "," + "净资产:" + str(round(
                                                        net_asset / common_service_fun_api.HUNDRED_MILLION, 0)) + "亿",
                                                    '负债过高:' + "[" + str(liability_ratio) + "]",
                                                    '',
                                                    black_list_service_api.FINANCIAL_PROBLEM_DEBT)


# 未出财报
def un_report_check(sync_time, now_year, period, period_time):
    un_report_asset_df = finance_common_api.find_un_report_symbol(period_time,
                                                                  db_name_constant.EM_STOCK_ASSET_LIABILITY)
    un_report_profit_df = finance_common_api.find_un_report_symbol(period_time,
                                                                   db_name_constant.EM_STOCK_PROFIT)
    un_report_df = pd.concat([un_report_asset_df, un_report_profit_df])
    if period == 4 or period == 1:
        last_report_day = str(now_year) + "-05-01"
    elif period == 2:
        last_report_day = str(now_year) + "-07-01"
    elif period == 3:
        last_report_day = str(now_year) + "-10-01"
    max_report_day = trade_date_common_service_api.get_before_trade_date(last_report_day, LATE_REPORT_DAYS)
    if max_report_day >= sync_time:

        for un_asset_one in un_report_df.itertuples():
            symbol = un_asset_one.symbol
            id_key = symbol + "_" + period_time + "_" + black_list_service_api.FINANCIAL_PROBLEM_NOT_REPORT
            name = un_asset_one.name
            now_date = datetime.now()
            str_day = now_date.strftime('%Y-%m-%d')
            try:

                black_list_service_api.save_black_stock(id_key,
                                                        symbol,
                                                        name,
                                                        str_day,
                                                        sync_time,
                                                        '未出财报',
                                                        '未出财报',
                                                        '',
                                                        black_list_service_api.FINANCIAL_PROBLEM_NOT_REPORT)
            except Exception as e:
                logger.error("更新未出报告异常:{},{},{}", symbol, period_time, e)
