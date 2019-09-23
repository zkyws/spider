import scrapy
import re
import json
from wangyiyun.Decrypt import Func
import requests

class WangYiYun(scrapy.Spider):
    name = "wangyiyun"
    allowed_domains = ["music.163.com"]
    start_urls = ["https://music.163.com/discover/toplist?id=3778678"]

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
        }


    def parse(self, response):
        lis = response.xpath("//ul[@class='f-hide']/li")
        for li in lis:
            song_href = li.xpath("./a/@href").get()
            song_name = li.xpath("./a/text()").get()
            SongID = re.search("id=(.*)",song_href).group(1)
            SongComment_url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='.format(SongID)
            data = Func.EncryptData(1)
            # 发现评论不管有多少条，只能查看到前251页的评论内容(不知道是bug还是就是这种设计)，所以不能以总评论数来作为是否下一页的判断标准
            # totlepage = json.loads(requests.post(url=SongComment_url,data=data,headers=headers).text)["total"]//20+1
            # for i in range(1,totlepage+1):
            #     data = Func.EncryptData(i)
            #     yield scrapy.FormRequest(url=SongComment_url,formdata=data,callback=self.getComment,meta={"song_name":song_name})
            # break
            yield scrapy.FormRequest(url=SongComment_url,headers=self.headers,formdata=data,callback=self.getComment,meta={"song_name": song_name,"SongComment_url": SongComment_url,"page":1})
    def getComment(self,response):
        print("网页返回：")
        print(response.text)
        if re.search("-460",response.text):
            print("我被封了")
            with open(file="我被封了",mode="a",encoding="utf-8") as fp:
                fp.write("\r\n"+"我被封了"+"\r\n")
        Song_name = response.meta.get("song_name")
        SongComment_url = response.meta.get("SongComment_url")
        page = response.meta.get("page")
        content_json = json.loads(response.text)
        is_haveMore = content_json["more"]
        comments = content_json["comments"]
        for Comment in comments:
            UserName = Comment["user"]["nickname"]
            Comment_content = Comment["content"]
            LikedCount = Comment["likedCount"]
            item = {
                "Song_name": Song_name,
                "UserName": UserName,
                "Comment_content": Comment_content,
                "LikedCount": LikedCount
            }
            yield item
        if is_haveMore:
            print("还有下一页")
            print(is_haveMore)
            data = Func.EncryptData(page+1)
            yield scrapy.FormRequest(url=SongComment_url,headers=self.headers,formdata=data, callback=self.getComment,meta={"song_name": Song_name,"SongComment_url": SongComment_url,"page":page+1})







