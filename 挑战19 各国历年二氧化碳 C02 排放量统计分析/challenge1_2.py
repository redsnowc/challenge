import pandas as pd


def df(co2, i, name1, name2):
    df = co2.sort_values(by='Sum emissions', ascending=i)
    df = df.groupby('Income group').head(1).set_index('Income group')
    return df.rename(columns={'Country name': name1, 'Sum emissions': name2})


def co2():
    excel = 'ClimateChange.xlsx'
    data1 = pd.read_excel(excel).set_index('Country code')
    data2 = pd.read_excel(excel,
                          'Country').set_index('Country code')
    df1 = data1[data1['Series code'] == 'EN.ATM.CO2E.KT'].iloc[:, 6:]
    df1.replace({'..': pd.np.nan}, inplace=True)
    df1 = df1.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    df1 = pd.DataFrame(df1.groupby('Country code', sort=False).sum(
        axis=1).sum(axis=1), columns=['Sum emissions'])
    df2 = data2[['Country name', 'Income group']]
    co2 = df2.join(df1)
    co2.replace({0: pd.np.nan}, inplace=True)
    co2 = co2.dropna(thresh=3)
    ig_sum = co2.groupby('Income group').sum()
    high = df(co2, False, 'Highest emission country', 'Highest emissions')
    low = df(co2, True, 'Lowest emission country', 'Lowest emissions')

    return pd.concat([ig_sum, high, low], axis=1)


if __name__ == "__main__":
    print(co2())