from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

TYPE, COLOR = range(2)
YES_REPLIES = ['yes', 'yeah', 'yup', 'Yes', 'Yeah', 'Yup']
NO_REPLIES = ['no', 'nope', 'nah', 'No', 'Nope', 'Nah']
LEGIT_REPLIES = YES_REPLIES + NO_REPLIES

def get_reply(update):
    reply = update.message.text
    if reply in YES_REPLIES:
        return True
    return False

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
    

def unknown_message(update, context):
    update.message.reply_text("I am not a chat bot, reply yes or no only")
    # Return none for state to not change
    return None

def setup(updater):
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        states = {
            TYPE: [MessageHandler(Filters.text(LEGIT_REPLIES), process_type)], 
            COLOR: [MessageHandler(Filters.text(LEGIT_REPLIES), process_color)],
        },
        fallbacks=[CommandHandler('cancel', cancel), MessageHandler(Filters.text, unknown_message)],
        name="20qs",
        persistent=True
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

