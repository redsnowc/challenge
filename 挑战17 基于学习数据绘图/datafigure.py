import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


user_info = pd.read_json("user_study.json")
user_study_time = user_info[['user_id', 'minutes']].groupby('user_id').sum()
plt.plot(user_study_time)
plt.title('StudyData')
plt.xticks(np.arange(0, 200001, 50000))
plt.xlabel('User ID')
plt.ylabel('Study Time')
plt.show()
