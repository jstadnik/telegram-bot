from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
import logging

from bot.constants import LEGIT_REPLIES, Category
from bot.utils import process_reply, get_answer, get_question, parse, get_choices

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger()

TYPE, COLOR, SIZE, CHECK_ANSWER = range(4)


def show_data(update, context):
    """Show data held on the user -- useful for debugging"""
    data = []
    for key, item in context.user_data.get("known", {}).items():
        data.append(f"{key}: {item}")
    update.message.reply_text("This is what I know:\n" + "\n".join(data))
    # Return none for state to not change
    return None


def start(update, context):
    reply_text = "Hi, I am a 20 questions bot! Nice to meet you.\n\n"
    reply_text += "You can choose from the following items:\n\n"
    reply_text += "\n".join(list(get_choices(Category.ITEM)))
    reply_text += "\n\nTo start a new game, type /newgame\n"
    reply_text += "To stop talking to me, type /cancel\n"
    reply_text += "To see these instructions again, type /start"
    update.message.reply_text(reply_text)


def ask_question(update, context, category):
    """
    Ask a question in a given category and persist the question object to user_data.
    The question object indicates what the user answered yes/no to.
    """
    question_object = get_question(category, context.user_data["partial"])
    context.user_data["question_object"] = question_object
    update.message.reply_text(f"Is it {question_object.lower()}?")


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
        # We now know the type, so proceed to colour
        ask_question(update, context, Category.COLOR)
        return COLOR
    else:
        # There's only two type options so this
        # path should never get exacuted with data as is
        ask_question(update, context, Category.TYPE)
        return TYPE


def process_color(update, context):
    known, partial = process_reply(
        update.message.text, context.user_data, Category.COLOR
    )
    context.user_data["known"] = known
    context.user_data["partial"][Category.COLOR.value] = partial
    if Category.COLOR.value in known:
        # We know the colour so proceed to size
        ask_question(update, context, Category.SIZE)
        return SIZE
    else:
        # Still unsure about colour so keep asking
        ask_question(update, context, Category.COLOR)
        return COLOR


def process_size(update, context):
    known, partial = process_reply(
        update.message.text, context.user_data, Category.SIZE
    )
    context.user_data["known"] = known
    context.user_data["partial"][Category.SIZE.value] = partial
    if Category.SIZE.value in known:
        # Size is the last stage, so if we know the size,
        # we know everything and can proceed to fetching the answer
        answer = get_answer(known)
        if answer == -1:
            update.message.reply_text(
                "You cheated! This is not a valid item. Game over."
            )
            return ConversationHandler.END
        else:
            update.message.reply_text(f"Is it {answer.lower()}?")
            return CHECK_ANSWER
    else:
        ask_question(update, context, Category.SIZE)
        return SIZE


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
        "I seem to have gotten myself into a state... "
        "Don't worry, the error will DEFINITELY be looked into by someone.\n\n"
        "Looks like you'll have to start a new game in the mean time, though, sorry :("
    )
    logger.warning(f"Update {update} caused error {context.error}")
    return ConversationHandler.END


def setup(updater):
    """
    ConversationHandler based implementation.

    Each game has a rigid state progression. At each step the game either:
    stays in the same state, if it hasn't figured out the answer to that category
    proceeds to next state, when it has
    Additionally
    /newgame discards any game progress and resets state to TYPE
    /cancel exits the conversation flow completely
    The stages are as follows:
    TYPE - getting the type of the object
    COLOR - getting the color of the object
    SIZE - getting the size of the object
    CHECK_ANSWER - confirming the validity of the answer and exit game

    The updater is equipped with a "persistent" dictionary-state of the form:
    question_object: string -- last thing the bot asked about
    known: Dict -- keys of each category are added at the completion of a stage,
            e.g. "Colour: Green", when the COLOR stage is completed.
            Example (at the answer stage):
            known = {
                "Type": "Animal",
                "Colour": "Brown"
                "Size": "Small"
            }
    partial: Dict of Dicts -- records user replies naively,
            used to keep track of questions asked during each stage,
            to avoid repeating the same questions.
            Example (halfway through the COLOR stage):
            partial = {
                "Type": {"Animal": True},
                "Colour": {"Green": False}
            }
            Tells us it's an animal that is not green.
    After a few more questions in the color stage,
    we should have a user_data looking something like this:
    >>> {
        "question_object": "Orange",
        "known": {"Type": "Animal", "Colour": "Brown"},
        "partial": {
            "Type": {"Animal": True},
            "Colour": {"Green": False, "Grey": False, "Orange": False}
        }
    }
    The above tells us the last question the bot asked was
    "Is it orange?" (from question_object)
    To which the user replied negatively.

    Earlier, the user also answered positively to "Is it animal?",
    And negatively to "Is it green?" and "Is it grey?". (from partial)

    Since it's not green, grey or orange, it must be brown,
    which the program inferred. (as recorded in known)
    """
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("newgame", new_game)],
        states={
            TYPE: [MessageHandler(Filters.text(LEGIT_REPLIES), process_type)],
            COLOR: [MessageHandler(Filters.text(LEGIT_REPLIES), process_color)],
            SIZE: [MessageHandler(Filters.text(LEGIT_REPLIES), process_size)],
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
