import requests
import lxml.html
import time
import threading
import queue
import keyboard
import random
import sys
import os

def request_site(url):
    
    user_agent_list = [
    #Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        #Firefox
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
    ]

    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    response = requests.get(url,headers=headers)
    return response



directory='C:\\Users\\dell\\Desktop\\testScrapy\\scrape'
start_url='https://www.indiatoday.in'
categories1=['/india','/world','/fact-check','/fyi','/mail-today','/travel','/business']
categories2=['/movies','https://www.indiatoday.in/technology','/sports','/fact-check','/lifestyle','https://www.indiatoday.in/education-today','/television','/auto']
def join_url(url):
    if start_url in url:
        return url
    else:
        url=start_url+url
        return url


def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write('{}\n'.format(data))
        



def type1(url):
    name = os.path.join(directory,'scrape.txt')
    if not os.path.isfile(name):
        write_file(name,'')
    response=request_site(url)
    tree=lxml.html.fromstring(response.text)
    heading=tree.xpath("//div[@class='detail']//h3/@title")
    para=tree.xpath("//div[@class='detail']//p/text()")
    dictionary=dict(zip(heading,para))
    append_to_file(name,dictionary)
    print(dictionary)
    url=start_url
    next_url=tree.xpath("//li[@class='pager-next']//a/@href")
    url=join_url(next_url[0])
    while url:
        response=request_site(url)
        tree=lxml.html.fromstring(response.text)
        heading=tree.xpath("//div[@class='detail']//h3/@title")
        para=tree.xpath("//div[@class='detail']//p/text()")
        dictionary=dict(zip(heading,para))
        append_to_file(name,dictionary)
        print(dictionary)
        next_url=tree.xpath("//li[@class='pager-next']//a/@href")
        if next_url==[]:
            break
        else:
            url=join_url(next_url[0])



def type2(url):
    response=request_site(url)
    tree=lxml.html.fromstring(response.text)
    urls=[]
    category=tree.xpath("//span[@class='widget-title']//a/@href")
    for i in category:
        urls.append(join_url(i))
    for i in urls:
        time.sleep(2)
        type1(i)



def scrapeForType1(url):
    url=join_url(url)
    type1(url)



def scrapeForType2(url):
    url=join_url(url)
    type2(url)


if not os.path.exists(directory):
    os.makedirs(directory)






q1=queue.Queue()
q2=queue.Queue()

for i in range(7):
    t=threading.Thread(target=scrapeForType1,name='thread {}'.format(i+1),args=(categories1[i],),daemon=True)
    q1.put(t)
    t.start()
while not q1.empty():
    t=q1.get()
    t.join()
for i in range(8):
    t=threading.Thread(target=scrapeForType2,name='thread {}'.format(i+1),args=(categories2[i],),daemon=True)
    q2.put(t)
    t.start()
while not q2.empty():
    t=q2.get()
    t.join()

if keyboard.is_pressed('a'):
    sys.exit()



