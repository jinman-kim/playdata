import pickle
import pandas as pd
import numpy as np

with open('./kbo_player.pkl', 'rb') as f:
    data = pickle.load(f)
pd.set_option('display.max_rows',None)
kbo = pd.DataFrame(data)
kbo.loc[kbo.연봉.apply(lambda x: len(x) == 0), '연봉'] = np.nan
# kbo.loc[kbo['연봉'].apply(lambda x: len(x) == 0), '연봉'] = np.nan
a = kbo['연봉'].isna().sum()
usd = 1300
kbo2 = kbo.loc[kbo.연봉.notnull()].copy()
# kbo2.loc[kbo2.연봉.apply(lambda x : x[-2:] == '달러')].연봉.apply(lambda x: int(x[:-2])*usd)
kbo2.loc[kbo2.연봉.apply(lambda x : x[-2:] == '달러'), '원화']=kbo2.loc[kbo2.연봉.apply(lambda x : x[-2:] == '달러')].연봉.apply(lambda x: int(x[:-2])*usd//10000)
kbo2.loc[kbo2.원화.isnull(),'원화'] =  kbo2.loc[kbo2.원화.isnull()].연봉.apply(lambda x : x[:-2])
kbo2.원화 = kbo2.원화.astype(int)
print(kbo2.shape)
# for i in kbo2.원화:
#     print(i)
# print('{:,}'.format(kbo2.원화.sum()))
kbo2.loc[kbo2.Team=='고양 히어로즈','Team'] = '키움 히어로즈'
# print(kbo2.Team.value_counts())
a = kbo2.groupby(kbo2.Team).원화.agg(['mean','median','std','count'])
kt_sort = kbo2[kbo2.Team=='KT 위즈'].sort_values('원화',)

print(kt_sort[::-1])
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(5, 6))
ax = fig.add_subplot(111)
ax.boxplot(kbo2[kbo2.Team == "한화 이글스"]['원화'], labels=['salary'])

plt.show()
# print(kbo2.연봉)
# print(kbo['연봉'])