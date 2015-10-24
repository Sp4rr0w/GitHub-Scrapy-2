# -*- coding: utf-8 -*-

# Scrapy settings for GitHub project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os
BOT_NAME = 'GitHub'
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))#返回绝对路径（#返回文件路径）
SPIDER_MODULES = ['GitHub.spiders']
NEWSPIDER_MODULE = 'GitHub.spiders'

#ITEM_PIPELINES=['GitHub.pipelines.MongoDBPipeline']
ITEM_PIPELINES={
    'scrapy.contrib.pipeline.images.ImagesPipeline':1,
    'GitHub.pipelines.MongoDBpipeline':300,
    }
#ITEM_PIPELINES=['scrapy.contrib.pipeline.images.ImagesPipeline']#图片管道。
MONGODB_SERVER="localhost"
MONGODB_PORT=27017
MONGODB_DB="github"
MONGODB_COLLECTION="github14_info"
DOWLOAD_DELAY = 2
IMAGES_STORE = os.path.join(PROJECT_DIR,'media/people_image')
IMAGES_EXPIRES = 90
IMAGES_THUMBS = {
     'small': (50, 50),
}

COOKIES_ENABLED = False
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'GitHub (+http://www.yourdomain.com)'
LOG_FILE = "logs/scrapy.log"
USER_AGENT = ''
DOWLOAD_MIDDLEWARES={
	'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'GitHub.rotate_useragent.RotateUserAgentMiddleware':400,
}

JOBDIR='github.com'

#DEPTH_LIMIT=xx#限制爬取深度
