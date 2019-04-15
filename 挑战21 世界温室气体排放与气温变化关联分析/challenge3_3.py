import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def climate_plot():
    data1 = pd.read_excel('ClimateChange.xlsx')
    data2 = pd.read_excel('GlobalTemperature.xlsx')
    i = [
        'EN.ATM.CO2E.KT', 'EN.ATM.METH.KT.CE',
        'EN.ATM.NOXE.KT.CE', 'EN.ATM.GHGO.KT.CE', 'EN.CLC.GHGR.MT.CE']
    ghg = data1[data1['Series code'].isin(
        i)].iloc[:, 6: -1].replace('..', pd.np.nan)
    ghg = ghg.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    ghg = pd.DataFrame(ghg.sum().values, index=pd.period_range(
        '1990', '2010', freq='A'), columns=['Total GHG'])
    ghg = (ghg - ghg.min()) / (ghg.max() - ghg.min())
    temp = data2[['Land Average Temperature',
                  'Land And Ocean Average Temperature']].set_index(
        pd.to_datetime(data2['Date']))
    temp1 = temp['1990': '2010'].resample('A').mean().set_index(ghg.index)
    temp1 = (temp1 - temp1.min()) / (temp1.max() - temp1.min())
    # 实验楼挑战检测环境的 pandas 0.20.1 版本不支持注释写法，只能降级或者升级 pandas 版本
    # 可能是因为索引导致的，如果索引为时间序列就会出现，重设索引则正常，可能是版本BUG
    #ghg_temp = temp1.join(ghg)
    ghg_temp = pd.concat([temp1, ghg], axis=1)
    ghg_temp.set_index(pd.Series([str(i)
                                  for i in range(1990, 2011)]), inplace=True)
    temp2 = temp.resample('Q').mean()

    sns.set()
    fig = plt.figure(figsize=(16, 10))
    ax1 = fig.add_subplot(2, 2, 1)
    ghg_temp.plot(ax=ax1)
    ax1.set_xlabel('Years')
    ax1.set_ylabel('Values')
    labels = ['1990', '1992', '1995', '1997',
             '2000', '2002', '2005', '2007', '2010']
    ticks = [0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20]
    ax1.set_xticks(ticks)
    ax1.set_xticklabels(labels)
    plt.legend(loc='lower right')
    ax2 = fig.add_subplot(2, 2, 2)
    ghg_temp.plot.bar(ax=ax2)
    ax2.set_xlabel('Years')
    ax2.set_ylabel('Values')
    ax3 = fig.add_subplot(2, 2, 3)
    temp2.plot.area(ax=ax3)
    ax3.set_xlabel('Quarters')
    ax3.set_ylabel('Temperature')
    ax4 = fig.add_subplot(2, 2, 4)
    temp2.plot.kde(ax=ax4)
    ax4.set_xlabel('Values')
    ax4.set_ylabel('Values')
    plt.show()
    return fig


if __name__ == '__main__':
    climate_plot()
