from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

# pip install pandas
# pip install selenium
# pip install beautifulsoup4
# pip install openpyxl


# first above
data = pd.read_excel('seo.xlsx')
my_website = data.website[0]
words_list = list(data.words_list)


def google_crawler(word, website):
    driver = webdriver.Chrome(
        executable_path=r"C:\Users\Administrator\chromedriver.exe")
    driver.get('https://www.google.com/')

    # maybe need to delete
    button_agreement_address  = '#W0wltc'
    button_agreement = driver.find_element(
        by=By.CSS_SELECTOR, value=button_agreement_address)
    button_agreement.click()

    # main start
    search_input_box_address = \
        'body > div.L3eUgb > div.o3j99.ikrT4e.om7nvf > form > div:nth-child(1) > div.A8SBwf > div.RNNXgb > div > div.a4bIc > input'
    search_input_box = driver.find_element(
        by=By.CSS_SELECTOR, value=search_input_box_address)
    search_input_box.send_keys(str(word))
    search_button_address = \
        'body > div.L3eUgb > div.o3j99.ikrT4e.om7nvf > form > div:nth-child(1) > div.A8SBwf > div.FPdoLc.lJ9FBc > center > input.gNO89b'
    search_button = driver.find_element(
        by=By.CSS_SELECTOR, value=search_button_address)
    search_button.send_keys(Keys.RETURN)
    time.sleep(2)
    reply_list=[]
    website_rank=[]
    number_of_page_crawled=[]
    k=False
    for i in range(1,9):

        number_of_page_crawled.append(i)
        source = driver.page_source

        soup = BeautifulSoup(source, 'html.parser')

        text_list_unclean = soup.find_all(
            'cite', {'role': 'text'})


        for k in range(len(text_list_unclean)):
            text = text_list_unclean[k].text
            if len(text)==0:
                text = 'no text'
            if k%2==0:
                reply_list.append(text)
        
        print('k: '+str(k))
        print('page: '+str(i))
        for site_index in range(len(reply_list)):
            site = reply_list[site_index]
            print(site)
            if website in site:
                print(site+' :' + ' this site is similar to my website')
                website_rank.append(site_index)
                k=True
                break
        if k==True:
            break
        else:
            pass

        print('')
        print('')

        # ================== Lets Go Next Page =============
        next_page_number = i+2
        print(next_page_number)
        next_page_address = \
            '#botstuff > div > div:nth-child(2) > table > tbody > tr > td:nth-child('+str(next_page_number)+') > a'
        next_page = driver.find_element(
            by=By.CSS_SELECTOR, value=next_page_address)
        next_page.click()
        time.sleep(2)

    driver.quit()

    return word, str(website_rank[0]+1), str(number_of_page_crawled[-1]), str(reply_list[website_rank[0]])


for word in words_list:
    word, website_rank, number_of_page_crawled, url = google_crawler(word,website=my_website)
    df.loc[len(df)] = [word, number_of_page_crawled, website_rank, url]
    print('done.')
    time.sleep(3)


# finally
df.to_csv(my_website+'_crawled'+'.xlsx')
