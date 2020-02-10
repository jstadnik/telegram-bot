from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--token",
        type=str,
        help="If not passed, the token stored in bot/token.py will be used.",
    )
    args = parser.parse_args()
    token = args.token
    if token is None:
        try:
            from bot.token import TOKEN

            token = TOKEN
        except ImportError:
            print(
                "The secret token must be specified either in the bot/token.py "
                "file or passed as an argument"
            )

    if token:
        from telegram.ext import (
            Updater,
            DictPersistence,
        )
        from bot.handlers import setup

        per = DictPersistence()
        updater = Updater(token=token, persistence=per, use_context=True)
        setup(updater)
