# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from os.path import basename
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from os.path import join
from scrapy import Request

class InsPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        post_id = item['post_id']
        urls = item['image_urls']
        for url in urls:
            yield Request(url, meta={'post_id': post_id})

    def file_path(self, request, response=None, info=None):
        post_id = request.meta['post_id']
        return join('photo',post_id,basename(request.url))
