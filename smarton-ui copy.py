## import library
import numpy as np
import pandas as pd
import streamlit as st
#import pickle
import re
#import matplotlib.pyplot as plt 
from PIL import Image
import glob
import cv2

############## Data Processing
# import data
## import features (numbers and string features)
data = pd.read_csv(r'laptops.csv',encoding='latin-1')
data = data.drop_duplicates(subset=['Model Name'], keep='first')

data['screensize'] = data['Screen Size']


## import picture of each laptops model  
pre_image = cv2.imread(r'images/white.png')
pre_image = cv2.resize(pre_image, (250,250), interpolation=cv2.INTER_LINEAR)


    

diction = {}
for file in glob.glob("images/*.png"):
    name = re.sub('/','!',file)
    name = re.sub('!images!',' ',name)
    name = re.sub('!\w+','',name)
    name = re.sub('.png','',name).strip()
    diction[name] = cv2.imread(file)


# resize laptops pictures
#image1 = image1.resize((300,200))
#image2 = image2.resize((250,190))
#image3 = image3.resize((300,200))


# remove old brands from dataframe
old_brands = ['Huawei','Xiaomi','Vero','Razer','LG','Fujitsu','Samsung','Google','Mediacom','Chuwi']
data = data[~data.Manufacturer.isin(old_brands)]

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

# Screen Size
for i in range(len(data['screensize'])):
    text = data.screensize.iloc[i]
    text = float(re.sub('"','',text))
    data.screensize.iloc[i] = text


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

brands = list(data.Manufacturer.unique())

remv_list=[]
for i in range(len(data['Model Name'])):
    txt = data['Model Name'].iloc[i]
    if '/' in txt:
        remv_list.append(i)
    else:
        pass

for i in range(len(remv_list)):
    try:
        num = int(remv_list[i])
        data = data.drop(num)
        #print(num)
    except :
        pass
############################## App

#header
html_header="""
<head>
<title>PControlDB</title>
<meta charset="utf-8">
<meta name="keywords" content="project control, dashboard, management, EVA">
<meta name="description" content="SMARTON">
<meta name="author" content="Larry Prato">
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<h1 style="font-size:250%; color:#37281E; margin:0px; padding: 1rem 1rem 1rem;font-family:Georgia";> Smarton <br>
    <hr style= " display: block;
        margin-top: auto;
        margin-bottom: auto;
        margin-left: auto;
        margin-right: auto;
        border-style: inset;
        border-width: 0.25 em;"></h1>
"""

st.set_page_config(page_title="Project Control Dashboard", page_icon="", layout="wide")
st.markdown('<style>body{background-color: #fbfff0}</style>',unsafe_allow_html=True)
st.markdown(html_header, unsafe_allow_html=True)
st.markdown(""" <style>
#MainMenu 
{visibility: hidden;}
footer 
{visibility: hidden;}
</style> """,
 unsafe_allow_html=True)


col1 , col2 = st.columns(2)

with col1:
    with st.container():
        # select brand 
        brand_name = st.multiselect('Select Brand: ',brands)
        st.write('______________________________')
        
        # main works
        works = st.multiselect('What kind of work will you frequently use your laptop for?',
            ['Graphic Design',
            'Programming',
            'Web Browsing',
            'Casual Game',
            'Hardcore Game',
            '3D Design',
            'Pro Video editing',
            'Office',
            'Watch Movie',
            'Social Media'
            ])
        st.write('______________________________')
        
        # screen size
        ## i am felexible
        ScreenSize = st.slider('Select Screensize Range: ',
            min_value = 11,
            max_value = 18,
            value = (11,18),
            step = 1)
        st.write('______________________________')
    

if 'Hardcore Game' in works or '3D Design' in works:
    ### bring gaming laptops
    ### laptops sorted by price assending

    works = 'Gaming'

elif 'Graphic Design' in works  or 'Pro Video editing' in works:
    ### bring type of laptops
    ### laptops sorted by price assending
    works = 'Workstation'

elif 'programming' in works:
    ### bring type of laptops
    ### laptops sorted by price assending
    works = 'Workstation'

elif 'Casual Game' in works :
    ### bring rame higher than 8 and high graphics and windows operation system
    ### laptops sorted by price assending
    works = 'Ultrabook'

elif 'Office' in works or 'Web Browsing' in works or 'Watch Movie' in works or 'Social Media' in works:
    ### bring casual laptops 
    ### laptops sorted assending
    works = 'Ultrabook'




with col2:
    with st.container():
        # weight of laptop
        where_used = st.selectbox('How often do you plan to carry your laptop around?',
            ['All time',
            'Occasionally',
            'hardly ever'
            ])
        st.write('______________________________')

        # feature importance
        important_features = st.multiselect('Are any of these important to you?',
            ['Using laptop as tablet',
            'TouchScreen',
            'Work alot with number',
            'Working in low light condition',
            'present often'
            ])
        st.write('______________________________')

        # operation system
        ####
        # price range
        price = st.slider('Select Price Range: ',
            min_value = 50,
            max_value = round(data.Price.max())+50,
            value = (100,500),
            step = 10)
        st.write('______________________________')




