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


def process_reply(reply, user_data, category):
    reply_value = parse(reply)
    known = user_data["known"]
    partial = user_data["partial"].get(category.value, {})
    question_object = user_data["question_object"]
    partial[question_object] = reply_value
    if reply_value is True:
        # Only one value can describe the item in a given category
        # So if the user answered "yes", then we know this category
        # is equal to the question object
        known[category.value] = question_object
    else:
        available_choices = get_choices(category)
        if len(partial.keys()) == len(available_choices) - 1:
            # All the other answers are negative so it must be this one
            last_one_left = (available_choices - set(partial.keys())).pop()
            known[category.value] = last_one_left
    return known, partial


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


def get_question(category, partial):
    """
    Make the game more interesting by randomizing the order of asking questions.
    Collect the possible values, and filter out those already asked, which are present
    in the "partial".
    """
    available_choices = get_choices(category)
    if category.value in partial:
        for key in partial[category.value].keys():
            # This has already been asked
            available_choices.remove(key)
    return random.choice(list(available_choices))


def get_answer(known):
    """
    Return item that matches on all three fields,
    or indicate item as described does not exist
    """
    with open(FILEPATH) as f:
        csv_reader = csv.reader(f, delimiter=",")
        for row in csv_reader:
            if (
                row[Category.TYPE.col()] == known[Category.TYPE.value]
                and row[Category.COLOR.col()] == known[Category.COLOR.value]
                and row[Category.SIZE.col()] == known[Category.SIZE.value]
            ):
                return row[0]
    return -1
