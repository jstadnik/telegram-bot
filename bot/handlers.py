from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

TYPE, COLOR = range(2)
YES_NO_DICT = {
    'yes': True,
    'no': False,
}

def get_reply(update):
    return YES_NO_DICT[update.message.text.lower()]

def start(update, context):
    update.message.reply_text("Hi, you want to play a game")
    update.message.reply_text("Is it an animal?")
    return TYPE

def process_type(update, context):
    context.user_data['animal'] = get_reply(update)
    update.message.reply_text("Is it brown?")
    return COLOR

def process_color(update, context):
    brown = get_reply(update)
    animal = context.user_data['animal']
    if brown:
        if animal:
            answer = 'horse'
        else:
            answer = 'table'
    else:
        if animal:
            answer = 'frog'
        else:
            answer = 'pencil'
    update.message.reply_text(f"Is it {answer}?")
    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text("Till next!")
    return ConversationHandler.END
    

def setup(updater):
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        states = {
            TYPE: [MessageHandler(Filters.regex('^(yes|no)$'), process_type)], 
            COLOR: [MessageHandler(Filters.regex('^(yes|no)$'), process_color)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        name="20qs",
        persistent=True
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

