from flask import Flask, abort
import logging
import json
import os
import redis

from src import redis_wrapper

app = Flask(__name__)

FORMATTER = logging.Formatter('%(asctime)s - %(name)s - '
                              '%(levelname)s - %(message)s')
# console handler
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.INFO)
CONSOLE_HANDLER.setFormatter(FORMATTER)
log = logging.getLogger(__name__)
log.addHandler(CONSOLE_HANDLER)
log.setLevel(logging.INFO)


@app.route('/')
def index():
    return json.dumps({"service": "translate",
                       "version": os.getenv('TRANSLATE_API_VER')})


@app.route('/translate/<from_language>/<to_language>/<word>/', methods=["GET"])
def translate(from_language, to_language, word):
    try:
        rdb = redis_wrapper.new_redis_connection()
    except redis.exceptions.ConnectionError:
        return json.dumps({"error": "redis down"}), 500
    key = [from_language.lower(),
           to_language.lower(),
           word.lower()]
    translation = rdb.get('-'.join(key))
    if not translation:
        abort(404)
    try:
        return json.dumps({"translation": translation.decode("utf-8")})
    except Exception as translate_error:
        return json.dumps({"error": str(translate_error)}), 500


@app.route('/translate/<from_language>/<to_language>/<word>/<translation>/',
           methods=["POST"])
def add(from_language, to_language, word, translation):
    try:
        rdb = redis_wrapper.new_redis_connection()
    except redis.exceptions.ConnectionError:
        return json.dumps({"error": "redis down"}), 500
    key = '-'.join([from_language.lower(),
                    to_language.lower(),
                    word.lower()])
    rdb.set(key, translation)
    return json.dumps({"status": "success"})


@app.route('/translate/<from_language>/<to_language>/<word>/',
           methods=["DELETE"])
def delete(from_language, to_language, word):
    try:
        rdb = redis_wrapper.new_redis_connection()
    except redis.exceptions.ConnectionError:
        return json.dumps({"error": "redis down"}), 500
    key = '-'.join([from_language.lower(),
                    to_language.lower(),
                    word.lower()])
    rdb.delete(key)
    return json.dumps({"status": "success"})
