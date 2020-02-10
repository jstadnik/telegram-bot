from enum import Enum

YES_REPLIES = ["yes", "yeah", "yup", "Yes", "Yeah", "Yup"]
NO_REPLIES = ["no", "nope", "nah", "No", "Nope", "Nah"]
LEGIT_REPLIES = YES_REPLIES + NO_REPLIES
FILEPATH = "data.csv"

class Category(Enum):
    TYPE = "Type"
    COLOR = "Colour"
    SIZE = "Size"
