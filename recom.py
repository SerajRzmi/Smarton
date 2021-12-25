## import library
import numpy as np
import pandas as pd
import streamlit as st
#import pickle
import re
#import matplotlib.pyplot as plt 


# import data
data = pd.read_csv(r'laptops.csv',encoding='latin-1')

# remove kg in weight and conver to float
for i in range(len(data)): 
    txt = data.Weight.iloc[i] 
    txt = re.sub('kg','',txt)
    try :
        txt = float(txt)
    except ValueError :
        txt = re.sub('s','',txt)
        txt = float(txt)
    data.Weight.iloc[i] = txt

#labeling each weight
data['Weight2']='newcolumn'
for i in range(len(data)): 
    wieght = float(data.Weight.iloc[i])
    if wieght <=1.41 :
        data.Weight2.iloc[i]='LightWeight'
    elif wieght >1.41 and wieght < 2 :
        data.Weight2.iloc[i]='Medium'
    elif wieght >= 2:
        data.Weight2.iloc[i]='HeavyWeight'
    else:
        print('error')

#remove 'GB' from ram
for i in range(len(data)): 
    txt = data.RAM.iloc[i] 
    txt = re.sub('GB','',txt)
    txt = int(txt)
    data.RAM.iloc[i] = txt

#clustering ram 
data['RAM2']='newcolumn'
for i in range(len(data)): 
    ram = float(data.RAM.iloc[i])
    if ram ==2 or ram ==4 or ram ==6 :
        data.RAM2.iloc[i]='LowRam'
    elif ram == 8 :
        data.RAM2.iloc[i]='MediumRam'
    elif ram == 12 or ram ==16:
        data.RAM2.iloc[i]='GoodRam'
    elif ram == 24 or ram == 64 or ram == 32:
        data.RAM2.iloc[i]='HighRam'
    else:
        print('error')


        
# seprate length and width and calculate area
data['ScreenSize']='newcolumn'
for i in range(len(data)): 
    text = data.Screen.iloc[i] 
    text = re.search('\d+x\d+',text)[0]
    data.ScreenSize.iloc[i] = text
    
    
data['length']='newcolumn'
for i in range(len(data)): 
    txt = data.ScreenSize.iloc[i] 
    txt = re.search('\d+x',txt)[0]
    txt = re.sub('x','',txt)
    data.length.iloc[i] = int(txt)
    
data['width']='newcolumn'
for i in range(len(data)): 
    txt = data.ScreenSize.iloc[i] 
    txt = re.sub('\d+x','',txt)
    data.width.iloc[i] = int(txt)

    
## area
data['area']=data.length * data.width

## labeling Screen
data['ScreenCat']='newcolumn'
for i in range(len(data)): 
    screen = int(data.area.iloc[i])
    if screen <= 1900000 :
        data.ScreenCat.iloc[i]='LowScreen'
    elif screen > 1900000 and screen <= 2900000  :
        data.ScreenCat.iloc[i]='MediumScreen'
    elif screen > 3000000 and screen <= 4100000:
        data.ScreenCat.iloc[i]='GoodScreen'
    elif screen > 4200000 and screen < 7000000 :
        data.ScreenCat.iloc[i]='VeryGoodScreen'
    elif screen > 7000000 :
        data.ScreenCat.iloc[i]='HighScreen'
    else:
        print('error')

# labeling Touch Screen
data['TouchScreen']='newcolumn'
for i in range(len(data)):
    text = data.Screen.iloc[i]
    if re.search('Touchscreen',text):
        data.TouchScreen.iloc[i] = 'Touch'
    else:
        data.TouchScreen.iloc[i] = '0'


# price string change to float dtype
for i in range(len(data)):
    text = data['Price (Euros)'].iloc[i]
    text = re.sub(',','.',text)
    data['Price (Euros)'].iloc[i] = float(text)
data['Price (Euros)']=data['Price (Euros)'].astype(float)
data.rename(columns={'Price (Euros)':'Price'},inplace = True)

# Selected Column 
df = data[['Manufacturer','Weight2','ScreenCat','RAM2','Category']]       
df_new = data[['Manufacturer','Model Name','Screen Size','Screen','CPU','GPU','Price','Category']]


brands = []
for x in df.Manufacturer:
    if x not in brands:
        brands.append(x)



brand_name = st.multiselect('select brands: ',brands)
st.write(brand_name)
works = st.multiselect('WHAT DO YOU WANT FROM LAPTOP?',
    ['Office',
    'Graphic Design',
    'Programming',
    'Wide Screen',
    'Web Browsing',
    'Gaming',
    'Architeture Software',
    'Watch Movie'
    ])
st.write(works)


price = st.slider('CHOOSE PRICE RANGE: ',
    min_value = round(data.Price.min())-50,
    max_value = round(data.Price.max())+50,
    value = (30,500),
    step = 10)

st.write('Min Price is:   ',
    price[0],
    'Max Price is:  ',
    price[1])

touch = st.checkbox('Do You need Touchscreen Laptop?',
    value = False)
if touch:
    st.write('Touch On')
else:
    pass


if 'Gaming' in works:
    df_new = df_new[df_new.Category=='Gaming']
    df_show = df_new[df_new.Manufacturer.isin(brand_name)]
    st.write('Top nearest: ')
    st.dataframe(df_show[(df_show.Price>price[0]) & (df_show.Price<price[1])][:7])



