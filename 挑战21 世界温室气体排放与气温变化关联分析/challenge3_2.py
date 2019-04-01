import pandas as pd
import matplotlib.pyplot as plt


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
    #ghg_temp = temp1.join(ghg)
    ghg_temp = pd.concat([temp1, ghg], axis=1)
    temp2 = temp.resample('Q').mean()

    with plt.style.context('Solarize_Light2'):
        fig = plt.figure(figsize=(16, 10))
        ax1 = fig.add_subplot(2, 2, 1)
        ghg_temp.plot(ax=ax1, marker='*', linewidth=2, alpha=0.8)
        ax1.set_xlabel('Years')
        ax1.set_ylabel('Values')
        plt.legend(loc='lower right')
        ax2 = fig.add_subplot(2, 2, 2)
        ghg_temp.plot.bar(ax=ax2, width=0.6, alpha=0.8)
        ax2.set_xlabel('Years')
        ax2.set_ylabel('Values')
        ax3 = fig.add_subplot(2, 2, 3)
        temp2.plot.area(ax=ax3, alpha=0.8)
        ax3.set_xlabel('Quarters')
        ax3.set_ylabel('Temperature')
        ax4 = fig.add_subplot(2, 2, 4)
        temp2.plot.kde(ax=ax4, alpha=0.8)
        ax4.set_xlabel('Values')
        ax4.set_ylabel('Values')
        plt.show()
    return fig


if __name__ == '__main__':
    climate_plot()
