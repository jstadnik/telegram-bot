from enum import Enum

YES_REPLIES = ["yes", "yeah", "yup", "Yes", "Yeah", "Yup"]
NO_REPLIES = ["no", "nope", "nah", "No", "Nope", "Nah"]
LEGIT_REPLIES = YES_REPLIES + NO_REPLIES
FILEPATH = "data/data.csv"


class Category(Enum):
    ITEM = "Item"
    TYPE = "Type"
    COLOR = "Colour"
    SIZE = "Size"

    def col(self):
        if self == self.ITEM:
            return 0
        elif self == self.TYPE:
            return 1
        elif self == self.COLOR:
            return 2
        else:
            return 3
