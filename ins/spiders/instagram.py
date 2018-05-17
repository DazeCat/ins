# -*- coding: utf-8 -*-
import scrapy
import json,re
from os.path import basename,join
from os import getcwd
import os
from .selenium_ins import extract_information
from scrapy import Request
from ..settings import IMAGES_STORE

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    alias_name = IMAGES_STORE.split('/')[-1]
    allowed_domains = ['www.instagram.com/','scontent-arn2-1.cdninstagram.com']
    start_urls = ['https://www.instagram.com/p/Bi3vjUwhKoi/?taken-by=rockchaeeun']
    static = join(getcwd(),'instagram')

    def start_requests(self):
        if not os.path.exists(join(self.static,self.alias_name,'mp4')):
            os.mkdir(join(self.static,self.alias_name,'mp4'))
        if not os.path.exists(join(self.static, self.alias_name, 'photo')):
            os.mkdir(join(self.static, self.alias_name, 'photo'))
        for link in  extract_information(self.alias_name):
            yield Request(link,callback=self.parse)
        # yield Request(self.start_urls[0],callback=self.parse)

    def parse(self, response):
        # print(response.text)
        images = []
        datas = re.findall('<script type="text/javascript">(.*?)</script>',response.text)
        # print(datas[0][21:-1])
        data = json.loads(datas[0][21:-1])
        # print(data.entry_data.PostPage[0].graphql.shortcode_media.edge_sidecar_to_children.edges[1].node.display_resources[2].src)
        shortcode_media = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']
        is_video = shortcode_media['is_video']
        post_id = shortcode_media['id']
        if is_video:
            images.append(shortcode_media['display_resources'][2]['src'])
            mp4 = shortcode_media['video_url']
            yield Request(mp4,callback=self.download_mp4)
        else:
            try:
                for node in data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']:
                    image = node['node']['display_resources'][2]['src']
                    print(image)
                    images.append(image)
            except KeyError as es:
                images.append(shortcode_media['display_resources'][2]['src'])
        yield {'image_urls': images,'post_id':post_id}

    def download_mp4(self,response):
        name = basename(response.url)
        print(name)
        with open(join(getcwd(),'instagram',alias_name,'mp4',name),'wb')as fw:
            fw.write(response.body)

