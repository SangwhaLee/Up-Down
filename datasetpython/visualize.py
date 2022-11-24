#%%

import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

file_path = './prototype.json'
with open(file_path,'r', encoding='UTF-8') as file:
    datas = json.load(file)

popular = sorted(list(map(lambda x: int(datas[x]['popularity']), range(len(datas)))))

popr = pd.Series(popular)

print()

index = len(popular)
plt.boxplot(popular)

print(popr.quantile(.2),popr.quantile(.66),popr.quantile(.8))

plt.show()

# %%
