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
    ghg_temp = temp1.join(ghg)
    #ghg_temp = pd.concat([temp1, ghg], axis=1)
    temp2 = temp.resample('Q').mean()

    with plt.style.context('Solarize_Light2'):
        fig = plt.figure()
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.set_xlabel('Years')
        ax1.set_ylabel('Values')
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.set_xlabel('Years')
        ax2.set_ylabel('Values')
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.set_xlabel('Quarters')
        ax3.set_ylabel('Temperature')
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.set_xlabel('Values')
        ax4.set_ylabel('Values')
        ghg_temp.plot(ax=ax1)
        ghg_temp.plot.bar(ax=ax2)
        temp2.plot.area(ax=ax3)
        temp2.plot.kde(ax=ax4)
        plt.show()
    return fig


if __name__ == '__main__':
    climate_plot()
