from bot.constants import YES_REPLIES, NO_REPLIES


def process_reply(reply):
    if reply in YES_REPLIES:
        return True
    elif reply in NO_REPLIES:
        return False
    # TODO: Add handling for rogue response
    return False


def get_answer(data):
    is_animal = data["animal"]
    is_brown = data["brown"]
    if is_animal:
        if is_brown:
            return "horse"
        else:
            return "frog"
    else:
        if is_brown:
            return "table"
        else:
            return "pencil"
