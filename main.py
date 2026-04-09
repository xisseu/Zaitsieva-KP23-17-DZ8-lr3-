# #контейнер Расчета
# from sympy import * 
# k,T,C,L = symbols ('k C T L')
# #1 способ
# C_ost=100000
# Am_lst=[]
# C_ost_lst=[]
# for i in range(5):
#   Am=(C-L)/T
#   C_ost-=Am.subs({C:100000,T:5,L:0})
#   Am_lst.append(round(Am.subs({C:100000,T:5,L:0}),2))
#   C_ost_lst.append(round(C_ost,2))
# print('Am_lst:',Am_lst)
# print('C_ost_lst:',C_ost_lst)
# #2 способ
# Aj=0
# C_ost=100000
# Am_lst_2=[]
# C_ost_lst_2=[]
# for i in range(5):
#   Am=k*1/T*(C-Aj)
#   C_ost -= Am.subs({C:100000,T:5,k:2})
#   Am_lst_2.append(round(Am.subs({C:100000,T:5,k:2}),2))
#   Aj+=Am
#   C_ost_lst_2.append(round(C_ost,2))
# print('Am_lst_2:',Am_lst_2)
# print('C_ost_lst_2:',C_ost_lst_2)
# #Контейнер для табличного вывода 
# import pandas as pd
# Y= range(1,6)
# table1= list(zip(Y,C_ost_lst,Am_lst))
# table2= list(zip(Y,C_ost_lst_2,Am_lst_2))
# tfame=pd.DataFrame(table1,columns=['Y','C_ost_lst','Am_lst'])
# tfame2=pd.DataFrame(table2,columns=['Y','C_ost_lst_2','Am_lst_2'])
# print(tfame)
# print(tfame2)
# #Контейнер визуализации
# import numpy  as np
# import matplotlib.pyplot as plt
# plt.plot(tfame['Y'],tfame['C_ost_lst'],label='Am')
# plt.savefig('chart1.png')
# plt.figure()
# plt.plot(tfame2['Y'],tfame2['C_ost_lst_2'],label='Am2')
# plt.savefig('chart2.png')
# plt.figure()
# vals= Am_lst
# labels=[str(x) for x in range (1,6)]
# explode = (0.1,0.1,0.1,0.1,0.1)
# fig, ax= plt.subplots()
# ax.pie(vals,labels = labels, autopct ='%1.1f%%',shadow = True, explode=explode, wedgeprops ={'lw':1,'ls':'--','edgecolor':"k"}, rotatelabels = True)
# ax.axis('equal')
# plt.savefig('chart3.png')
# plt.figure()
# vals= Am_lst_2
# labels=[str(x) for x in range (1,6)]
# explode = (0.1,0.1,0.1,0.1,0.1)
# fig, ax= plt.subplots()
# ax.pie(vals,labels = labels, autopct ='%1.1f%%',shadow = True, explode=explode, wedgeprops ={'lw':1,'ls':'--','edgecolor':"k"}, rotatelabels = True)
# ax.axis('equal')
# plt.savefig('chart4.png')
# plt.figure()
# table1_am=list(zip(Y, Am_lst))
# table2_am= list(zip(Y,Am_lst_2))
# tfame_am=pd.DataFrame(table1_am,columns=['Y','Am_lst'])
# tfame2_am=pd.DataFrame(table2_am,columns=['Y','Am_lst_2'])
# plt.figure()
# plt.bar(tfame_am['Y'],tfame_am['Am_lst'])
# plt.savefig('chart5.png')
# plt.figure()
# plt.bar(tfame2_am['Y'],tfame2_am['Am_lst_2'])
# plt.savefig('chart6.png')
# plt.figure()
# #Индивидуальное задание
# from sympy import *
# k,T,C,L = symbols ('k C T L')
# #1 способ Линейный
# C_ost=2000000
# Am_lst=[]
# C_ost_lst=[]
# for i in range(16):
#   Am=(C-L)/T
#   C_ost-=Am.subs({C:2000000,T:16,L:0})
#   Am_lst.append(round(Am.subs({C:2000000,T:16,L:0}),2))
#   C_ost_lst.append(round(C_ost,2))
# print('Am_lst:',Am_lst)
# print('C_ost_lst:',C_ost_lst)
# #2 способ Уменьш остатка
# Aj=0
# C_ost=2000000
# Am_lst_2=[]
# C_ost_lst_2=[]
# for i in range(16):
#    Am=k*1/T*(C-Aj)
#    C_ost -= Am.subs({C:2000000,T:16,k:2})
#    Am_lst_2.append(round(Am.subs({C:2000000,T:16,k:2}),2))
#    Aj+=Am.subs({C:2000000,T:16,k:2})
#    C_ost_lst_2.append(round(C_ost,2))
# print('Am_lst_2:',Am_lst_2)
# print('C_ost_lst_2:',C_ost_lst_2)
# #Контейнер для табличного вывода
# import pandas as pd
# Y= range(1,17)
# table1= list(zip(Y,C_ost_lst,Am_lst))
# table2= list(zip(Y,C_ost_lst_2,Am_lst_2))
# tfame=pd.DataFrame(table1,columns=['Y','C_ost_lst','Am_lst'])
# tfame2=pd.DataFrame(table2,columns=['Y','C_ost_lst_2','Am_lst_2'])
# print(tfame)
# print(tfame2)
# #Контейнер визуализации
# import numpy  as np
# import matplotlib.pyplot as plt
# plt.plot(tfame['Y'],tfame['C_ost_lst'],label='Линейный метод')
# plt.savefig('chart7.png')
# plt.figure()
# plt.plot(tfame2['Y'],tfame2['C_ost_lst_2'],label='Уменьш остатка')
# plt.savefig('chart8.png')
# plt.figure()
# vals= Am_lst
# labels=[str(x) for x in range (1,17)]
# explode = tuple([0.05]*16)
# fig, ax= plt.subplots(figsize=(10,10))
# ax.pie(vals,labels = labels, autopct ='%1.1f%%',shadow = True, explode=explode, wedgeprops ={'lw':1,'ls':'--','edgecolor':"k"}, rotatelabels=True)
# ax.axis('equal')
# plt.savefig('chart9.png')
# plt.figure()
# vals= Am_lst_2
# labels=[str(x) for x in range (1,17)]
# explode = tuple([0.05]*16)
# fig, ax= plt.subplots(figsize=(10,10))
# ax.pie(vals,labels = labels, autopct ='%1.1f%%',shadow = True, explode=explode, wedgeprops ={'lw':1,'ls':'--','edgecolor':"k"}, rotatelabels=True)
# ax.axis('equal')
# plt.savefig('chart10.png')
# plt.figure()
# table1_am=list(zip(Y, Am_lst))
# table2_am= list(zip(Y,Am_lst_2))
# tfame_am=pd.DataFrame(table1_am,columns=['Y','Am_lst'])
# tfame2_am=pd.DataFrame(table2_am,columns=['Y','Am_lst_2'])
# plt.figure()
# plt.bar(tfame_am['Y'],tfame_am['Am_lst'])
# plt.savefig('chart11.png')
# plt.figure()
# plt.bar(tfame2_am['Y'],tfame2_am['Am_lst_2'])
# plt.savefig('chart12.png')
# plt.figure()
# # ЛР3
# import os 
# my=os.environ['first_key']
# print(my)
from sympy import *
k,T,C,L = symbols ('k C T L')
#1 способ Линейный
C_ost=20000
Am_lst=[]
C_ost_lst=[]
for i in range(6):
  Am=(C-L)/T
  C_ost-=Am.subs({C:20000,T:6,L:0})
  Am_lst.append(round(Am.subs({C:20000,T:6,L:0}),2))
  C_ost_lst.append(round(C_ost,2))
