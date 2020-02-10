from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
import logging

from bot.constants import LEGIT_REPLIES, Category
from bot.utils import process_reply, get_answer, get_question, parse

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger()

TYPE, COLOR, CHECK_ANSWER = range(3)


def show_data(update, context):
    """Show data held on the user -- useful for debugging"""
    data = []
    for key, item in context.user_data.get("known", {}).items():
        data.append(f"{key}: {item}")
    update.message.reply_text("This is what I know:\n" + "\n".join(data))
    # Return none for state to not change
    return None


def start(update, context):
    update.message.reply_text(
        "Hi, I am a 20 questions bot! Nice to meet you.\n\n"
        "To start a new game type /newgame\n"
        "To stop talking to me type /cancel\n"
        "To see these instructions again, type /start\n"
    )


def ask_question(update, context, category):
    """Ask a question in a given category
    and persist the question object to user_data"""
    question_object = get_question(category, context.user_data["partial"])
    context.user_data["question_object"] = question_object
    update.message.reply_text(f"Is it {question_object}?")


def new_game(update, context):
    # Clear user data to start anew
    context.user_data["known"] = {}
    context.user_data["partial"] = {}

    # Start game with first question
    ask_question(update, context, Category.TYPE)
    return TYPE


def process_type(update, context):
    known, partial = process_reply(
        update.message.text, context.user_data, Category.TYPE
    )
    context.user_data["known"] = known
    context.user_data["partial"][Category.TYPE.value] = partial
    if Category.TYPE.value in known:
        ask_question(update, context, Category.COLOR)
        return COLOR
    else:
        ask_question(update, context, Category.COLOR)
        return TYPE


def process_color(update, context):
    known, partial = process_reply(
        update.message.text, context.user_data, Category.COLOR
    )
    context.user_data["known"] = known
    context.user_data["partial"][Category.COLOR.value] = partial
    if Category.COLOR.value in known:
        answer = get_answer(known)
        if answer == -1:
            update.message.reply_text("You cheated! This is not a valid item.")
            return ConversationHandler.END
        else:
            update.message.reply_text(f"Is it {answer}")
            return CHECK_ANSWER
    else:
        ask_question(update, context, Category.COLOR)
        return COLOR


def check_answer(update, context):
    if parse(update.message.text) is True:
        reaction = "Yay, I am a genius! If "
    else:
        reaction = "I am wrong, this should never have happened. But if "
    update.message.reply_text(reaction + "you want to play again, type /newgame")
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
