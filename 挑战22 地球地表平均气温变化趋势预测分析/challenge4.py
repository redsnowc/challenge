import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression as lr
from sklearn.metrics import mean_absolute_error


def Temperature():

    # 获取数据
    tmp = pd.read_csv('GlobalSurfaceTemperature.csv', header=0)
    tmp = tmp.set_index(pd.to_datetime([str(i) for i in tmp.Year]))
    ghg = pd.read_csv('GreenhouseGas.csv', header=0)
    ghg = ghg.set_index(pd.to_datetime([str(i) for i in ghg.Year]))
    co2 = pd.read_csv('CO2ppm.csv', header=0)
    co2 = co2.set_index(pd.to_datetime([str(i) for i in co2.Year]))

    data = pd.concat([ghg, co2, tmp], axis=1)
    data.drop(['Year'], axis=1, inplace=True)
    data = data.fillna(
        method='ffill', axis=0).fillna(method='bfill', axis=0)

    # 分割数据集和目标
    x = data['1970': '2010'].iloc[:, :4]
    x_test = data['2011': '2017'].iloc[:, :4]
    y_upper = data['1970': '2010'].Upper
    y_median = data['1970': '2010'].Median
    y_lower = data['1970': '2010'].Lower

    # 获取验证用数据
    upper_true = data['2005': '2010'].Upper
    x_true = data['2005': '2010'].iloc[:, :4]

    # 建立并训练模型
    model_upper = lr()
    model_median = lr()
    model_lower = lr()
    model_upper.fit(x, y_upper)
    model_median.fit(x, y_median)
    model_lower.fit(x, y_lower)

    # 测试模型精度
    upper_pred = model_upper.predict(x_true)
    print(mean_absolute_error(upper_true, upper_pred))

    # 预测气温
    UpperPredict = model_upper.predict(x_test)
    MedianPredict = model_median.predict(x_test)
    LowerPredict = model_lower.predict(x_test)

    np.set_printoptions(precision=3)
    return UpperPredict, MedianPredict, LowerPredict

if __name__ == '__main__':
    print(Temperature())
