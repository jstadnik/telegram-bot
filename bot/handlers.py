from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger()

TYPE, COLOR, CHECK_ANSWER = range(3)
YES_REPLIES = ["yes", "yeah", "yup", "Yes", "Yeah", "Yup"]
NO_REPLIES = ["no", "nope", "nah", "No", "Nope", "Nah"]
LEGIT_REPLIES = YES_REPLIES + NO_REPLIES


def show_data(update, context):
    """Show data held on the user -- useful for debugging"""
    data = []
    for key, item in context.user_data.get("known", {}).items():
        data.append(f"{key}: {item}")
    update.message.reply_text("This is what I know:\n" + "\n".join(data))


def get_reply(update):
    reply = update.message.text
    if reply in YES_REPLIES:
        return True
    return False


def start(update, context):
    update.message.reply_text(
        "Hi, I am a 20 questions bot! Nice to meet you.\n\n"
        "To start a new game type /newgame\n"
        "To stop talking to me type /cancel\n"
        "To see these instructions again, type /start\n"
    )


def new_game(update, context):
    context.user_data["known"] = {}
    update.message.reply_text("Is it an animal?")
    return TYPE


def process_type(update, context):
    context.user_data["known"]["animal"] = get_reply(update)
    update.message.reply_text("Is it brown?")
    return COLOR


def process_color(update, context):
    brown = get_reply(update)
    animal = context.user_data["known"]["animal"]
    if brown:
        if animal:
            answer = "horse"
        else:
            answer = "table"
    else:
        if animal:
            answer = "frog"
        else:
            answer = "pencil"
    update.message.reply_text(f"Is it {answer}?")
    return CHECK_ANSWER


def check_answer(update, context):
    if get_reply(update) is True:
        reaction = "Yay, I am a genius! "
    else:
        reaction = "This should never have happened. "
    update.message.reply_text(reaction + "If you want to play again, type /newgame")
    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text("'till next!")
    return ConversationHandler.END


def unknown_message(update, context):
    update.message.reply_text("I am not a chat bot, reply yes or no only")
    # Return none for state to not change
    return None


def error(update, context):
    update.message.reply_text(
        "I seem to have gotten myself into a state..."
        "Don't worry, the error will DEFINITELY be looked into by someone.\n\n"
        "Looks like you'll have to start a new game in the mean time, though, sorry :("
    )
    logger.warning(f"Update {update} caused error {context.error}")
    return ConversationHandler.END


def setup(updater):
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("newgame", new_game)],
        states={
            TYPE: [MessageHandler(Filters.text(LEGIT_REPLIES), process_type)],
            COLOR: [MessageHandler(Filters.text(LEGIT_REPLIES), process_color)],
            CHECK_ANSWER: [MessageHandler(Filters.text(LEGIT_REPLIES), check_answer)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("newgame", new_game),
            CommandHandler("show", show_data),
            MessageHandler(Filters.text, unknown_message),
        ],
        name="20qs",
        persistent=True,
    )

    start_handler = CommandHandler("start", start)

    dp.add_handler(conv_handler)
    dp.add_handler(start_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
