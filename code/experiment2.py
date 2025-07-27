import matplotlib.pyplot as plt
import pandas as pd
import StrategyLearner as sl
import numpy as np
import marketsimcode as msim


def author():
    # gatech username
    return "ssubedi33"


def study_group():
    # No study group
    return "ssubedi33"

def df_sig(data, s):
    df_signal = pd.DataFrame(index=data.index, columns=["Symbol", "Order", "Shares"])
    df_signal["Symbol"] = s
    df_signal["Order"] = "HOLD"
    df_signal["Shares"] = 0
    idx = 0
    holding = 0
    for i in range(0, len(data)-1):
        idx += 1
        if data.iloc[i]["Shares"] == 0:
            df_signal.iloc[i] = [s, "HOLD", 0]
        elif data.iloc[i]["Shares"] < 0:
            holding += data.iloc[i]["Shares"]
            df_signal.iloc[i] = [s, "SELL", abs(data.iloc[i]["Shares"])]
        else:
            holding += data.iloc[i]["Shares"]
            df_signal.iloc[i] = [s, "BUY", abs(data.iloc[i]["Shares"])]
    if holding < 0:
        df_signal.iloc[-1] = [s, "BUY", 1000]
    if holding > 0:
        df_signal.iloc[-1] = [s, "SELL", 1000]
    return df_signal


def experiment_2(sym, in_sample_date, svm, com, imp):
    # strategy learner
    s = sl.StrategyLearner(False, imp[0], com)
    s.add_evidence(sym, in_sample_date[0], in_sample_date[1], svm)

    # in sample
    trades_in = s.testPolicy(sym, in_sample_date[0], in_sample_date[1], svm)
    trades_learner_in = df_sig(trades_in, sym)
    portfolio_in = msim.compute_portvals(trades_learner_in, svm, com, imp[0])

    #Metrics
    port_val_norm = portfolio_in / portfolio_in.iloc[0]
    port_daily_ret = (port_val_norm / port_val_norm.shift(1)) - 1
    port_daily_ret = port_daily_ret[1:]
    daily_return_mean = round(port_daily_ret.mean(), 6)
    std = round(port_daily_ret.std(), 6)
    cr = round((portfolio_in[-1] / portfolio_in[0]) - 1, 6)

    # strategy learner
    s1 = sl.StrategyLearner(False, imp[1], com)
    s1.add_evidence(sym, in_sample_date[0], in_sample_date[1], svm)

    # in sample
    trades_in_1 = s1.testPolicy(sym, in_sample_date[0], in_sample_date[1], svm)
    trades_learner_in_1 = df_sig(trades_in_1, sym)
    portfolio_in_1 = msim.compute_portvals(trades_learner_in_1, svm, com, imp[1])

    # Metrics
    port_val_norm_1 = portfolio_in_1 / portfolio_in_1.iloc[0]
    port_daily_ret_1 = (port_val_norm_1 / port_val_norm_1.shift(1)) - 1
    port_daily_ret_1 = port_daily_ret_1[1:]
    daily_return_mean_1 = round(port_daily_ret_1.mean(), 6)
    std_1 = round(port_daily_ret_1.std(), 6)
    cr_1 = round((portfolio_in_1[-1] / portfolio_in_1[0]) - 1, 6)

    # strategy learner
    s2 = sl.StrategyLearner(False, imp[2], com)
    s2.add_evidence(sym, in_sample_date[0], in_sample_date[1], svm)

    # in sample
    trades_in_2 = s2.testPolicy(sym, in_sample_date[0], in_sample_date[1], svm)
    trades_learner_in_2 = df_sig(trades_in_2, sym)
    portfolio_in_2 = msim.compute_portvals(trades_learner_in_2, svm, com, imp[2])

    # Metrics
    port_val_norm_2 = portfolio_in_2 / portfolio_in_2.iloc[0]
    port_daily_ret_2 = (port_val_norm_2 / port_val_norm_2.shift(1)) - 1
    port_daily_ret_2 = port_daily_ret_2[1:]
    daily_return_mean_2 = round(port_daily_ret_2.mean(), 6)
    std_2 = round(port_daily_ret_2.std(), 6)
    cr_2 = round((portfolio_in_2[-1] / portfolio_in_2[0]) - 1, 6)

    #plot
    plt.figure()
    plt.plot(port_val_norm, label="Impact = 0.0", color="blue")
    plt.plot(port_val_norm_1, label="Impact = 0.01", color="red")
    plt.plot(port_val_norm_2, label="Impact = 0.02", color="purple")
    plt.legend(loc='upper left')
    plt.title("Normalized Portfolio for different for different impact")
    plt.xlabel("Date (YYYY-MM-DD)")
    plt.ylabel('Normalized Price')
    plt.xticks(pd.date_range('2008-1-1', '2010-1-1', freq='2MS'), rotation=60)
    plt.tight_layout()
    plt.savefig("./images/figure_5.png")
    plt.close()

    #get metrics
    daily_list = [daily_return_mean, daily_return_mean_1,daily_return_mean_2]
    sharpe_list = [-1*np.sqrt(252)*(daily_return_mean/std), -1*np.sqrt(252)*(daily_return_mean_1/std_1), -1*np.sqrt(252)*(daily_return_mean_2/std_2)]
    cr_list = [cr, cr_1, cr_2]

    # Plot metrics
    labels = ['Impact = 0.0', 'Impact = 0.01', 'Impact = 0.02']
    width = 0.35
    plt.figure()
    fig, axs = plt.subplots(1, 3, figsize=(16, 5))

    # Daily Return Mean
    axs[0].bar(labels, daily_list, width, color='blue')
    axs[0].set_title('Daily Return Mean Vs Impact')
    axs[0].set_ylabel('Mean')
    axs[0].set_ylim(0, max(daily_list) * 1.25)

    # Sharpe Ratio
    axs[1].bar(labels, sharpe_list, width, color='red')
    axs[1].set_title('Sharpe Ratio Vs Impact')
    axs[1].set_ylabel('Sharpe Ratio')
    axs[1].set_ylim(0, max(sharpe_list) * 5.5)

    # Cumulative Return
    axs[2].bar(labels, cr_list, width, color='orange')
    axs[2].set_title('Cumulative Return Vs Impact')
    axs[2].set_ylabel('Cumulative Return')
    axs[2].set_ylim(0, max(cr_list) * 1.2)

    plt.tight_layout()
    plt.savefig("./images/figure_6.png")
    plt.close()

