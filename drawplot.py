from cmath import nan
from tkinter import N, image_names
from cv2 import threshold
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

from pyparsing import col

threshold=20

path="csv\\"
names=['normal01.csv','normal03.csv','normal04.csv','normal05.csv','cancer01.csv','cancer02.csv','normal06.csv']
#不能把不同图数据放在一个df里，这样会导致细胞数和第一个对齐
df2=pd.DataFrame()
for i,name in enumerate(names):
    df=pd.read_csv(path+name)
    name=os.path.splitext(name)[0]
    df2[name]=df['mean_gray']
df3=pd.DataFrame(columns=df2.columns,index=['>20','<=20'])
for column in df3.columns:
    n1=0
    n2=0
    for i in df2.index:
        if np.isnan(df2[column][i]):
            print('nan')
            continue
        if df2[column][i]>20:
            n1+=1
        else :
            n2+=1
    df3[column]['>20']=n1
    df3[column]['<=20']=n2  
df2.plot.box()
df3.T.plot.bar()
plt.show()
   
