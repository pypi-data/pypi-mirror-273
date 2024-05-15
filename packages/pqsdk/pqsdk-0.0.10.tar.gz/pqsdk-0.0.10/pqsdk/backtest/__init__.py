# coding=utf-8
from .main import BacktestExecutor
import pqsdk.utils.file_util as fu
import json
import faxdatasdk
from pqsdk import log
import pandas as pd
import quantstats as qs
from pathlib import Path
import datetime
import os


def execute(parameters: dict, script: str = None, strategy_file: str = None):
    # 登录faxdatasdk
    config_file = 'config.sdk.json'
    if not fu.check_path_exists(config_file):
        print("未找到配置文件. 请先运行命令进行配置: pqsdk config")
        exit(-1)

    with open(config_file, 'r', encoding='utf-8') as f:
        sdk_config = json.loads(f.read())
    faxdatasdk.auth_by_token(token=sdk_config['token'], host=sdk_config['host'], audience=sdk_config['audience'])

    if strategy_file:
        strategy_file = os.path.splitext(strategy_file)[0]
    kwargs = {"parameters": parameters, "script": script, "strategy_file": strategy_file}
    executor = BacktestExecutor(kwargs=kwargs)
    results = executor.run()
    return results


def tearsheet(results: dict, save_path="storage/reports"):
    """
    保存回测结果到Tearsheet

    :param save_path: 保存路径
    :param results:
    :return None: .
    """
    log.info("生成Tearsheet, 请稍后...")

    # 计算总市值时间序列
    total_values = results['analysis']['time_return']['total_values']
    stats_df = pd.DataFrame({'total_value': total_values})
    stats_df.index = pd.to_datetime(stats_df.index)
    # stats_df["diff"] = stats_df["total_value"].diff().dropna()
    # stats_df["diff"] = stats_df["diff"].abs().cumsum()
    # stats_df = stats_df[stats_df["diff"] > 0]

    if stats_df.empty:
        log.warning(f"总资产没有变动，放弃生成Tearsheet")
        return

    strat_returns = qs.utils.rebase(stats_df['total_value'])
    strat_returns = qs.utils.to_returns(strat_returns)

    # 计算benchmark收盘价时间序列
    bchmk = results['analysis']['time_return']['bchmk_returns']
    bchmk_df = pd.DataFrame({'bchmk_returns': bchmk})
    bchmk_df.index = pd.to_datetime(bchmk_df.index)
    # 重命名benchmark的Column名称，用于Tearsheet显示
    bchmk_df = bchmk_df.rename(columns={"bchmk_returns": results['benchmark']})
    # bchmk_df = bchmk_df.loc[stats_df.index]  # 以持仓日期列表保留benchmark的记录
    bchmk_returns = bchmk_df[results['benchmark']]

    # tearsheet保存路径
    ts_path = Path(save_path)
    ts_path.mkdir(parents=True, exist_ok=True)
    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = (
            "tearsheet"
            + "-"
            + time_str.replace("-", "").replace(":", "").replace(" ", "-")
            + ".html"
    )
    filepath = ts_path / filename

    title = f"回测报告 {time_str}"
    qs.reports.html(
        strat_returns,
        benchmark=bchmk_returns,
        title=title,
        output=filepath,
        download_filename=filepath
    )

    log.info(f"Tearsheet创建完成，路径：{filepath}")


def save_results(results: dict, save_path="storage/results"):
    """
    保存最终回测结果
    :param results:
    :param save_path: 保存路径
    :return:
    """
    # 计算总市值时间序列
    returns = results['analysis']['time_return']['returns']
    total_values = results['analysis']['time_return']['total_values']
    market_values = results['analysis']['time_return']['market_values']
    cash = results['analysis']['time_return']['cash']
    pnls = results['analysis']['time_return']['pnls']
    bchmk_returns = results['analysis']['time_return']['bchmk_returns']
    total_values_df = pd.DataFrame({'return': returns,  # 策略收益率
                                    'total_value': total_values,  # 总资产
                                    'market_value': market_values,  # 总市值
                                    'cash': cash,  # 现金
                                    'pnl': pnls,  # 盈亏
                                    'bchmk_return': bchmk_returns  # 基准收益率
                                    })
    total_values_df.index = pd.to_datetime(total_values_df.index)
    total_values_df.index.name = "trade_date"
    total_values_df['total_value_'] = qs.utils.rebase(total_values_df['total_value'])  # rebase的总资产
    total_values_df['strat_return'] = qs.utils.to_returns(total_values_df['total_value_'])  # 通过总资产的变化算收益率
    total_values_df['cum_returns'] = (1 + total_values_df['strat_return']).cumprod() - 1  # 累计收益率

    run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = Path(save_path)
    file_path.mkdir(parents=True, exist_ok=True)
    filename = ("results" + "_" + run_time.replace("-", "").replace(":", "").replace(" ", "_") + ".csv")
    file_path = file_path / filename
    log.info(f"save results data: {file_path}")
    total_values_df.to_csv(file_path, index=True)


def save_orders(results: dict, save_path="storage/orders"):
    orders_df: pd.DataFrame = results['orders']
    run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = Path(save_path)
    file_path.mkdir(parents=True, exist_ok=True)
    filename = ("orders" + "_" + run_time.replace("-", "").replace(":", "").replace(" ", "_") + ".csv")
    file_path = file_path / filename
    log.info(f"save orders data: {file_path}")
    orders_df.to_csv(file_path, index=False)


# ---------------------------------------------------------
# 外部可以访问的列表
# ---------------------------------------------------------
__all__ = ["execute", "tearsheet", "save_results", "save_orders"]
