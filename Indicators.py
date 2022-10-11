
import pandas as pd
import numpy as np
import networkx as nx
import networkx.algorithms.components as com
import matplotlib.pyplot as plt
import math
class Indicators():
    def __init__(self,csvpath='routes4.csv',nums=20,times=100,interval=1,start=3,end=100,kconnect=[2,3,20]):
        self.df = pd.read_csv(csvpath,header=None)
        self.nums=nums              #节点数
        self.times=times            #时间长度
        self.interval=interval      #时间间隔
        self.count=0
        self.accesslist=[]  
        self.start=start            #路由表开始时间
        self.end=end                #路由表结束时间
        self.kconnect=kconnect        
        self.avg_node_degree=[]     #平均节点度  
        self.avg_min_route=[]       #平均最短路
        self.kconnectivity=[]       #k连通度
        self.avg_concen_degree=[]   #平均聚集系数
        self.con_coet=[]        #连通系数
        pass

    def printNodeDegree(self,time1):
        '''打印 节点度''''''打印所有节点的平均节点度'''
        arr=[]
        df=self.df
        nums=self.nums
        times=self.times
        interval=self.interval
        for num in range(0,nums):
            for time in range(interval,times,interval):
                row=df[(df[0]==str(num))&(df[1]=="+"+str(time)+"s")& (df[5]=="1")].shape[0]
                arr.append([num,time,row])
        df2=pd.DataFrame(arr)
        df2.rename(columns={0:"Node",1:"Time",2:"Degree"})
        for index,row in df2[(df2[1]==time1)].iterrows():
            print("节点"+str(row[0])+"在time:+"+str(row[1])+"s的节点度为"+str(row[2]))
    def printAvegminRoute(self):
        '''todo打印 平均最短路'''
        mylist = []
        df=self.df
        for i in range(3,101,1):
            # row=df[(df[0]==str(num))&(df[1]=="+"+str(time)+"s")& (df[5]=="1")].shape[0]
            mylist.append(df[df[1]=="+"+str(i)+"s"])
        mylist
        listmartix = []
        for j in range(len(mylist)):
            martixmap = np.zeros([20,20],dtype = int)
            for i in range(len(mylist[j])): 
                prenode = int(mylist[j].iloc[i][0])
                desnode = int(mylist[j].iloc[i][2][7:])-1
                distance = int(mylist[j].iloc[i][5])
                # print(prenode,desnode,distance)
                martixmap[prenode,desnode] = distance
                martixmap[desnode,prenode] = distance
            listmartix.append(martixmap)
        avgminroute = []
        for i in range(len(listmartix)):
            sum = np.sum(listmartix[i].reshape(-1))
            avg = sum/(20*19)
            avgminroute.append(avg.item())
        for i in avgminroute:
            print('{:.2f}'.format(i))
    def coutConnetion(self,nums,kconnect,a:list,index,time):
        '''计算time时刻k连通的个数'''
        if kconnect==0:
            flag=1
            for i in range(0,len(a)):
                for j in range(0,len(a)):
                    if (i<j and self.Accesslist[time][a[i]][a[j]]==0):
                        return
            self.count+=flag
        else:
            for i in range(nums,kconnect-1,-1):
                a[index]=i-1
                self.coutConnetion(i-1,kconnect-1,a,index+1,time)  
    def printKConnectivity(self,kconnect):
        df=self.df;nums=self.nums;name_dict={};times=self.times;interval=self.interval
        dp=[]#分时间写入列表
        Accesslist=[]#各个时间段的可达矩阵列表
        for i in range(nums):
            name_dict['10.1.0.'+str(i+1)]=str(i)
        for i in range(interval,times,interval):
            dp.append(df[df[1]=="+{}s".format(str(i))])
        for i in range(len(dp)):
            AccessMatrix=[[0 for col in range(nums)] for row in range(nums)]
            for row in dp[i].itertuples():#读入邻接矩阵
                i=int(row[1])
                j=int(name_dict[row[4]])
                AccessMatrix[i][j]=1
            for k in range(nums):#warshall算法求传递闭包
                for i in range(nums):
                    for j in range(nums):
                        if AccessMatrix[i][j]==1:
                            AccessMatrix[i][j]=1
                        else:
                            AccessMatrix[i][j]=AccessMatrix[i][k]*AccessMatrix[k][j]
            Accesslist.append(AccessMatrix)
        self.Accesslist=Accesslist
        for i in range(0,49):#第2i秒
            for k in [2,kconnect,nums]:#2连通，k连通，全连通
                self.count=0
                a=[0 for col in range(k)]
                self.coutConnetion(nums,k,a,0,i)
                print('第+{}s:{}连通率:{:.4f}%'.format((i+1)*2,k,self.rate(self.count,nums,k)*100))
    def countConnectivity(self,nums,kconnect,a:list,index,time):
        '''计算time时刻k连通的个数'''
        if kconnect==0:
            flag=1
            for i in range(0,len(a)):
                for j in range(0,len(a)):
                    # print(i,j,time)
                    if (i<j and self.accesslist[time][a[i]][a[j]]==0):
                        return
            self.count+=flag
        else:
            for i in range(nums,kconnect-1,-1):
                a[index]=i-1
                self.countConnectivity(i-1,kconnect-1,a,index+1,time)  
    def rate(self,nums,k):
        '''个数除以总数得到比率'''
        total=(math.factorial(nums)//(math.factorial(k)*math.factorial(nums-k)))
        return self.count/total
    
    def genAvgNodeDegree(self):
        '''生成全时段的平均节点度'''
        arr=[];df=self.df
        for num in range(0,self.nums):
            for time in range(self.start,self.end+1,self.interval):
                row=df[(df[0]==str(num))&(df[1]=="+"+str(time)+"s")& (df[5]=="1")].shape[0]
                arr.append([num,time,row])
        df2=pd.DataFrame(arr)
        df2.rename(columns={0:"Node",1:"Time",2:"Degree"})
        total=0;avg_list=[]
        for time in range(self.start,self.end+1,self.interval):
            for index,row in df2[(df2[1]==time)].iterrows():
                total+=row[2]
            avg_list.append(total/self.nums)
            total=0
        #print(avg_list)
        self.avg_node_degree=avg_list
    def genAvgMinRoute(self):
        mylist=[];df=self.df;listmartix=[];avgminroute = []
        for i in range(self.start,self.end+1,self.interval):
            mylist.append(df[df[1]=="+"+str(i)+"s"])
        for j in range(len(mylist)):
            martixmap = np.zeros([self.nums,self.nums],dtype = int)
            for i in range(len(mylist[j])): 
                prenode = int(mylist[j].iloc[i][0])
                desnode = int(mylist[j].iloc[i][2][7:])-1
                distance = int(mylist[j].iloc[i][5])
                # print(prenode,desnode,distance)
                martixmap[prenode,desnode] = distance
                martixmap[desnode,prenode] = distance
            listmartix.append(martixmap)
        for i in range(len(listmartix)):
            sum = np.sum(listmartix[i].reshape(-1))
            avg = sum/(self.nums*(self.nums-1))
            avgminroute.append(avg.item())
        self.avg_min_route=avgminroute
    def genKConnectivity(self):
        df=self.df;name_dict={};dp=[]
        for i in range(self.nums):
            name_dict['10.1.0.'+str(i+1)]=str(i)
        for i in range(self.start,self.end+1,self.interval):
            dp.append(df[df[1]=="+{}s".format(str(i))])
        for i in range(len(dp)):
            AccessMatrix=[[0 for col in range(self.nums)] for row in range(self.nums)]
            for row in dp[i].itertuples():#读入邻接矩阵
                i=int(row[1])
                j=int(row[4][7:])
                AccessMatrix[i][j]=1
            for k in range(self.nums):#warshall算法求传递闭包
                for i in range(self.nums):
                    for j in range(self.nums):
                        if AccessMatrix[i][j]==1:
                            AccessMatrix[i][j]=1
                        else:
                            AccessMatrix[i][j]=AccessMatrix[i][k]*AccessMatrix[k][j]
            self.accesslist.append(AccessMatrix)
        for k in self.kconnect:#2连通，k连通，全连通
            kconnectivity=[]
            for i in range(0,len(self.accesslist)):
                self.count=0
                a=[0 for col in range(k)]
                self.countConnectivity(self.nums,k,a,0,i)
                kconnectivity.append(self.rate(self.nums,k))
                # time=self.start+i*self.interval
                # print('{:>3}s:{}连通率:{:.4f}%'.format(time,k,self.rate(self.nums,k)*100))
            self.kconnectivity.append(kconnectivity)
    def genAvgConcenDegree(self):
        pass
    def genConCeot(self):
        df=self.df
        df.dropna(axis = 0, inplace = True)
        df=df[~(df[0]=='Node')]
        df.reset_index(drop=True, inplace=True)
        dic = {}
        for index in range(df.shape[0]):
            t = eval(df[1][index][1: -1])
            startNode = eval(df[0][index]) + 1
            nextNode = eval(df[3][index][7:])
            nowDistance = df[5][index]
            dic.setdefault(t, {}).setdefault(startNode, []).append(nextNode)
        G = nx.MultiDiGraph()
        G.add_nodes_from(range(1, self.nums+1))
        n = G.number_of_nodes()
        C = []
        for t in dic:
            for startV in dic[t]:
                for endV in dic[t][startV]:
                    keys = G.add_edge(startV, endV)
            w = com.number_weakly_connected_components(G)
            #print(w)
            sum = 0
            for index in com.weakly_connected_components(G):
                subG = G.subgraph(index)
                subN = subG.number_of_nodes()
                #print('subG\'s number:', subG.number_of_nodes())
                averShortestLenOfSubG = nx.average_shortest_path_length(subG)
                #print(averShortestLenOfSubG)
                sum += averShortestLenOfSubG * subN
            C.append(n / (w * sum))
        self.con_coet=C
        pass
    def genIndicator(self):
        self.genAvgNodeDegree()
        self.genAvgMinRoute()
        self.genKConnectivity()
        self.genAvgConcenDegree()
        self.genConCeot()
        pass
    def showIndicator(self):
        self.genIndicator()
        for indicator in [self.avg_node_degree,self.avg_min_route,self.kconnectivity,self.avg_concen_degree,self.con_coet]:
            print('{}项'.format(len(indicator)),end='')
            #print(indicator)
        x_time = []
        for i in range(self.start,self.end+1,1):
            x_time.append(i)
        for indicator in [self.avg_node_degree,self.avg_min_route,self.avg_concen_degree,self.con_coet]:
            if(len(indicator)==len(x_time)):
                plt.figure()
                plt.plot(x_time, indicator, color = 'red',)
        for indicator in self.kconnectivity:
            if(len(indicator)==len(x_time)):
                plt.figure()
                plt.plot(x_time, indicator, color = 'red',)
        plt.show()
        pass
        


i=Indicators(csvpath='routes.csv',nums=30,start=3,end=50,kconnect=[2,5])
i.showIndicator()