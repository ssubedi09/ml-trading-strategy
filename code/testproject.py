import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import experiment1 as e1
import experiment2 as e2

#random seed with userID
np.random.seed(904080188)

def author():
    # gatech username
    return "ssubedi33"


def study_group():
    # No study group
    return "ssubedi33"

def plots():
    #Inputs
    sym = "JPM"
    svm = 100000
    com = 9.95
    imp = 0.005
    in_date = [dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31)]
    out_date = [dt.datetime(2010, 1, 1), dt.datetime(2011, 12, 31)]

    #run experiment 1, this plots figures for experiment 1 and outputs benchmark portfolio and manual strategy portfolio to plot
    bench_port_in, bench_port_out, portfolio_in, portfolio_out, buy_in, sell_in, buy_out, sell_out, port_in_1, port_out_1 = e1.experiment_1(sym, in_date, out_date, svm, com, imp)

    port_in_1_norm = port_in_1/port_in_1.iloc[0]
    port_out_1_norm = port_out_1/port_out_1.iloc[0]
    #run experiment 2
    e2.experiment_2(sym, in_date, svm, 0, [0.0, 0.01, 0.02])
    #plot Manual strategy - in sample
    plt.figure()
    portfolio_in_norm = portfolio_in/portfolio_in.iloc[0]
    bench_port_in_norm = bench_port_in/bench_port_in.iloc[0]
    plt.plot(portfolio_in_norm, label="Manual Strategy", color = "red")
    plt.plot(bench_port_in_norm, label="Benchmark", color = "purple")
    # Add vertical lines for buy and sell dates
    for date in buy_in:
        plt.axvline(x=date , color='blue', linestyle = '--', linewidth=1)
    plt.axvline(x=date, label = "Long Entry" ,linestyle = '--', color='blue', linewidth=1)
    for date in sell_in:
        plt.axvline(x=date, color='black', linestyle = '--', linewidth=1)
    plt.axvline(x=date, label = "Short Entry" ,linestyle = '--', color='black', linewidth=1)
    plt.legend( loc='upper left')
    plt.title("Benchmark Vs Manual Strategy for JPM (In-sample)")
    plt.xlabel("Date (YYYY-MM-DD)")
    plt.ylabel('Normalized Price')
    plt.xticks(pd.date_range('2008-1-1', '2010-1-1', freq='2MS'), rotation=60)
    plt.tight_layout()
    plt.savefig("./images/figure_1.png")
    plt.close()

    #plot Manual Strategy Plot - out sample
    plt.figure()
    portfolio_out_norm = portfolio_out/portfolio_out.iloc[0]
    bench_port_out_norm = bench_port_out/bench_port_out.iloc[0]
    plt.plot(portfolio_out_norm, label="Manual Strategy", color = "red")
    plt.plot( bench_port_out_norm, label="Benchmark", color = "purple")
    for date in buy_out:
        plt.axvline(x=date, color='blue',  linestyle = '--',linewidth=1)
    plt.axvline(x=date, label = "Long Entry" ,linestyle = '--', color='blue', linewidth=1)
    for date in sell_out:
        plt.axvline(x=date, color='black',  linestyle = '--', linewidth=1)
    plt.axvline(x=date, label = "Short Entry" ,linestyle = '--', color='black', linewidth=1)
    plt.legend( loc='upper left')
    plt.title("Benchmark Vs Manual Strategy for JPM (Out-sample)")
    plt.xlabel("Date (YYYY-MM-DD)")
    plt.ylabel('Normalized Price')
    plt.xticks(pd.date_range('2010-1-1', '2012-1-1', freq='2MS'), rotation=60)
    plt.tight_layout()
    plt.savefig("./images/figure_2.png")
    plt.close()

    #plot statistics
    # Metrics
    port_in_dr = (portfolio_in_norm / portfolio_in_norm.shift(1)) - 1
    port_in_dr = port_in_dr[1:]
    port_in_dr_mean = round(port_in_dr.mean(), 6)
    print("Average Daily Return of Manual Strategy (in-sample): ", port_in_dr_mean)
    std_port_in = round(port_in_dr.std(), 6)
    print("Average STD of Manual Strategy (in-sample): ", std_port_in)
    cr_port_in = round((portfolio_in[-1] / portfolio_in[0]) - 1, 6)
    print("Average CR of Manual Strategy (in-sample): ", cr_port_in)
    sharpe_ratio_in = -1*np.sqrt(252)*(port_in_dr_mean/std_port_in)

    port_out_dr = (portfolio_out_norm / portfolio_out_norm.shift(1)) - 1
    port_out_dr = port_out_dr[1:]
    port_out_dr_mean = round(port_out_dr.mean(), 6)
    std_port_out = round(port_out_dr.std(), 6)
    cr_port_out = round((portfolio_out[-1] / portfolio_out[0]) - 1, 6)
    sharpe_ratio_out = -1 * np.sqrt(252) * (port_out_dr_mean / std_port_out)

    print("Average Daily Return of Manual Strategy (out-sample): ", port_out_dr_mean)
    print("Average STD of Manual Strategy (out-sample): ", std_port_out)
    print("Average CR of Manual Strategy (out-sample): ", cr_port_out)

    #strategy learner
    # Metrics
    port_in_dr_1 = (port_in_1_norm / port_in_1_norm.shift(1)) - 1
    port_in_dr_1 = port_in_dr_1[1:]
    port_in_dr_mean_1 = round(port_in_dr_1.mean(), 6)
    std_port_in_1 = round(port_in_dr_1.std(), 6)
    cr_port_in_1 = round((port_in_1[-1] / port_in_1[0]) - 1, 6)
    sharpe_ratio_in_ = -1 * np.sqrt(252) * (port_in_dr_mean_1 / std_port_in_1)

    port_out_dr_1 = (port_out_1_norm / port_out_1_norm.shift(1)) - 1
    port_out_dr_1 = port_out_dr_1[1:]
    port_out_dr_mean_1 = round(port_out_dr_1.mean(), 6)
    std_port_out_1 = round(port_out_dr_1.std(), 6)
    cr_port_out_1 = round((port_out_1[-1] / port_out_1[0]) - 1, 6)
    sharpe_ratio_out_ = -1 * np.sqrt(252) * (port_out_dr_mean_1 / std_port_out_1)

    bench_in_dr = (bench_port_in_norm / bench_port_in_norm.shift(1)) - 1
    bench_in_dr = bench_in_dr[1:]
    bench_in_dr_mean = round(bench_in_dr.mean(), 6)
    std_bench_in = round(bench_in_dr.std(), 6)
    cr_bench_in = round((bench_port_in[-1] / bench_port_in[0]) - 1, 6)
    sharpe_ratio_in_1 = -1 * np.sqrt(252) * (bench_in_dr_mean / std_bench_in)

    print("Average Daily Return of Benchmark (in-sample): ", bench_in_dr_mean)
    print("Average STD of Benchmark (in-sample): ", std_bench_in)
    print("Average CR of Benchmark (in-sample): ", cr_bench_in)


    bench_out_dr = (bench_port_out_norm / bench_port_out_norm.shift(1)) - 1
    bench_out_dr = bench_out_dr[1:]
    bench_out_dr_mean = round(bench_out_dr.mean(), 6)
    std_bench_out = round(bench_out_dr.std(), 6)
    cr_bench_out = round((bench_port_out[-1] / bench_port_out[0]) - 1, 6)
    sharpe_ratio_out_1 = -1 * np.sqrt(252) * (bench_out_dr_mean / std_bench_out)

    print("Average Daily Return of Benchmark (out-sample): ", bench_out_dr_mean)
    print("Average STD of Benchmark (out-sample): ", std_bench_out)
    print("Average CR of Benchmark (out-sample): ", cr_bench_out)


    benchmark_metrics = {
        'Daily Return': [bench_in_dr_mean, bench_out_dr_mean],
        'Cumulative Return': [cr_bench_in, cr_bench_out],
    }

    manual_strategy_metrics = {
        'Daily Return': [port_in_dr_mean, port_out_dr_mean],
        'Cumulative Return': [cr_port_in, cr_port_out],
    }

    learner_strategy_metrics = {
        'Daily Return': [port_in_dr_mean_1, port_out_dr_mean_1],
        'Cumulative Return': [cr_port_in_1, cr_port_out_1],
    }

    metrics = ['Daily Return', 'Cumulative Return']
    time_periods = ['In-Sample', 'Out-of-Sample']

    # Convert to DataFrames
    benchmark_df = pd.DataFrame(benchmark_metrics, index=time_periods)
    manual_df = pd.DataFrame(manual_strategy_metrics, index=time_periods)
    learner_df = pd.DataFrame(learner_strategy_metrics, index=time_periods)

    # Bar plot
    bar_width = 0.25
    x = np.arange(len(time_periods))

    # Create subplots
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))

    for i, metric in enumerate(metrics):
        ax = axs[i]
        ax.bar(x - bar_width, benchmark_df[metric], bar_width, label='Benchmark', color='gray')
        ax.bar(x, manual_df[metric], bar_width, label='Manual Strategy', color='blue')
        ax.bar(x + bar_width, learner_df[metric], bar_width, label='Strategy Learner', color='green')

        ax.set_title(metric)
        ax.set_xticks(x)
        ax.set_xticklabels(time_periods)
        ax.set_ylabel(metric)
        ax.legend()


    fig.suptitle('Performance Comparison: Benchmark vs Manual Strategy vs Strategy Learner', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    plt.savefig("./images/figure_7.png")
    plt.close()

if __name__ == '__main__':
    plots()
