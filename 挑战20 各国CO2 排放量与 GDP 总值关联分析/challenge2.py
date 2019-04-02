import pandas as pd
import matplotlib.pyplot as plt


def get_value(data, code, name):
    df = data[data['Series code'] == code].set_index(
        'Country code').replace('..', pd.np.nan)
    df = df.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    df = pd.DataFrame(df.sum(axis=1), index=df.index, columns=[name])
    df = (df - df.min()) / (df.max() - df.min())
    return df


def co2_gdp_plot():
    data = pd.read_excel('ClimateChange.xlsx')
    co2_gdp = get_value(data, 'EN.ATM.CO2E.KT', 'CO2 SUM').join(
        get_value(data, 'NY.GDP.MKTP.CD', 'GDP SUM'))
    fig = plt.subplot()
    co2_gdp.plot(ax=fig)
    labels = ['CHN', 'FRA', 'GBR', 'RUS', 'USA']
    ticks = [list(co2_gdp.index).index(i) for i in labels]
    plt.xticks(ticks, labels, rotation='vertical')
    plt.title('GDP-CO2')
    plt.xlabel('Countries')
    plt.ylabel('Values')
    plt.show()

    china = [float(format(i, '.3f')) for i in list(co2_gdp.loc['CHN'])]
    return fig, china


if __name__ == '__main__':
    co2_gdp_plot()
