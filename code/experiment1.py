import matplotlib.pyplot as plt
import pandas as pd
import StrategyLearner as sl
import ManualStrategy as sm
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
            df_signal.iloc[idx] = [s, "HOLD", 0]
        elif data.iloc[i]["Shares"] < 0:
            holding += data.iloc[i]["Shares"]
            df_signal.iloc[idx] = [s, "SELL", abs(data.iloc[i]["Shares"])]
        else:
            holding += data.iloc[i]["Shares"]
            df_signal.iloc[idx] = [s, "BUY", abs(data.iloc[i]["Shares"])]
    if holding < 0:
        df_signal.iloc[-1] = [s, "BUY", 1000]
    if holding > 0:
        df_signal.iloc[-1] = [s, "SELL", 1000]
    return df_signal


def experiment_1(sym, in_sample_date, out_sample_date, svm, com, imp):
    #strategy learner
    s = sl.StrategyLearner(False, imp, com)
    s.add_evidence(sym, in_sample_date[0], in_sample_date[1], svm)

    #in sample
    trades_in = s.testPolicy(sym, in_sample_date[0], in_sample_date[1], svm)
    trades_learner_in = df_sig(trades_in, sym)
    portfolio_in = msim.compute_portvals(trades_learner_in, svm, com, imp)

    #out sample
    trades_out = s.testPolicy(sym, out_sample_date[0], out_sample_date[1], svm)
    trades_learner_out = df_sig(trades_out, sym)
    portfolio_out = msim.compute_portvals(trades_learner_out, svm, com, imp)

    #manual strategy
    m = sm.ManualStrategy(False, imp, com)
    m.add_evidence(sym, in_sample_date[0], in_sample_date[1], svm)

    # in sample
    trades_learner_in_1, buy_in, sell_in = m.testPolicy(sym, in_sample_date[0], in_sample_date[1], svm)
    portfolio_in_1 = msim.compute_portvals(trades_learner_in_1, svm, com, imp)

    # out sample
    trades_learner_out_1, buy_out, sell_out = m.testPolicy(sym, out_sample_date[0], out_sample_date[1], svm)
    portfolio_out_1 = msim.compute_portvals(trades_learner_out_1, svm, com, imp)

    # benchmark in-sample
    benchmark_in = pd.DataFrame(index=trades_in.index, columns=["Symbol", "Order", "Shares"])
    benchmark_in["Symbol"] = sym
    benchmark_in["Order"] = "HOLD"
    benchmark_in["Shares"] = 0
    benchmark_in.iloc[0] = [sym, 'BUY', 1000]
    benchmark_in.iloc[-1] = [sym, 'SELL', 1000]
    bench_in = msim.compute_portvals(benchmark_in, svm, com, imp)

    # benchmark out-sample
    benchmark_out = pd.DataFrame(index=trades_out.index, columns=["Symbol", "Order", "Shares"])
    benchmark_out["Symbol"] = sym
    benchmark_out["Order"] = "HOLD"
    benchmark_out["Shares"] = 0
    benchmark_out.iloc[0] = [sym, 'BUY', 1000]
    benchmark_out.iloc[-1] = [sym, 'SELL', 1000]
    bench_out = msim.compute_portvals(benchmark_out, svm, com, imp)


    #plot in sample
    plt.figure()
    plt.plot(portfolio_in / portfolio_in.iloc[0], label="Strategy Learner", color="blue")
    plt.plot(portfolio_in_1 / portfolio_in_1.iloc[0], label="Manual Strategy", color="red")
    plt.plot(bench_in / bench_in.iloc[0], label="Benchmark", color="purple")
    plt.legend(loc='upper left')
    plt.title("JPM Benchmark Vs Strategy_Learner Vs Manual Strategy (In-sample)")
    plt.xlabel("Date (YYYY-MM-DD)")
    plt.ylabel('Normalized Price')
    plt.xticks(pd.date_range('2008-1-1', '2010-1-1', freq='2MS'), rotation=60)
    plt.tight_layout()
    plt.savefig("./images/figure_3.png")
    plt.close()

    # plot in sample
    plt.figure()
    plt.plot(portfolio_out / portfolio_out.iloc[0], label="Strategy Learner", color="blue")
    plt.plot(portfolio_out_1 / portfolio_out_1.iloc[0], label="Manual Strategy", color="red")
    plt.plot(bench_out / bench_out.iloc[0], label="Benchmark", color="purple")
    plt.legend(loc='upper left')
    plt.title("JPM Benchmark Vs Strategy_Learner Vs Manual Strategy (Out-sample)")
    plt.xlabel("Date (YYYY-MM-DD)")
    plt.ylabel('Normalized Price')
    plt.xticks(pd.date_range('2010-1-1', '2012-1-1', freq='2MS'), rotation=60)
    plt.tight_layout()
    plt.savefig("./images/figure_4.png")
    plt.close()
    return bench_in, bench_out, portfolio_in_1, portfolio_out_1, buy_in, sell_in, buy_out, sell_out, portfolio_in, portfolio_out


