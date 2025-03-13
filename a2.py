#!/usr/bin/env python
# coding: utf-8

# In[2]:


import yfinance as yf
import pandas as pd

# دریافت داده‌های بیت‌کوین با افزایش زمان Timeout
btc_data = yf.download("BTC-USD", start="2018-01-01", end="2025-03-10", timeout=60)


# In[3]:


df = pd.DataFrame(btc_data)

print(df)
print("##################")
print(df.shape)


# In[4]:


df["Date"] = pd.to_datetime(df.index)

print(df)


# In[5]:


print(df["Close"])
y = df["Close"].iloc[:, 0]
x = df.index
print(f" y : {y.shape}")
print(f" x : {x.shape}")


# In[6]:


import plotly.express as px
fig = px.line(x=x , y=y, title="Bitcoin Price Trend")

# نمایش نمودار
fig.show()


# ساختن ستون کلوز و اوپن برای یکشنبه و چهارشنبه و میزان سود و زیان

# In[7]:


from persiantools.jdatetime import JalaliDate
from datetime import date





df["JalaliDate"] = df["Date"].apply(lambda miladi_date:JalaliDate(miladi_date))
df["Year"] = df["Date"].apply(lambda miladi_date:JalaliDate(miladi_date).year)
df["Month"]=df["Date"].apply(lambda miladi_date:JalaliDate(miladi_date).month)
df["Day"]=df["Date"].apply(lambda miladi_date:JalaliDate(miladi_date).day)
df["Weekday"]=df["Date"].apply(lambda miladi_date:JalaliDate(miladi_date).isoweekday())


# print(btc)

cleaned_btc= df[["Open","Low","High","Close","Volume","Year","Month","Day", "Weekday" ]]

# print(cleaned_btc[cleaned_btc["Month"]==1])
# print(cleaned_btc[cleaned_btc["Month"]==1].mean())

# for group in cleaned_btc.groupby("Month"):
#     print(group)


print(cleaned_btc)


# In[8]:


filtered_df1 = cleaned_btc[cleaned_btc["Weekday"].isin([2, 5])]
filtered_df2 = filtered_df1[["Open","Close","Weekday"]]

# نمایش دیتای فیلتر شده
print(filtered_df2)
filtered_df2 = filtered_df2.drop(index="2018-01-03") 
print(filtered_df2)
print(filtered_df2.index)

filtered_df1.to_csv("filtered_bitcoin_data1.csv", index=False)
filtered_df2.to_csv("filtered_bitcoin_data2.csv", index=False)


# In[9]:


filtered_df2 = filtered_df2.reset_index()

sundays = filtered_df2[filtered_df2["Weekday"] == 2][["Date", "Open"]].rename(columns={"Date": "sundays", "Open": "sundays_open"})
wednesdays = filtered_df2[filtered_df2["Weekday"] == 5][["Date", "Close"]].rename(columns={"Date": "wednesdays", "Close": "wednesdays_close"})

# ادغام روزهای دوشنبه و پنجشنبه‌ای که بعد از آن هستند
merged = pd.merge_asof(wednesdays.sort_values("wednesdays"), sundays.sort_values("sundays"), 
                        left_on="wednesdays", right_on="sundays", direction="backward")

# محاسبه نسبت Close پنجشنبه به Open دوشنبه همان هفته
merged["Ratio_Close_Thu_Open_Mon"] = merged["wednesdays_close"] / merged["sundays_open"]

print(merged.head)


# In[10]:


initial_value = 1000

merged["Cumulative_Value"] = initial_value * merged["Ratio_Close_Thu_Open_Mon"].cumprod()

print(merged[["Ratio_Close_Thu_Open_Mon", "Cumulative_Value"]])


# In[11]:


y1 = merged["Cumulative_Value"]
x1 = merged.index
fig1 = px.line(x=x1 , y=y1 , title="interest line")

# نمایش نمودار
fig1.show()


# پیدا کردن میانگین کلوز و اوپن روز های هفته در طی این ۷سال

# In[12]:


print(cleaned_btc)


# In[13]:


cleaned_btc["Weekday"].value_counts()


# In[20]:


shanbe = (((cleaned_btc.loc[cleaned_btc["Weekday"] == 1, "Close"] - cleaned_btc.loc[cleaned_btc["Weekday"] == 1, "Open"]) / cleaned_btc.loc[cleaned_btc["Weekday"] == 1, "Open"]) * 100).sum()
shanbe = shanbe/375

yek_shanbe = (((cleaned_btc.loc[cleaned_btc["Weekday"] == 2, "Close"] - cleaned_btc.loc[cleaned_btc["Weekday"] == 2, "Open"]) / cleaned_btc.loc[cleaned_btc["Weekday"] == 2, "Open"]) * 100).sum()
yek_shanbe = yek_shanbe/375

do_shanbe = (((cleaned_btc.loc[cleaned_btc["Weekday"] == 3, "Close"] - cleaned_btc.loc[cleaned_btc["Weekday"] == 3, "Open"]) / cleaned_btc.loc[cleaned_btc["Weekday"] == 3, "Open"]) * 100).sum()
do_shanbe = do_shanbe/375

se_shanbe = (((cleaned_btc.loc[cleaned_btc["Weekday"] == 4, "Close"] - cleaned_btc.loc[cleaned_btc["Weekday"] == 4, "Open"]) / cleaned_btc.loc[cleaned_btc["Weekday"] == 4, "Open"]) * 100).sum()
se_shanbe = se_shanbe/375

char_shanbe = (((cleaned_btc.loc[cleaned_btc["Weekday"] == 5, "Close"] - cleaned_btc.loc[cleaned_btc["Weekday"] == 5, "Open"]) / cleaned_btc.loc[cleaned_btc["Weekday"] == 5, "Open"]) * 100).sum()
char_shanbe = char_shanbe/375

panj_shanbe = (((cleaned_btc.loc[cleaned_btc["Weekday"] == 6, "Close"] - cleaned_btc.loc[cleaned_btc["Weekday"] == 6, "Open"]) / cleaned_btc.loc[cleaned_btc["Weekday"] == 6, "Open"]) * 100).sum()
panj_shanbe = panj_shanbe/375

jomeh = (((cleaned_btc.loc[cleaned_btc["Weekday"] == 7, "Close"] - cleaned_btc.loc[cleaned_btc["Weekday"] == 7, "Open"]) / cleaned_btc.loc[cleaned_btc["Weekday"] == 7, "Open"]) * 100).sum()
jomeh = jomeh/375


# In[21]:


days =["شنبه" , "یکشنبه " , "دوشنبه",  "سه شنبه"  , "چهاشنبه" , "پنج شنبه" , "جمعه " ]
avg_days =[shanbe.values[0] , yek_shanbe.values[0] , do_shanbe.values[0] , se_shanbe.values[0] , char_shanbe.values[0] , panj_shanbe.values[0] 
           , jomeh.values[0]]
print(avg_days)


# In[23]:


import plotly.graph_objects as go
fig2 = go.Figure(data=[go.Bar(x=days, y=avg_days)])
fig2.show()


# معیار برای سوال ج گرفتن میانگین تفاوت کلوز و اوپن روز های هفته طی این هفت سال

# In[ ]:




