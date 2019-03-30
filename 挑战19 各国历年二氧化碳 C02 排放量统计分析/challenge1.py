import pandas as pd


def group_sum(co2e, i):
    return co2e[co2e[
        'Income group'] == i].drop('Income group', axis=1).sum().sum()


def country_sum(co2e, i):
    x = co2e[co2e['Income group'] == i].drop('Income group', axis=1)
    x['sum'] = x.sum(axis=1)
    x_sorted = x.sort_values('sum')
    return [x_sorted.index[-1], x_sorted.max().iloc[-1],
            x_sorted.index[0], x_sorted.min().iloc[-1]]


def co2():
    data = pd.read_excel('ClimateChange.xlsx')
    country = pd.read_excel('ClimateChange.xlsx', 'Country')
    co2e = data[data['Series code'] == 'EN.ATM.CO2E.KT']
    co2e.index = co2e['Country name']
    co2e = co2e.iloc[:, 6:].replace('..', pd.np.nan)
    co2e = co2e.fillna(
        method='ffill', axis=1).fillna(method='bfill', axis=1)
    ig = country[['Country name', 'Income group']].set_index(
        country['Country name']).drop('Country name', axis=1)
    co2e = co2e.join(ig)
    co2e.dropna(thresh=2, inplace=True)
    hio = country_sum(co2e, 'High income: OECD')
    hino = country_sum(co2e, 'High income: nonOECD')
    li = country_sum(co2e, 'Low income')
    lmi = country_sum(co2e, 'Lower middle income')
    umi = country_sum(co2e, 'Upper middle income')
    results = pd.DataFrame({
        'Sum emissions': [
            group_sum(co2e, 'High income: OECD'),
            group_sum(co2e, 'High income: nonOECD'),
            group_sum(co2e, 'Low income'),
            group_sum(co2e, 'Lower middle income'),
            group_sum(co2e, 'Upper middle income')
        ],
        'Highest emission country': [
            hio[0], hino[0], li[0], lmi[0], umi[0]],
        'Highest emissions': [hio[1], hino[1], li[1], lmi[1], umi[1]],
        'Lowest emission country': [
            hio[2], hino[2], li[2], lmi[2], umi[2]],
        'Lowest emissions': [hio[3], hino[3], li[3], lmi[3], umi[3]]},
        index=[
            'High income: OECD', 'High income: nonOECD', 'Low income',
            'Lower middle income', 'Upper middle income'],
        columns=[
            'Sum emissions', 'Highest emission country',
            'Highest emissions', 'Lowest emission country',
            'Lowest emissions'])
    results.index.name = 'Income group'
    return results


if __name__ == '__main__':
    print(co2())
