#!/bin/bash

black start_bot.py
black bot/
black tests/
flake8 start_bot.py
flake8 bot/
flake8 tests/
