from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler
from sm import SmBot


def start(update, context):
    context.chat_data['smbot'] = SmBot()
    return choose_product(update, context)


def choose_product(update, context):
    options = context.chat_data['smbot'].get_dialogs()
    i = 0
    reply_keyboard = []
    while options[i:i + 3]:
        reply_keyboard.append([InlineKeyboardButton(opt, callback_data=opt) for opt in options[i:i + 3]])
        i += 3
    markup = InlineKeyboardMarkup(reply_keyboard)
    context.bot.send_message(update.effective_chat.id, "Что бы вы хотели заказать?",
                             reply_markup=markup)
    return 1


def new_order(update, context):
    query = update.callback_query
    choice = query.data
    query.answer()
    context.chat_data['smbot'].set_dialog(choice)
    return next(update, context)


def next(update, context):
    query = update.callback_query
    choice = query.data
    query.answer()
    if choice == 'Сделать еще один заказ':
        return choose_product(update, context)
    elif choice == 'До свидания!':
        context.bot.send_message(update.effective_chat.id, 'Всего доброго! Приходите еще!')
        stop(update, context)
    else:
        context.chat_data['smbot'].next(choice)
        data = context.chat_data['smbot'].data
        reply_keyboard = [[InlineKeyboardButton(opt, callback_data=opt) for opt in data['buttons']]]
        markup = InlineKeyboardMarkup(reply_keyboard)
        context.bot.send_message(update.effective_chat.id, data['message'],
                                 reply_markup=markup)
        return 2


def stop(update, context):
    return ConversationHandler.END


if __name__ == '__main__':
    TOKEN = '1797783540:AAFPXzqG6tbfgAWPPF6tQ0j05X7UJ10iAqE'
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [CallbackQueryHandler(new_order)],
            2: [CallbackQueryHandler(next)]
        },
        allow_reentry=True,
        fallbacks=[CommandHandler('stop', stop)]
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()
