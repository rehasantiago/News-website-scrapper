import requests
import os
from bs4 import BeautifulSoup,Comment
from urllib.error import HTTPError
from urllib.error import URLError
start_url="https://www.indiatoday.in"
def category(className):
    try:
        
        response=requests.get(start_url)
    except HTTPError as e:
        print(e)
    except URLError as e:
        print('the server could not be found')
    else:
        soup=BeautifulSoup(response.text,'html.parser')
        heading=soup.findAll('a',{'class':className})[0]['href']
        return heading
def scrapeCategory(url):
    if url in start_url:
        next_url=url
    else:
        next_url=start_url+url
    response=requests.get(next_url)
    soup=BeautifulSoup(response.text,'lxml')
    diction={}
    a=soup.xpath("//div[@class='detail']//h3")
    b=soup.xpath("//div[@class='detail']//p")
    print(a)
    print(b)
        

scrapeCategory('/india')


