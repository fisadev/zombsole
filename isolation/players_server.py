#!/usr/bin/python
# coding: utf-8
'''Serve the players logic as a http service.'''
from flask import Flask


app = Flask('zombsole_isolator')


@app.route('/')
def index():
    return 'ok'


app.run('0.0.0.0', 8000)
