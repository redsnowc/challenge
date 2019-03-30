from sys import argv
import pandas as pd


def analysis(file, user_id):
    user_info = pd.read_json(file)
    times = user_info[user_info['user_id'] == user_id]['user_id'].count()
    minutes = user_info[user_info['user_id'] == user_id]['minutes'].sum()

    return times, minutes


if __name__ == '__main__':
    file = "user_study.json"
    user_id = int(argv[1])
    print(analysis(file, user_id))
