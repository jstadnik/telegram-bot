#!/bin/bash

black start_bot.py
black bot/
flake8 start_bot.py
flake8 bot/
