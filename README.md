# telegram-bot
Simple implementation of telegram-bot-based 20 Questions game using python.  
Current master implementation can be chatted to at Joanna20QsBot (hosted on AWS EC2)  
All `.git` etc dirs on branch `all-inclusive`  

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