## show dataframe 
try:
    if works != 0:
        try:
            df_new = df_new[df_new.Category== works]
        except ValueError:
            st.write('no laptop selected')
        # df_new = df_new[(df_new['screensize']>=float(ScreenSize[0])) & (df_new['screensize']<=float(ScreenSize[1]))]
        df_show = df_new[df_new.Manufacturer.isin(brand_name)]
        length = len(df_show[(df_show.Price>price[0]) & (df_show.Price<price[1])].drop('Category',axis = 1))
        st.write(str('laptops remain: '+str(length)))
        main_dataframe = df_show[(df_show.Price>price[0]) & (df_show.Price<price[1])].drop('Category',axis = 1)
        main_dataframe = main_dataframe.sort_values(by=['Price'],ascending = False)
         
            

        #main_dataframe['Model Name'].unique()
        #main_dataframe = main_dataframe[main_dataframe['Model Name'].unique()]  
                 


        # name and model and other laptops features
        ## laptop model
        laptop1_model = main_dataframe['Model Name'].iloc[0]
        laptop2_model = main_dataframe['Model Name'].iloc[1]
        laptop3_model = main_dataframe['Model Name'].iloc[2]
        
        ## laptop brand
        laptop1_brand = main_dataframe['Manufacturer'].iloc[0]
        laptop2_brand = main_dataframe['Manufacturer'].iloc[1]
        laptop3_brand = main_dataframe['Manufacturer'].iloc[2]

        ## laptop screensize
        laptop1_screensize = main_dataframe['Screen Size'].iloc[0]
        laptop2_screensize = main_dataframe['Screen Size'].iloc[1]
        laptop3_screensize = main_dataframe['Screen Size'].iloc[2]

        ## laptop price
        laptop1_price = main_dataframe['Price'].iloc[0]
        laptop2_price = main_dataframe['Price'].iloc[1]
        laptop3_price = main_dataframe['Price'].iloc[2]

        ## laptop cpu
        laptop1_cpu = main_dataframe['CPU'].iloc[0]
        laptop2_cpu = main_dataframe['CPU'].iloc[1]
        laptop3_cpu = main_dataframe['CPU'].iloc[2]

        ## laptop gpu
        laptop1_gpu = main_dataframe['GPU'].iloc[0]
        laptop2_gpu = main_dataframe['GPU'].iloc[1]
        laptop3_gpu = main_dataframe['GPU'].iloc[2]

        st.write('________________')
        st.write('Result: ')
        main_dataframe = main_dataframe.astype(str)
        st.dataframe(main_dataframe.transpose())
        st.write('________________')
        name_col,col_1,col_2,col_3 = st.columns([3,5,5,5])
        with name_col:
            st.image(pre_image)
            st.write('________________')
            st.write('Brand: ')
            st.write('________________')
            st.write('Model: ')
            st.write('________________')
            st.write('Screen Size:')
            st.write('________________')
            st.write('CPU: ')
            st.write('________________')
            st.write('GPU: ')
            st.write('________________')
            st.write('Price: ')
            
        with col_1:
            try:  
                image1 = diction[laptop1_model]
                image1 = cv2.resize(image1, (250,200), interpolation=cv2.INTER_LINEAR)
                st.image(image1)
            except KeyError:
                st.write('no picture of this laptop')
            st.write('________________')
            st.write(laptop1_brand)
            st.write('________________')
            st.write(laptop1_model)
            st.write('________________')
            st.write(laptop1_screensize)
            st.write('________________')
            st.write(laptop1_cpu)
            st.write('________________')
            st.write(laptop3_gpu)
            st.write('________________')
            st.write(str(laptop1_price))

        with col_2:
            try:  
                image2 = diction[laptop2_model]
                image2 = cv2.resize(image2, (250,200), interpolation=cv2.INTER_LINEAR)
                st.image(image2)
                #st.image(image2)
            except KeyError:
                st.write('no picture of this laptop')
            st.write('________________')
            st.write(laptop2_brand)
            st.write('________________')
            st.write(laptop2_model)
            st.write('________________')
            st.write(laptop2_screensize)
            st.write('________________')
            st.write(laptop2_cpu)
            st.write('________________')
            st.write(laptop2_gpu)
            st.write('________________')
            st.write(str(laptop2_price))

        with col_3:
            try:  
                image3 = diction[laptop3_model]
                image3 = cv2.resize(image3, (250,200), interpolation=cv2.INTER_LINEAR)
                st.image(image3)
            except KeyError:
                st.write('no picture of this laptop')
            st.write('________________')
            st.write(laptop3_brand)
            st.write('________________')
            st.write(laptop3_model)
            st.write('________________')
            st.write(laptop3_screensize)
            st.write('________________')
            st.write(laptop3_cpu)
            st.write('________________')
            st.write(laptop3_gpu)
            st.write('________________')
            st.write(str(laptop3_price))
    else:
        pass

except IndexError:
    st.write('There is no laptop available with these features')



