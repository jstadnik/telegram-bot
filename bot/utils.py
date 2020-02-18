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
    reply_value = parse(reply)
    question_category = Category(user_data["question_category"])
    question_object = user_data["question_object"]

    # Save the user reply as is
    if not question_category.value in user_data["partial"]:
        user_data["partial"][question_category.value] = {}
    user_data["partial"][question_category.value][question_object] = reply_value

    # Check if value is now known
    if reply_value is True:
        # Only one value can describe the item in a given category
        # So if the user answered "yes", then we know this category
        # is equal to the question object
        user_data["known"][question_category.value] = question_object
    check_if_anything_known(user_data)
    # Retruning anything for debugging purposes, really
    return user_data["known"], user_data["partial"]


def get_column_values(col):
    """
    Get all the distinct values in a given column of a csv file
    """
    all_values = set()
    with open(FILEPATH) as f:
        csv_reader = csv.reader(f, delimiter=",")
        lc = -1
        for row in csv_reader:
            lc += 1
            if lc == 0:
                # Ignore the first line, it's titles, not values
                continue
            all_values.add(row[col])
    return all_values


def get_choices(category):
    """Return possible options given the category of the question"""
    return get_column_values(category.col())

def check_if_anything_known(user_data):
    get_possible_choices_for_question(user_data)

def get_possible_choices_for_question(user_data):
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
    category = random.choice(list(all_options.keys()))
    return category, random.choice(list(all_options[category]))


def get_answer(known):
    """
    Return item that matches on all three fields,
    or indicate item as described does not exist
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
