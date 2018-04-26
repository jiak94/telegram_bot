import requests
import json
import telegram
from lxml import etree

BRANDS = json.load(open('shade_brand.json'))


def search_brand(keyword):
    res = list()
    for entry in BRANDS:
        if keyword.lower() in entry['name'].lower():
            tmp = [entry['name'], entry['id']]
            res.append(tmp)
    return res


def search_product(brand_id):
    url = "http://findation.com/products?brand_id=" + brand_id
    res = requests.get(url).json()
    ret = list()
    for entry in res:
        tmp = [entry['name'], entry['id']]
        ret.append(tmp)
    return ret


def search_shade(product_id):
    url = "http://findation.com/shades?product_id=" + product_id
    r = requests.get(url).json()
    res = list()
    for entry in r:
        tmp = [entry['name'], entry['id']]
        res.append(tmp)
    return res


def build_menu(buttons):
    menu = [buttons[i:i+1] for i in range(0, len(buttons), 1)]
    return menu


def get_keyboard_markup(l):
    button_list = list()

    for brand in l:
        button = telegram.InlineKeyboardButton(brand[0], callback_data=brand[1])
        button_list.append(button)

    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list))
    return reply_markup


def get_result(shade_id):
    url = "http://findation.com/searches"
    data = {'search[shade_ids][]': shade_id}
    res = dict()
    r = requests.post(url, data=data)
    # r.encode('utf-8')
    html = r.text
    counter = 0
    sel = etree.HTML(html)
    for product in sel.xpath("//*/a"):
        if product.find('div[1]/img') is not None:
            img = product.find('div[1]/img').get('src')
            brand = product.find('div[2]/h4').text
            brand = brand.replace("\xa0", " ")
            name = product.find('div[2]/p').text
            name = name.replace("\xa0", " ")
            shade = product.find('div[2]/p/strong').text
            shade = shade.replace("\xa0", " ")
            counter += 1
            if brand in res:
                tmp = {"shade": shade,
                       "img_url": img,
                       "name": name}
                res[brand].append(tmp)
            else:
                tmp = {"name": name,
                       "img_url": img,
                       "shade": shade}
                res[brand] = [tmp]
    return res


def result_generate(res_dict):
    res = list()
    # counter = 0
    for key, val in res_dict.items():
        res.append([key, key])
        # print(val)
        # res.append([key, val])
        # del res_dict[key]
        # counter += 1
        # if counter == 5:
        #     break

    # for item in res:
    #     res_dict.pop(item[0])

    # if len(res_dict) > 0:
    #     res.append(["More", "More"])
    #     # res.append(["More", res_dict])

    return res
