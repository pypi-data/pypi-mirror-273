import pandas as pd
import sys
import subprocess as sp
import matplotlib.pyplot as plt
import numpy as np
sp.call('wget -nc https://data.cdc.gov/api/views/3rge-nu2a/rows.csv',shell=True)
d=pd.read_csv('rows.csv')
months=d.month.unique()
days=[]
#age=18-29,30-49,50-64,65-79,80+
if len(sys.argv)==1: 
 print('enter one of five age groups: vuv 80+')
 print('18-29,30-49,50-64,65-79,80+')
 sys.exit(0)
else:
 age=sys.argv[1]
for i in months:
 for j in range(4):
  days.append(i+'.'+str(j))
 vwo=d.loc[(d.outcome=='death') & (d['Age group']==age),'Vaccinated with outcome']
 fvp=d.loc[(d.outcome=='death') & (d['Age group']==age),'Fully vaccinated population']
 v=vwo/fvp
 uwo=d.loc[(d.outcome=='death') & (d['Age group']==age),'Unvaccinated with outcome']
 up=d.loc[(d.outcome=='death') & (d['Age group']==age),'Unvaccinated population']
 u=uwo/up
#print(len(days),len(v),len(u))
def main():
 plt.plot(range(len(v)),v,'-k')
 plt.plot(range(len(u)),u,'--k')
 days.append(" ")
 days.append(" ")
# print("days= ",len(days))
 plt.xticks(np.arange(0,len(days),5),days[::5],rotation=90)
 plt.legend(('vaccinated','unvaccinated'))
 plt.title('COVID-19 mortality for '+age+' age group')
 plt.savefig(age+'.png',bbox_inches='tight')
 print(age+'.png image file is generated')
 plt.close()
main()
