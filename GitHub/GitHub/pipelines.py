# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class GithubPipeline(object):
#     def process_item(self, item, spider):
#         return item



import pymongo
import codecs
import json
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from pymongo import MongoClient

class MongoDBpipeline(object):
    def __init__(self):
        client=MongoClient(
            settings['MONGODB_SERVER'],#MONGODB_SERVER是setting.py文件里的，这里是引用。
            settings['MONGODB_PORT']
            )
        db=client[settings['MONGODB_DB']]
        self.collection=db[settings['MONGODB_COLLECTION']]
        #模块codecs提供了一个open()方法，可以指定一个编码打开文件，使用这个方法打开的文件读取返回的将是unicode
        self.file=codecs.open('GitHub14_data_utf-8.json','wb',encoding='utf-8')#json文件的处理转为utf-8。
        
    def process_item(self, item, spider):
        valid=True
        for data in item:
            if not data:
                valid=False
                raise DropItem("Missing {0}!".format(data))#格式化输出字符串

        if valid:
            self.collection.insert(dict(item))
            log.msg("github14_info added to Mondb database!",
                    level=log.DEBUG,spider=spider)#level – 该信息的log级别,默认DEBUG调试信息
        line=json.dumps(dict(item))+'\n'
        self.file.write(line.decode("unicode_escape"))#json文件的处理转为utf-8。
        return item

#class TxtPipeline(object):
    #def __init__(self):
        #self.github_repo_file=open('github_repo.txt','wb',encoding='utf-8')
    #def process_item(self, item, spider):
        #self.github_repo_file.write(json.dumps(dict(item), ensure_ascii=False).encode('utf8') + '\n')
        #return item
    #def spider_closed(self, spider):
        #self.github_repo_file.close()
from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):#去重

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item






import scrapy

from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem

class MyImagesPipeline(ImagesPipeline):
    # def file_path(self,request,response=None,info=None):
    #     print "1111111111"+request.url+"111111111111111"
    #     print "11111111111111111111111111111111"
    #     open("image_urls.txt","a").write(request.url + "\n")
    #     image_guid = request.url.split('/')[-1]
    #     return 'full/%s' % (image_guid)

    def get_meida_request(self,item,info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self,result,item,info):
        image_paths=[x['path'] for ok,x in results if ok]
        print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        if not image_paths:
            raise DropItem("It contains no image")
        item['image_paths']=image_paths
        return item





# import requests
# from fun import settings
# import os


# class ImageDownloadPipeline(object):
#     def process_item(self, item, spider):
#         if 'image_urls' in item:
#             images = []
#             dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)

#             if not os.path.exists(dir_path):
#                 os.makedirs(dir_path)
#             for image_url in item['image_urls']:
#                 us = image_url.split('/')[3:]
#                 image_file_name = '_'.join(us)
#                 file_path = '%s/%s' % (dir_path, image_file_name)
#                 images.append(file_path)
#                 if os.path.exists(file_path):
#                     continue

#                 with open(file_path, 'wb') as handle:
#                     response = requests.get(image_url, stream=True)
#                     for block in response.iter_content(1024):
#                         if not block:
#                             break

#                         handle.write(block)

#             item['images'] = images
#         return item
