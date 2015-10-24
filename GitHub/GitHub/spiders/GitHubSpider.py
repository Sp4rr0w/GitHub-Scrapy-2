#coding:utf-8
#!/usr/bin/env python
#author:Z0fr3y
#update:2015-10-11
#version:1.0--1.2--1.3--1.4!----------------------2.0(规则变了)!
#name:GitHubSpider
#运行：scrapy crawl github 或者加上 -s LOG_FILE=scrapy.log
#暂停：ctrl+c
#再运行：scrapy crawl github -s JOBDIR=crawl/github_stop
import urllib
from scrapy import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
#from scrapy.spiders import CrawlSpider, Rule
from GitHub.items import Github_Item
import pymongo
import sys
import os
reload (sys)
sys.setdefaultencoding("utf-8")#这3句话让爬到的内容是utf-8的
host="https://github.com"
a=1#followers为零的人数
q=1#判断
j=0#判断
b=0#限制爬取数量
#c=30#爬取深度为30
f_newlist=[]#文件名（不包含后缀），避免重复爬取。
filecount = 0#文件数量
followers_list=["https://github.com/1st1",]#用户主页链接
followers_urls=["https://github.com/1st1/followers",]#存储所有followers不为零的用户followers页面，以便进一步爬取
counter=0#多少followers
followers_url_people=51#每个follwers页面最多为51位
class GithubSpider(Spider):
    """
    爬取GitHub网站中用户信息
    """
    name = 'github'
    allowed_domains = ['github.com']
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    }
    start_urls = ["https://github.com/1st1",]
    #def __init__(self,category=None,*args,**kwargs):
        #super(GithubSpider,self).__init__(*args,**kwargs)
        
    def parse(self,response):
        print "~"*60+"start"
        print response.url
        people_mainpage=Selector(response)
        
        self.getfile()
        self.filesnum()
        print "saved "+str(filecount)+" people.    OK-Continue~~~"
        global f_newlist
        global followers_list
        people=Github_Item()#以下是爬取用户的详细信息
        people['home_page']=response.url
        people_profile=people_mainpage.xpath('//div[@class="column one-fourth vcard"]')
        people['image_urls'] = people_profile.xpath('a[1]/img/@src').extract()
        x1=people_profile.xpath('h1/span[@class="vcard-fullname"]/text()').extract()
        if x1==[]:#没有if/else 会出现超越边界错误。以下都是
            people['fullname']="None"
        else:
            people['fullname']=x1[0]    
        for i in range(len(f_newlist)):
            if (people['fullname']==f_newlist[i]):
                if followers_urls==[]:
                    break
                    #如果和followers_urls相等  则跳出
                else:
                    if followers_list !=[]:
                        followers_1=followers_list[0]
                        followers_list.remove(followers_1)
                        yield Request(url=followers_1,callback=self.parse,dont_filter=True)
        
        x2=people_profile.xpath('h1/span[@class="vcard-username"]/text()').extract()
        if x2==[]:
            people['username']="None"
        else:
            people['username']=x2[0]
        x3=people_profile.xpath('//li/@title').extract()
        if x3==[]:
            people['organization']="None"
        else:
            people['organization']=x3[0] 
        x4=people_profile.xpath('//a[@class="email"]/text()').extract()
        if x4==[]:
            people['mail']="None"
        else:
            people['mail']=x4[0]
        
        x5=people_profile.xpath('//time[@class="join-date"]/text()').extract()
        if x5==[]:
            people['joined']="None"
        else:
            people['joined']=x5[0]
        x6=people_profile.xpath('div[@class="vcard-stats"]/a[1]/strong[@class="vcard-stat-count"]/text()').extract()
        if x6==[]:
            people['followers']="None"
        else:
            people['followers']=x6[0]
        x7=people_profile.xpath('div[@class="vcard-stats"]/a[2]/strong[@class="vcard-stat-count"]/text()').extract()
        if x7==[]:
            people['starred']="None"
        else:
            people['starred']=x7[0]
        x8=people_profile.xpath('div[@class="vcard-stats"]/a[3]/strong[@class="vcard-stat-count"]/text()').extract()
        if x8==[]:
            people['following']="None"
        else:
            people['following']=x8[0]
        popular_repo=people_mainpage.xpath('//div[@class="columns popular-repos"]/div[@class="column one-half"][1]')
        people['popular_repos']=" "
        for i in range(1,6):#这是popular_repos数据
            people['popular_repos']=people['popular_repos']+" "+' '.join(popular_repo.xpath('div/ul[@class="boxed-group-inner mini-repo-list"]/li['+str(i)+']/a/span[2]/span/text()').extract())
        repo_contribution=people_mainpage.xpath('//div[@class="columns popular-repos"]/div[@class="column one-half"][2]')
        people['repo_contributions']=" "
        for i in range(1,6):#这是repo_contributions数据
            people['repo_contributions']=people['repo_contributions']+" "+' '.join(repo_contribution.xpath('div/ul[@class="boxed-group-inner mini-repo-list"]/li['+str(i)+']/a/span[2]/span[1]/text()').extract())+"/"+' '.join(repo_contribution.xpath('div/ul[@class="boxed-group-inner mini-repo-list"]/li['+str(i)+']/a/span[2]/span[2]/text()').extract())
        
        followers_page=host+''.join(people_mainpage.xpath('//a[@class="vcard-stat"][1]/@href').extract())
        xxxx=people
        fh=open('GitHub/media/people/'+people['fullname']+'.txt','w')
        fh.write(str(xxxx))
        fh.close()
        global b
        if(b<50000):
            b+=1
            #have a error!!!!!!!!!!!!!!!!!
            if people['home_page']!=host:
                print "crawl "+str(b)+" people"
                yield people#yield people 才能把数据存入数据库和json文件
            yield Request(url=followers_page,callback=self.parse_followers,dont_filter=True)

    def parse_followers(self,response):
        print "~"*60+"parse_followers"
        print response.url#followers页面
        global followers_urls
        global followers_list
        people_parse_one=Selector(response)
        ########################################################
        counterr=people_parse_one.xpath('//span[@class="counter"]/text()').extract()
        counter=counterr[0]
        #follower页面人数表示为"123,456"
        counter=int(counter.replace(',',''))
        if counter==0:
            yield Request(url=followers_list[0],callback=self.parse,dont_filter=True)
        elif counter>followers_url_people:
            counter1=counter/followers_url_people+1
            #一个页面有51个人，counter1指有多少页面
            for o in range(2,counter1+1):
                followers_urls.append(response.url+"?page="+str(o))
        else:
            pass

        followers_urls_2=[]#去重
        for m in range(len(followers_urls)):
            if followers_urls[m] not in followers_urls_2:
                followers_urls_2.append(followers_urls[m])

        followers_urls=followers_urls_2
        #尝试把所有关注者（followers）的主页面链接保存下来
        for i in range(1,52):
            followers_link=host+''.join(people_parse_one.xpath('//ol[@class="follow-list clearfix"]/li['+str(i)+']/a/@href').extract())
            followers_list.append(followers_link)

        followers_list_2=[]#去重
        for m in range(len(followers_list)):
            if followers_list[m] not in followers_list_2:
                followers_list_2.append(followers_list[m])

        followers_list=followers_list_2
        if host in followers_list:
            followers_list.remove(host)
        followers_1=followers_list[0]#先把要取的一个保存为followers_1  然后再删掉  再爬取followers_1。
        followers_list.remove(followers_1)
        print "len(followers_list):"+str(len(followers_list))
        yield Request(url=followers_1,callback=self.parse_one,dont_filter=True)

    def parse_one(self,response):
        print "~"*60+"parse_one_start"
        print response.url
        people_parse_one=Selector(response)
        x=people_parse_one.xpath('//div[@class="vcard-stats"]/a[1]/strong[@class="vcard-stat-count"]/text()').extract()
        followers_page=host+''.join(people_parse_one.xpath('//a[@class="vcard-stat"][1]/@href').extract())

        #x[-1]取最后面一个字符  eg：1.6k人数、2.4m人数
        #x[:-1]从开始取到倒数第二个数
        xx=x[0]
        rr=1
        if xx[-1]=="k":
            rr=xx[:-1]
            rr=int(float(rr)*1000)
        elif xx[-1]=="m":
            rr=xx[:-1]
            rr=int(float(rr)*1000*1000)
        else:
            rr=int(xx)
        
        print "followers:"+str(rr)
        #判断followers是否等于0
        if rr!= 0:
            followers_urls.append(followers_page)
            print "followers is not 0 ....Go to--->"
            yield Request(url=response.url,callback=self.parse,dont_filter=True)
        else:
            #当x=['0']时 不再返回前一页面（难搞），而是重新爬取followers_urls里面链接。
            if followers_list==[]:
                if followers_urls != []:
                    followers_1=followers_urls[0]
                    followers_urls.remove(followers_1)
                    yield Request(url=followers_1,callback=self.parse,dont_filter=True)
            else:
                print "followers_list第一个参数:"
                print followers_list[0]  
                followers_1=followers_list[0]#先把要取的一个保存为followers_1  然后再删掉  再爬取followers_1。
                followers_list.remove(followers_1)
                yield Request(url=followers_1,callback=self.parse,dont_filter=True)
    
    def getfile(self):#获取文件名（不包含后缀)
        path1 = r'GitHub\media\people'
        f_list = os.listdir(path1)
        global f_newlist
        for i in range(len(f_list)):
            l,b=os.path.splitext(f_list[i])
            f_newlist.append(l)
        return f_newlist
    def filesnum(self):#获取已下载用户的txt文件数量
        global filecount 
        filecount = 0
        path2 = r'GitHub\media\people'
        #path2 = r'e://scrapy/GitHub/GitHub/media/people'
        for root, dirs, files in os.walk(path2):
            #print files
            fileLength = len(files)
            if fileLength != 0:
                filecount = filecount + fileLength
        return filecount
        #print "The number of files under <%s> is: %d" %(path,count)


#1.通过scrapy进行大数据采集时，默认的scrpay crawl spider 是不能暂停的
#但是在settings.py文件里加入下面的代码： 
#JOBDIR='github.com'
#crawl/github_stop是目录  按ctrl+c时会把暂停的数据存放到那里面
#scrapy提供了相关的方法保存采集的作业状态:
#ctrl+c之后再启动时输入
#scrapy crawl github -s JOBDIR=crawl/github_stop

#2.yield：生成器
# 任何使用yield的函数都称之为生成器
# def count(n):  
#     while n > 0:  
#         yield n   #生成值：n  
#         n -= 1
# 使用yield，可以让函数生成一个序列
# 该函数返回的对象类型是"generator"，通过该对象连续调用next()方法返回序列值。

# c = count(5)  
# c.next()  
# >>> 5  
# c.next()  
# >>>4  