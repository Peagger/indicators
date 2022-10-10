import pandas as pd
import numpy as np
def get_avgminroute(file):
    df = pd.read_csv(file,header = 0)
    df.dropna(inplace = True)
    mylist = []
    for i in range(2,20,2):
        # row=df[(df[0]==str(num))&(df[1]=="+"+str(time)+"s")& (df[5]=="1")].shape[0]
        mylist.append(df[df[1]=="+"+str(i)+"s"])
    listmartix = []
    for j in range(len(mylist)):
        martixmap = np.zeros([20,20],dtype = int)
        for i in range(len(mylist[j])): 
            prenode = int(mylist[j].iloc[i][0][5:])
            desnode = int(mylist[j].iloc[i][2][7:])-1
            distance = int(mylist[j].iloc[i][5])
            print(prenode,desnode,distance)
            martixmap[prenode,desnode] = distance
            martixmap[desnode,prenode] = distance
        listmartix.append(martixmap)
    avgminroute = []
    for i in range(len(listmartix)):
        sum = np.sum(listmartix[i].reshape(-1))
        avg = sum/(25*24)
        avgminroute.append(avg.item())
    #avgminroute.insert(0,0)   
    return avgminroute
avgminroute=get_avgminroute('routes4.csv')
print(avgminroute)
