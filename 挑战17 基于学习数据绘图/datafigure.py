import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def data_plot():
    user_info = pd.read_json("user_study.json")
    user_study_time = user_info[['user_id', 'minutes']].groupby('user_id').sum()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    user_study_time.plot(ax=ax)
    ax.set_xlabel('User ID')
    ax.set_ylabel('Study Time')
    plt.show()

    return ax

if __name__ == '__main__':
    data_plot()