print('Am_lst:',Am_lst)
print('C_ost_lst:',C_ost_lst)
#2 способ Уменьш остатка
Aj=0
C_ost=20000
Am_lst_2=[]
C_ost_lst_2=[]
for i in range(6):
   Am=k*1/T*(C-Aj)
   C_ost -= Am.subs({C:20000,T:6,k:2})
   Am_lst_2.append(round(Am.subs({C:20000,T:6,k:2}),2))
   Aj+=Am.subs({C:20000,T:6,k:2})
   C_ost_lst_2.append(round(C_ost,2))
print('Am_lst_2:',Am_lst_2)
print('C_ost_lst_2:',C_ost_lst_2)
#Контейнер для табличного вывода
import pandas as pd
Y= range(1,7)
table1= list(zip(Y,C_ost_lst,Am_lst))
table2= list(zip(Y,C_ost_lst_2,Am_lst_2))
tfame=pd.DataFrame(table1,columns=['Y','C_ost_lst','Am_lst'])
tfame2=pd.DataFrame(table2,columns=['Y','C_ost_lst_2','Am_lst_2'])
print(tfame)
print(tfame2)
#Контейнер визуализации
import numpy  as np
import matplotlib.pyplot as plt
plt.plot(tfame['Y'],tfame['C_ost_lst'],label='Линейный метод')
plt.savefig('chart7.png')
plt.figure()
plt.plot(tfame2['Y'],tfame2['C_ost_lst_2'],label='Уменьш остатка')
plt.savefig('chart8.png')
plt.figure()
vals= Am_lst
labels=[str(x) for x in range (1,7)]
explode = tuple([0.05]*6)
fig, ax= plt.subplots(figsize=(10,10))
ax.pie(vals,labels = labels, autopct ='%1.1f%%',shadow = True, explode=explode, wedgeprops ={'lw':1,'ls':'--','edgecolor':"k"}, rotatelabels=True)
ax.axis('equal')
plt.savefig('chart9.png')
plt.figure()
vals= Am_lst_2
labels=[str(x) for x in range (1,7)]
explode = tuple([0.05]*6)
fig, ax= plt.subplots(figsize=(10,10))
ax.pie(vals,labels = labels, autopct ='%1.1f%%',shadow = True, explode=explode, wedgeprops ={'lw':1,'ls':'--','edgecolor':"k"}, rotatelabels=True)
ax.axis('equal')
plt.savefig('chart10.png')
plt.figure()
table1_am=list(zip(Y, Am_lst))
table2_am= list(zip(Y,Am_lst_2))
tfame_am=pd.DataFrame(table1_am,columns=['Y','Am_lst'])
tfame2_am=pd.DataFrame(table2_am,columns=['Y','Am_lst_2'])
plt.figure()
plt.bar(tfame_am['Y'],tfame_am['Am_lst'])
plt.savefig('chart11.png')
plt.figure()
plt.bar(tfame2_am['Y'],tfame2_am['Am_lst_2'])
plt.savefig('chart12.png')
plt.figure()

# Работа выполнена правильно. Проверила Максимова Е.А.