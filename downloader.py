# 1. To create a program that will take a name of 
# a given tiktok channel, and procede to download
# every single video on said channel. 



#       DO NOT USE OTHER API, CREATE REQUESTER
#       AND PARSER FROM THE GROUND UP! 

# @Selenium 
# -----------------------------------
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# -----------------------------------

import os
import requests

from bs4 import BeautifulSoup

class Downloader():
    
    def download(link, counter, name):
        # Attempted Methods:
        #   requests    N
        #   urllib3     N
        #   TikTokAPI   N
        #   
        #   RapidApi    Y


        url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"
        querystring = {"url":f"{link}","hd":"0"}

        headers = {
            "X-RapidAPI-Key": "7d58c4de90msh9eaa80c141cc63ep1514dejsnfdb0ef8759f6",
            "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        js = response.json()
        video_link = js['data']['play']
        

        video_data = requests.get(f'{video_link}')
        
        path = './videos/'
        # #CREATE DIRECTORY 
        total_path = path+f'{name}/'+'original/'
        if not os.path.exists(total_path):
            os.makedirs(total_path)


        open(total_path+name+'_'+str(counter)+'.mp4','wb').write(video_data.content)

    def parser(username):

        headers1 = { 
            "Accept" : "*/*",
            "Accept-Encoding" : "identity",
            "Accept-Language" : "en-US,en;q=0.5",
            "Cache-Control" : "no-cache",
            "Connection" : "keep-alive",
            "Cookie" : "ttwid=1%7C62B1KsRpgLc0TLrEAD_b1evkmB2yVf-mP1NU76ovHVc%7C1676055361%7Cd4fb34a23718e7c92e8bfd8f385fccbb5b76ac8d9db2c9b5cdd9b41364e1f4bf; msToken=PYSaQWNJHpunw_oMvFf4nz1oLAQ8ReggPeKZbRQ-_4h4OAW30T4YZLurU1ep1jh7TgeKoZqENKCEu20yafOp3w0wiYCE9kbQHxvJY6OfcqtkIlnSzAqgdgOcyLl6ZajeXyuKu5-7hygEJyFH; _abck=EDD041B968500D3F88BE3008876EE3E3~0~YAAQ5GsRAjHNZS+GAQAAFo2vPAk3tiCcCsE8pegmU3o/5rECdSHhziPnkxOyTZeL8F1M/I6u3ANU8uLftRTYgNKZqblk/4AOjuQjX69XD9SlpRBDenfYsYOd9itBEwIrsZ2aSFfXA2lNLyrxlzhQr5MZ8kGG8p433umBfabkcjSxJ+WwhGJDURE93547269A119F18162C4B~YAAQnmsRAj6pJimGAQAAeOdrPBJijLcRf5YtXx8OuWoriwzU+sAdnjnmwfsQJICv2GUhQ5FgjRcbgbAJPG7bPuiRVm9H8HqGKqD8DmhLxZwuYL2YATiNcY3vpYGJhoruUWjU3GR+2ieiTLt+l7XqxoKKiRKp51p1h41F/xCv9VSTN8RY3n8OKltDWJLdxIpk2kgfl1CCRFhDEBTgCGd+iIabjad2KIb7nbEGtbE6MYgGN6IKIuJYzd2zllhsovWE5JuWiwPm56MfXi22OPBOXJoLatPjEtjqGI10j0FD4CY4qDQh9LRo2SU4s9MJ2z/sa1aUldTlCI4=~1; msToken=PYSaQWNJHpunw_oMvFf4nz1oLAQ8ReggPeKZbRQ-_4h4OAW30T4YZLurU1ep1jh7TgeKoZqENKCEu20yafOp3w0wiYCE9kbQHxvJY6OfcqtkIlnSzAqgdgOcyLl6ZajeXyuKu5-7hygEJyFH",
            "DNT" : "1",
            "Host":"www.tiktok.com",
            "Pragma":"no-cache",
            "Referer":f"https://www.tiktok.com/@{username}",
            "Sec-Fetch-Dest":"empty",
            "Sec-Fetch-Mode":"cors",
            "Sec-Fetch-Site":"same-origin",
            "TE":"trailers",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0"
        }

        


        # CANT GET ALL LINKS FOR VIDEOS WITH REQUESTS
        # INSTEAD CONSIDER GETTING HTML USING SELENIUM WITH 
        # SCROLLING & WAITING, THEN PARSE AGAIN WITH 
        # SOUP 

        #       HOW DO WE BEAT THE CAPCHA WITH SELENIUM? 



        opt = Options()
        #opt.add_argument("-profile")
        #opt.add_argument("/Users/fkestner/Library/Application Support/Firefox/Profiles/td50755t.default")
        #opt.add_argument('start-maximized')
        #opt.add_argument('--disable-blink-features=AutomationControlled')
        opt.add_argument('--headless') # :: Runs in background
        driver = webdriver.Firefox(options=opt)



        
        driver.get(f"https://www.tiktok.com/@{username}")

        #driver.get("https://bot.sannysoft.com/")

        


        
        # SCROLL TO GET CONTENT
        # --------------------------------------------------------------------------------
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # for i in range(5):
        #     try:
        #         driver.execute_script("window.scrollBy(0,document.body.scrollHeight);")
        #         time.sleep(5)
        #     except Exception as e:
        #         print(e, 'COULD NOT PRESS SEARCH FOR NEW CONTENT')
        # --------------------------------------------------------------------------------


        # SAVE HTML OF THE WEB PAGE
        html = driver.page_source
        
        # QUIT FIREFOX
        driver.quit()



        # PARSE HTML AND EXTRACT LINKS 
        html = BeautifulSoup(html,'html.parser')

        counter = 0
        links = []
        for link in html.find_all('a'):

            if link.get('href') is None:
                continue
            if(link.get('href').find(f'@{username}') != -1):
                print(link.get('href'))
                links.append(link.get('href'))
                counter += 1

        print(f'TOTAL LINKS: {counter}')
        # --------------------------------------------------------------------------------
        # @links :: contains the 20-30 most recent videos of given user 

        return links


if __name__ == "__main__":
    name = "pokerllama"
    links = Downloader.parser(name)
    

    counter = 1
    for l in links:
        Downloader.download(l, counter, name)
        counter+=1

        #break

    

    



