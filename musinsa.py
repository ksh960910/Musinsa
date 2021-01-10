import requests
import re
from bs4 import BeautifulSoup
import pymongo

item_info_dict = dict()

connection = pymongo.MongoClient()
item_db = connection.musinsa
item_collection = item_db.item_collection

for page in range(1,101):
    url = 'https://search.musinsa.com/ranking/best?period=now&mainCategory=&subCategory=&leafCategory=&price=&golf=false&newProduct=false&exclusive=false&discount=false&soldOut=false&page=' + str(page) + '&viewType=small&device=&priceMin=&priceMax='
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    items = soup.select('li.li_box')
    for item in items:
        item_rank = item.select_one('p.n-label.label-default.txt_num_rank')
        item_rank = re.sub('<.*?>', '', str(item_rank))
        item_rank = re.sub('\s','',item_rank)
        item_rank = re.sub('위.*', '', item_rank)
        item_brand = item.select_one('p.item_title').text
        item_brand = re.sub('\s','',item_brand)
        item_name = item.select_one('p.list_info').text
        item_name = re.sub('\s','',item_name)
        item_price = item.select_one('p.price').text
        item_price = re.sub('<.*>', '', item_price)
        item_price = re.sub('\s', '', item_price)
        item_price = re.sub(',','',item_price)

        if item_price.split('원')[1]!='':
            item_ori_price = item_price.split('원')[0]
            item_discount_price = item_price.split('원')[1]
        elif item_price.split('원')[1]=='':
            item_ori_price = item_price.split('원')[0]
            item_discount_price = item_price.split('원')[0]

        item_description = item.select_one('div.box-icon-right').text
        item_description = re.sub('\s', '', item_description)
        item_review = item.select_one('p.point > span.count')
        item_review = re.sub('<.*?>', '', str(item_review))
        item_review = re.sub('None', '', item_review)
        item_coupon = item.select_one('span.txt_discount_price')
        item_coupon = re.sub('<.*?>', '', str(item_coupon))
        item_coupon = re.sub('원','',item_coupon)
        item_coupon = re.sub('None', '', item_coupon)

        item_info_dict['rank'] = int(item_rank)
        item_info_dict['brand'] = item_brand
        item_info_dict['name'] = item_name
        item_info_dict['original price'] = int(item_ori_price)
        item_info_dict['selling price'] = int(item_discount_price)
        item_info_dict['description'] = item_description
        item_info_dict['review'] = item_review
        item_info_dict['coupon discount price'] = item_coupon

        if item_info_dict['description'] =='':
            del item_info_dict['description']
        if item_info_dict['review'] =='':
            del item_info_dict['review']
        if item_info_dict['coupon discount price'] =='':
            del item_info_dict['coupon discount price']


        item_collection.insert_one(item_info_dict.copy())

    #좋아요 수 출력 불가능
    # item_code = item.select_one('a[href]')
    # item_code = re.sub('<.*goods/', '', str(item_code))
    # item_code = re.sub('[?](.*?).*[\n].*[\n].*', '', item_code)
    # item_like = item.select_one('#like_' + str(item_code))


