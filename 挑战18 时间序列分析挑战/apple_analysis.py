import pandas as pd


def quarter_volume():
    data = pd.read_csv("apple.csv")
    '''
    # 教练写法
    haha = pd.Series(list(data.Volume), index=pd.to_datetime(data.Date))
    return haha.resample('q').sum().sort_values()[-2]
    '''
    data['Date'] = pd.to_datetime(data['Date'])
    volume_d = data[['Date', 'Volume']].set_index('Date')
    volume_q = volume_d.resample('Q').sum().sort_values(
        'Volume', ascending=False)
    second_volume = volume_q.Volume[1]
    return second_volume


if __name__ == '__main__':
    print(quarter_volume())
