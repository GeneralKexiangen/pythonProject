import pandas as pd
from datetime import datetime
import matplotlib.pylab as plt
from statsmodels.tsa.arima.model import ARIMA
from arch import arch_model
import numpy as np
import numpy.linalg as la
data= pd.read_excel('/Users/kehaigen/PycharmProjects/pythonProject/pt_st/armaModel20240327/auto.xlsx',
                    sheet_name="Sheet1",
                    index_col='year'
                    )
data.index = pd.to_datetime(data.index)
maxestu_dict={}
estu_frame=pd.DataFrame()
for j in range(1826):
# for j in range(20):
    try:
        ts=data.iloc[:,j]
        arma_model=ARIMA(ts,order=(1,1,1)).fit()
        RESID=arma_model.resid
        RESID = RESID.fillna(0)
        garch_model= arch_model(RESID,vol='GARCH',p=1,q=1,dist='normal').fit(disp='off')
        RESID_garch=garch_model.resid
        x=np.array(RESID).reshape(16,1)
        y=np.array(RESID_garch).reshape(16,1)
        H=x.dot(la.inv(x.T.dot(x))).dot(x.T)
        estu_dict={}
        for i in range(16):
            estu=y[i,0]/(y.std()*np.sqrt(1-H[i,i]))
            estu_dict[ts.index[i]] = estu
        estu_series=pd.Series(estu_dict)
        a= pd.DataFrame(estu_series)
        a= a.rename(columns={a.columns[-1]:data.columns[j]})
        estu_frame=pd.concat([estu_frame,a],axis=1)
        if abs(estu_series).max() in list(estu_series):
            maxestu_dict[data.columns[j]] = abs(estu_series).max()
        else:
            maxestu_dict[data.columns[j]] = -abs(estu_series).max()
    except:
        pass
    continue
maxestu_series=pd.Series(maxestu_dict)
maxestu_frame=pd.DataFrame(maxestu_series)


estu_frame_abs=abs(estu_frame)
print(estu_frame_abs)

# for i in estu_frame_abs.idxmax().loc[estu_frame_abs.idxmax()>=16].index:
#     del estu_frame_abs[i]

for j in range(1826):
    estu_frame_abs.loc[estu_frame_abs.index<estu_frame_abs.idxmax()[j],estu_frame_abs.columns[j]]=0;\
    estu_frame_abs.loc[estu_frame_abs.index>=estu_frame_abs.idxmax()[j], estu_frame_abs.columns[j]] =estu_frame_abs.max()[j]

print(estu_frame_abs)
estu_frame_abs.to_excel('result.xlsx')
