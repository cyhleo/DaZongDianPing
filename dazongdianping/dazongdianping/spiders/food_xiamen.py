# -*- coding: utf-8 -*-

from dazongdianping.items import DazongdianpingItem
import scrapy
from scrapy.loader.processors import MapCompose
import requests
from fontTools.ttLib import TTFont
import re

class FoodXiamenSpider(scrapy.Spider):
    name = 'food_xiamen'
    allowed_domains = ['dianping.com']
    start_url = 'http://www.dianping.com/xiamen/ch10/o3'

    def start_requests(self):
        yield scrapy.Request(self.start_url,callback=self.parse)

    def parse(self,response):
        # 获取包含小吃快餐、江河湖海鲜、咖啡厅等类型url，将url存储于base_urls列表中
        base_urls = response.xpath('.//div[@id="classfy"]/a/@href').extract()
        processor = MapCompose(lambda s:s[:-2])
        base_urls = processor(base_urls)

        # 获取热门商圈，如厦门火车站、中山路/轮渡等url编码，如r1839，将编码存储于type_loc_code列表中
        type_bussi = response.xpath('.//div[@id="bussi-nav"]/a/@href').extract()
        type_loc_code = []
        for bussi in type_bussi:
            try:
                type_loc_code.append(re.findall('/(\w\d+)o3', bussi)[0])
            except:
                type_loc_code.append(re.findall('/o3(\w\d+)', bussi)[0])

        # 根据美食分类、以及商圈组合方式，比如厦门火车站的小吃快餐，共获得576个组合方式，
        # 将其对应的url存储于class_url列表中
        class_url = []
        for url in base_urls:
            for loc in type_loc_code:
                class_url.append(url + loc)
        processor = MapCompose(lambda x: x + 'p{}')
        class_url = processor(class_url)

        for u in class_url:
            yield scrapy.Request(url=u.format(1),meta={'page':1,'base_url':u},callback=self.parse_item)





    def parse_item(self, response):

        if response.url:
            page = response.meta.get('page')
            base_url =response.meta.get('base_url')

            # 字体反爬
            css_href = response.xpath('.//link[contains(@href,"svgtextcss")]/@href').extract_first()
            css_href = 'https:' + css_href
            tagName_woff_url, shopNum_woff_url, address_woff_url = self.get_font_url(css_href)
            tagName_dict = self.get_font_file(tagName_woff_url, 'tagName')
            shopNum_dict = self.get_font_file(shopNum_woff_url, 'shopNum')
            address_dict = self.get_font_file(address_woff_url, 'address')

            li_list = re.findall('<li class="" >(.*?)<div class="operate J_operate Hide">', response.text, re.S|re.M)
            for li in li_list:
                item = DazongdianpingItem()
                # 店名
                item['shop'] = re.findall('<h4>(.*?)<\/h4>', li, re.S|re.M)[0]
                #评论数
                try:
                    comment_b = re.findall('LXAnalytics\(\'moduleClick\', \'shopreview\'\).*?>(.*?)<\/b>',li,re.S|re.M)[0]
                    comment_num_list = re.findall('>(.*?)<',comment_b,re.S|re.M)
                    comment_num = ''.join(comment_num_list)
                    for k, v in shopNum_dict.items():
                        comment_num = comment_num.replace(k, str(v))
                    item['comment_num'] = comment_num
                except:
                    item['comment_num'] = 'null'


                # 人均消费
                try:
                    per_b = re.findall('<b>￥(.*?)<\/b>', li, re.S | re.M)[0]
                    per_list = re.findall('>(.*?)<', per_b, re.S | re.M)
                    per_capita = ''.join(per_list)
                    for k, v in shopNum_dict.items():
                        per_capita = per_capita.replace(k, str(v))
                    item['per_capita'] = per_capita
                except:
                    item['per_capita'] = 'null'

                # 菜系
                type_span = re.findall('<a.*?data-click-name="shop_tag_cate_click".*?>(.*?)<\/span>', li, re.S | re.M)[0]
                type_list = re.findall('>(.*?)<', type_span, re.S | re.M)
                t = ''.join(type_list )
                for k, v in tagName_dict.items():
                    t = t.replace(k, str(v))
                item['type_food'] = t

                # 商区
                zone_span = re.findall('<a.*?data-click-name="shop_tag_region_click".*?>(.*?)<\/span>', li, re.S | re.M)[0]
                zone_list = re.findall('>(.*?)<', zone_span, re.S | re.M)
                business_zone = ''.join(zone_list)
                for k, v in tagName_dict.items():
                    business_zone = business_zone.replace(k, str(v))
                item['business_zone'] = business_zone

                # 位置
                location_span = re.findall('<span class="addr">(.*?)<\/span>', li, re.S | re.M)[0]
                location_list = re.findall('>(.*?)<', location_span, re.S | re.M)
                location = ''.join(location_list)
                for k, v in address_dict.items():
                    location = location.replace(k, str(v))
                item['location'] = location

                # 口味分数
                try:
                    taste_b = re.findall('口味<b>(.*?)<\/b>', li, re.S | re.M)[0]
                    taste_list = re.findall('>(.*?)<', taste_b, re.S | re.M)
                    taste = ''.join(taste_list)
                    for k, v in shopNum_dict.items():
                        taste = taste.replace(k, str(v))
                    print('口味：{}'.format(taste))
                    # loader.add_value('taste', taste)
                    item['taste'] = taste
                except:
                    item['taste'] ='null'

                # 环境分数
                try:
                    env_b = re.findall('环境<b>(.*?)<\/b>', li, re.S | re.M)[0]
                    env_list = re.findall('>(.*?)<', env_b, re.S | re.M)
                    env = ''.join(env_list)
                    for k, v in shopNum_dict.items():
                        env = env.replace(k, str(v))
                    # print('环境分数：{}'.format(env))
                    # loader.add_value('env', env)
                    item['env'] = env
                except:
                    item['env'] = 'null'

                # 服务分数
                try:
                    serve_b = re.findall('服务<b>(.*?)<\/b>', li, re.S | re.M)[0]
                    serve_list = re.findall('>(.*?)<', serve_b, re.S | re.M)
                    serve = ''.join(serve_list)
                    for k, v in shopNum_dict.items():
                        serve = serve.replace(k, str(v))
                    print('服务分数：{}'.format(serve))
                    item['serve'] = serve
                except:
                    item['serve'] = 'null'
                yield item

        # 从网站中提取下一页页码
        next_page = response.xpath('.//a[@title="下一页"]//@data-ga-page').extract_first()
        print('next_page:{}'.format(next_page))
        if next_page:
            yield scrapy.Request(base_url.format(next_page), meta={'page':next_page,'base_url':base_url}, callback=self.parse_item)



    def get_font_url(self, css_href):
        # 解析网页，获取tagName_woff、shopNum_woff、address_woff_url三种woff文件的url地址
        response2 = requests.get(css_href)

        tagName_woff_url = re.search('PingFangSC-Regular-tagName.*?opentype\"\),url\(\"(.*?)woff',
                                     response2.text).group(1)
        tagName_woff_url = 'https:' + tagName_woff_url + 'woff'

        shopNum_woff_url = re.search('PingFangSC-Regular-shopNum.*?opentype\"\),url\(\"(.*?)woff',
                                     response2.text).group(1)
        shopNum_woff_url = 'https:' + shopNum_woff_url + 'woff'

        address_woff_url = re.search('PingFangSC-Regular-address.*?opentype\"\),url\(\"(.*?)woff',
                                     response2.text).group(1)
        address_woff_url = 'https:' + address_woff_url + 'woff'

        return tagName_woff_url,shopNum_woff_url,address_woff_url

    def get_font_file(self, woff_url, font_class):
        # 生成编码与文字一一对应的字典
        response_font = requests.get(woff_url)
        file_name = 'font_{}.ttf'.format(font_class)
        with open(file_name, 'wb') as f:
            f.write(response_font.content)
        file = TTFont(file_name)

        font_str = '店中美家馆小车大市公酒行国品发电金心业商司超生装园场食有新限天面工服海华水房饰城乐汽香部利子老艺花专东肉菜学福饭人百餐茶务通味所山区门药银农龙停尚安广鑫一容动南具源兴鲜记时机烤文康信果阳理锅宝达地儿衣特产西批坊州牛佳化五米修爱北养卖建材三会鸡室红站德王光名丽油院堂烧江社合星货型村自科快便日民营和活童明器烟育宾精屋经居庄石顺林尔县手厅销用好客火雅盛体旅之鞋辣作粉包楼校鱼平彩上吧保永万物教吃设医正造丰健点汤网庆技斯洗料配汇木缘加麻联卫川泰色世方寓风幼羊烫来高厂兰阿贝皮全女拉成云维贸道术运都口博河瑞宏京际路祥青镇厨培力惠连马鸿钢训影甲助窗布富牌头四多妆吉苑沙恒隆春干饼氏里二管诚制售嘉长轩杂副清计黄讯太鸭号街交与叉附近层旁对巷栋环省桥湖段乡厦府铺内侧元购前幢滨处向座下県凤港开关景泉塘放昌线湾政步宁解白田町溪十八古双胜本单同九迎第台玉锦底后七斜期武岭松角纪朝峰六振珠局岗洲横边济井办汉代临弄团外塔杨铁浦字年岛陵原梅进荣友虹央桂沿事津凯莲丁秀柳集紫旗张谷的是不了很还个也这我就在以可到错没去过感次要比觉看得说常真们但最喜哈么别位能较境非为欢然他挺着价那意种想出员两推做排实分间甜度起满给热完格荐喝等其再几只现朋候样直而买于般豆量选奶打每评少算又因情找些份置适什蛋师气你姐棒试总定啊足级整带虾如态且尝主话强当更板知己无酸让入啦式笑赞片酱差像提队走嫩才更板知己无回晚微周值费性桌拍跟块调糕'
        font_list = ['', '', 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        for i in font_str:
            font_list.append(i)

        key_list = file.getGlyphOrder()
        font_dict_trans = {}
        for i in range(len(font_list)):
            font_dict_trans[key_list[i].replace('uni', '&#x') + ';'] = font_list[i]

        print('font_dict_trans:{}'.format(font_dict_trans))
        return font_dict_trans



