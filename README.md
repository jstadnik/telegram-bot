# telegram-bot
Simple implementation of telegram-bot-based 20 Questions game using python.  
Current master implementation can be chatted to at Joanna20QsBot (hosted on AWS EC2) 

The **stable** but inefficient version of the app is on master. 

An experimental branch, which should always arrive at one of the answers and not ask pointless questions, is on branch combine-question-stages. It has not been tested as extensively and the comments are not very good. Note, this is not the _minimum_ number of questions -- that would likely consist of, at every stage, eliminating as many options as possible, which would be halving it as much as possible (same logic as splitting things in half in the divide and conquer algorithm) -- so always asking about type first, as on the master branch implementation, is actually quite a good strategy.

The add-my-py-type-checking branch is a stab at adding python type checking to the master code.

## Test locally

To run locally, clone repository; then with python 3.6+ run
```
pip install -r requirements.txt
```
You then have two options:

1) Enter token by creating file

Create a file `bot/token.py` with contents
```
TOKEN = <your_secret_bot_token>
```
Then run
```
python start_bot.py
```

2) Pass token as argument  
```
python start_bot.py --token <your_secret_bot_token>
```

## Deploy to prod
Use `build_prod_zip.sh` to create a handy zip bundle of only the files important for deploying.

## "Contribute"
Get the dev requirements by running
```
pip install -r dev_requirements.txt
```
Run `clean.sh` to clean up code before committing.

## Future development
 - Don't keep asking questions when answer can already be inferred
 - Add a proper deploy pipeline
 - Improve flow of conversation, accept all the answers _containing_ "yes", "Nah", etc
 - Design a "least questions" algorithm
 - Add better tests
 - Add mypy type checking
