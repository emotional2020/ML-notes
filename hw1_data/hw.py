import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt


train_data = pd.read_csv('train.csv', encoding='big5')

data = train_data.iloc[:, 3:]
data[data == 'NR'] = 0

data = pd.DataFrame(data)
new_data = data.iloc[:18, :]

### 拼接所有日期的18项测试数据
for i in range(239):
    i = i + 1
    add_data = data.iloc[18 * i:18 + 18 * i, :].reset_index(drop=True)
    new_data = pd.concat([new_data, add_data], axis=1, ignore_index=True)

# 拼接240天，24小时的pm2.5数据（每行为一天，每列为一小时）
pm25 = new_data.iloc[[9], :].reset_index(drop=True)   #取出pm2.5
pm25_every_day = pm25.iloc[[0], 0:24]
for i in range(239):
    i = i+1
    add_data2 = pm25.iloc[[0], 24*i:24*(i+1)].T.reset_index(drop=True).T
    pm25_every_day =pm25_every_day.append(add_data2)

pm25_every_day.index = range(len(pm25_every_day))
pm25_every_day.iloc[:,:] = pm25_every_day.iloc[:,:].astype(int)
# print(pm25_every_day)

##### 归一化
# df = pm25_every_day
# df.iloc[:,:] = df.iloc[:,:].astype(int)
# df_norm2=df.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))

#取前200天的数据作为训练集
x_data = pm25_every_day.iloc[0:200,0:9]
y_data = pm25_every_day.iloc[0:200,[9]]

#取后200天的数据作为测试集
x_test = pm25_every_day.iloc[200:,0:9]
y_test = pm25_every_day.iloc[200:,[9]]

rfc = DecisionTreeRegressor(random_state=20, max_depth=3) #实例化
rfc = rfc.fit(x_data, y_data)
predict = rfc.predict(x_test)
score_te = rfc.score(x_test, y_test)
cross_score = cross_val_score(rfc, x_data, y_data, cv=10, scoring = "neg_mean_squared_error").mean()
print(score_te)
print(cross_score)

plt.figure()
plt.plot(range(40),np.array(predict))
plt.plot(range(40),np.array(y_test))
plt.show()





