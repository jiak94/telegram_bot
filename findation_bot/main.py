from telegram.ext import *
import command

if __name__ == "__main__":
    updater = Updater(token='')
    dispatcher = updater.dispatcher

    search_handler = CommandHandler('search', command.search, pass_args=True)
    # search_callback_handler = CallbackQueryHandler(command.callback_search)

    product_callback_handler = CallbackQueryHandler(command.callback_product)

    shade_callback_handler = CallbackQueryHandler(command.callback_shade)

    result_callback_handler = CallbackQueryHandler(command.callback_result,
                                                   pass_user_data=True)
    detail_callback_handler = CallbackQueryHandler(command.callback_detail,
                                                   pass_user_data=True)
    # dispatcher.add_handler(search_handler)
    # dispatcher.add_handler(search_callback)

    conversation_handler = ConversationHandler(
        entry_points=[search_handler],
        states={
            "product":[product_callback_handler],
            "shade": [shade_callback_handler],
            "detail": [detail_callback_handler],
            "result": [result_callback_handler]
        },
        fallbacks = [search_handler]
    )

    dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()
