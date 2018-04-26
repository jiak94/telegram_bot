import utils
import json
import telegram

def search(bot, update, args):
    if len(args) != 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Try /search ysl")
        return -1
    markup = utils.get_keyboard_markup(utils.search_brand(args[0]))

    if len(markup['inline_keyboard']) == 0:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Sorry, we currently don't have your brand in the database")
        return -1
    elif len(markup['inline_keyboard']) == 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Are you looking for this brand?",
                         reply_markup=markup)
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Are you looking for these brands?",
                         reply_markup=markup)

    return "product"

def callback_product(bot, update):
    markup = utils.get_keyboard_markup(utils.search_product(update.callback_query.data))

    if len(markup['inline_keyboard']) == 0:
        bot.send_message(chat_id=update.callback_query.message.chat_id,
                         text="Sorry, we currently don't have your brand in the database")
        return -1

    bot.send_message(chat_id=update.callback_query.message.chat_id,
                     text="Which product are you looking for?",
                     reply_markup=markup)

    return "shade"


def callback_shade(bot, update):
    markup = utils.get_keyboard_markup(utils.search_shade(update.callback_query.data))

    if len(markup['inline_keyboard']) == 0:
        bot.send_message(chat_id=update.callback_query.message.chat_id,
                         text="Sorry, we currently don't have your brand in the database")
        return -1

    bot.send_message(chat_id=update.callback_query.message.chat_id,
                     text="Which shade are you looking for?",
                     reply_markup=markup)
    return "result"

def callback_result(bot, update, user_data):
    shade_id = update.callback_query.data
    res_dict = utils.get_result(shade_id)
    keys = list(user_data.keys())

    # empty the user_data because it's new search
    for key in keys:
        del user_data[key]

    for key, val in res_dict.items():
        user_data[key] = val

    if len(res_dict) < 1:
        bot.send_message(chat_id=update.callback_query.message.chat_id,
                         text="Sorry, we currently can't find the product meet your requirement.")
        return -1

    converted = utils.result_generate(res_dict)
    # counter = 0
    # for item in converted:
    #     try:
    #         user_data[item[0]] = res_dict[item[0]]
    #         counter += 1
    #     except:
    #         user_data[item[0]] = counter+1

    markup = utils.get_keyboard_markup(converted)
    bot.send_message(chat_id=update.callback_query.message.chat_id,
                     text="Here are some products fit you!",
                     reply_markup=markup)

    return "detail"


def callback_detail(bot, update, user_data):
    print(user_data)

    brand_name = update.callback_query.data

    res_dict = user_data[brand_name]
    # res_dict = json.loads(update.callback_query.data)

    if type(res_dict) is list:
        for item in res_dict:
            text = "*" + item['name'] + "*\nshade: \n_" + item['shade'] + "_"
            bot.send_message(chat_id=update.callback_query.message.chat_id,
                            text=text,
                             parse_mode=telegram.ParseMode.MARKDOWN)
            # bot.send_photo(chat_id=update.callback_query.message.chat_id,
            #             photo=item['img_url'])
        return

    # converted, chat_data = utils.result_generate(user_data["More"])
    # user_data = chat_data
    markup = utils.get_keyboard_markup(utils.result_generate(res_dict))
    bot.send_message(chat_id=update.callback_query.message.chat_id,
                    text="Here are some products fit you!",
                    reply_markup=markup)

    return "detail"
