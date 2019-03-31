import pandas as pd


def country_sum(co2, i):
    x = co2[co2['Income group'] == i].sum(1).sort_values()
    return [x.index[-1], x.max(), x.index[0], x.min()]


def co2():
    data = pd.read_excel('ClimateChange.xlsx')
    country = pd.read_excel('ClimateChange.xlsx', 'Country')
    co2 = data[data['Series code'] == 'EN.ATM.CO2E.KT'].iloc[:, 6:].replace(
        '..', pd.np.nan).set_index(country['Country name'])
    co2 = co2.fillna(
        method='ffill', axis=1).fillna(method='bfill', axis=1)
    ig = country[['Country name', 'Income group']].set_index(
        country['Country name']).drop('Country name', axis=1)
    co2 = co2.join(ig)
    co2.dropna(thresh=2, inplace=True)
    index = ['High income: OECD', 'High income: nonOECD', 'Low income',
            'Lower middle income', 'Upper middle income']
    hio = country_sum(co2, index[0])
    hino = country_sum(co2, index[1])
    li = country_sum(co2, index[2])
    lmi = country_sum(co2, index[3])
    umi = country_sum(co2, index[4])
    results = pd.DataFrame(index=index, data={
        'Sum emissions': [
            co2[co2['Income group'] == index[0]].sum(1).sum(),
            co2[co2['Income group'] == index[1]].sum(1).sum(),
            co2[co2['Income group'] == index[2]].sum(1).sum(),
            co2[co2['Income group'] == index[3]].sum(1).sum(),
            co2[co2['Income group'] == index[4]].sum(1).sum()],
        'Highest emission country': [hio[0], hino[0], li[0], lmi[0], umi[0]],
        'Highest emissions': [hio[1], hino[1], li[1], lmi[1], umi[1]],
        'Lowest emission country': [hio[2], hino[2], li[2], lmi[2], umi[2]],
        'Lowest emissions': [hio[3], hino[3], li[3], lmi[3], umi[3]]},)
    results.index.name = 'Income group'
    return results


if __name__ == '__main__':
    print(co2())
