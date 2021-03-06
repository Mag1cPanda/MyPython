from html.parser import HTMLParser
from html.entities import name2codepoint
from urllib import request
import re
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super(MyHTMLParser,self).__init__()
        self.j_time = False #这些布尔值是为了在handle_data里作处理data的判断条件。
        self.j_title = False
        self.j_location = False
        self.j_year = False
        self.all_info=[]

    def handle_starttag(self, tag, attrs):
        if tag == 'span' and ('class','say-no-more') in attrs:
            self.j_year=True
        elif tag == 'span' and ('class','event-location') in attrs:
            self.j_location=True
        elif tag == 'h3' and ('class','event-title') in attrs:
            self.j_title=True
        elif tag == 'time':
            self.j_time=True

    def handle_data(self,data):
        if self.j_year is True:   #经大佬提醒这里很关键，要给个正则约束年份只读数字进去。[0-9]就是只读数字。否则会读出两个莫名其妙的字符。
            if re.match(r'[0-9]',data.strip()):
                self.all_info.append(dict(年份=data))
        elif self.j_time is True:
            self.all_info.append(dict(时间=data))
        elif self.j_location is True:
            self.all_info.append(dict(地点=data))
        elif self.j_title is True:
            self.all_info.append(dict(会议主题=data))


def deal(content):
    cope=MyHTMLParser()
    cope.feed(content)
    count=0       #这里可以用大佬的enumerate（枚举）
    for i in cope.all_info:
        count += 1
        print(i)
        if count % 4 == 0:
            print('-------------------------------------------------')

with request.urlopen('https://www.python.org/events/python-events/') as f:
    Data = f.read()


print(deal(Data.decode('utf-8')))
