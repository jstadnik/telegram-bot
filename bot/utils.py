import random
import csv
from bot.constants import YES_REPLIES, NO_REPLIES, FILEPATH, Category


def parse(reply):
    if reply in YES_REPLIES:
        return True
    elif reply in NO_REPLIES:
        return False
    # TODO: Add handling for rogue response
    # Shouldn't really happen as only replies in YES_REPLIES and NO_REPLIES
    # Are allowed through by the ConversationHandler
    return False


def process_reply(reply, user_data):
    """
    This is where all the magic happens. Record the reply,
    then check what we know based on the new information,
    and update the user data accordingly
    """
    reply_value = parse(reply)
    question_category = Category(user_data["question_category"])
    question_object = user_data["question_object"]

    # Save the user reply as is
    if question_category.value not in user_data["partial"]:
        user_data["partial"][question_category.value] = {}
    user_data["partial"][question_category.value][question_object] = reply_value

    # Check if value is now known
    if reply_value is True:
        # Only one value can describe the item in a given category
        # So if the user answered "yes", then we know this category
        # is equal to the question object
        user_data["known"][question_category.value] = question_object

    last_len_known = -1
    while last_len_known != len(user_data["known"]):
        # Check for known values until the check does not discover anything new
        last_len_known = len(user_data["known"])
        check_if_anything_known(user_data)

    # Retruning for testing purposes only, as dicts changed in place
    return user_data["known"], user_data["partial"]


def check_if_anything_known(user_data):
    get_possible_choices_for_question(user_data)


def get_possible_choices_for_question(user_data):
    """
    Go through the CSV file and populate all the categories with the possibilities
    still left, given the current data. Also automatically updates the "known" section,
    if there is only one choice left. This is why this doubles as a helper fuction both
    for obtaining the next question, as well as processing the information after
    a user's reply.
    """
    known = user_data["known"]
    partial = user_data["partial"]
    categories_not_known = []
    for category in Category:
        if category is not Category.ITEM and category.value not in known.keys():
            categories_not_known.append(category)

    all_options = {}
    for category in categories_not_known:
        all_options[category.value] = set()

    with open(FILEPATH) as f:
        csv_reader = csv.reader(f, delimiter=",")
        lc = -1
        for row in csv_reader:
            lc += 1
            if lc == 0:
                # Ignore the first line, it's titles, not values
                continue
            if all(row[Category(cat).col()] == val for cat, val in known.items()):
                for category in categories_not_known:
                    all_options[category.value].add(row[category.col()])

    for category_in_partial in partial.keys():
        if category_in_partial in all_options:
            for key in partial[category_in_partial]:
                # This has already been asked
                try:
                    all_options[category_in_partial].remove(key)
                except KeyError:
                    # This was asked, but is no longer an option anyway
                    pass

    to_del = []
    for cat, options in all_options.items():
        if len(options) == 1:
            user_data["known"][cat] = options.pop()
            to_del.append(cat)
        elif len(options) == 0:
            to_del.append(cat)
    for cat in to_del:
        del all_options[cat]

    return all_options


def get_question(user_data):
    """
    Make the game more interesting by randomizing the order of asking questions.
    Collect the possible values, and filter out those already asked, which are present
    in the "partial".
    """
    all_options = get_possible_choices_for_question(user_data)
    if len(all_options) == 0:
        return None, None
    category = random.choice(list(all_options.keys()))
    return category, random.choice(list(all_options[category]))


def get_answer(known):
    """
    Return item that matches on all the existing fields,
    if there is only one such item
    """
    matching_items = []
    with open(FILEPATH) as f:
        csv_reader = csv.reader(f, delimiter=",")
        for row in csv_reader:
            if all(row[Category(cat).col()] == val for cat, val in known.items()):
                matching_items.append(row[Category.ITEM.col()])
    if len(matching_items) == 1:
        return matching_items[0]
    return None


def get_items():
    """
    Return all the possible items listed in the csv file
    """
    items = set()
    with open(FILEPATH) as f:
        csv_reader = csv.reader(f, delimiter=",")
        lc = -1
        for row in csv_reader:
            lc += 1
            if lc == 0:
                # Ignore the first line, it's titles, not values
                continue
            items.add(row[Category.ITEM.col()])
    return items
