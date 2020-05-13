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

# Keep lower case for optimal performnce
SUPPORTED_LANGUAGES = ('english', 'spanish')


@app.errorhandler(404)
def page_not_found(e):
    return json.dumps({"error": "not found"}), 404


@app.route('/')
def index():
    return json.dumps({"service": "translate",
                       "supported_langugages": SUPPORTED_LANGUAGES,
                       "version": os.getenv('TRANSLATE_API_VER')})


def validate(word):
    return ''.join(e for e in word if e.isalnum())


@app.route('/translate/<from_language>/<to_language>/<word>/', methods=["GET"])
def translate(from_language, to_language, word):
    try:
        rdb = redis_wrapper.new_redis_connection()
    except redis.exceptions.ConnectionError:
        return json.dumps({"error": "redis down"}), 500
    if not from_language.lower() in SUPPORTED_LANGUAGES:
        return json.dumps({"error": "invalid from language"}), 400
    if not to_language.lower() in SUPPORTED_LANGUAGES:
        return json.dumps({"error": "invalid to language"}), 400
    if not validate(word):
        return json.dumps({"error": "invalid input"}), 400
    key = [from_language.lower(),
           to_language.lower(),
           word.lower()]
    try:
        translation = rdb.get('-'.join(key))
    except (ConnectionError, TimeoutError) as redis_error:
        return json.dumps({"error": "redis server error, containd admin"}), 500
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
    if not from_language.lower() in SUPPORTED_LANGUAGES:
        return json.dumps({"error": "invalid from language"}), 400
    if not to_language.lower() in SUPPORTED_LANGUAGES:
        return json.dumps({"error": "invalid to language"}), 400
    if not validate(word):
        return json.dumps({"error": "invalid input"}), 400
    key = '-'.join([from_language.lower(),
                    to_language.lower(),
                    word.lower()])
    try:
        rdb.set(key, translation)
    except (ConnectionError, TimeoutError) as redis_error:
        return json.dumps({"error": "redis server error, containd admin"}), 500
    return json.dumps({"status": "success"})


@app.route('/translate/<from_language>/<to_language>/<word>/',
           methods=["DELETE"])
def delete(from_language, to_language, word):
    try:
        rdb = redis_wrapper.new_redis_connection()
    except redis.exceptions.ConnectionError:
        return json.dumps({"error": "redis down"}), 500
    if not from_language.lower() in SUPPORTED_LANGUAGES:
        return json.dumps({"error": "invalid from language"}), 400
    if not to_language.lower() in SUPPORTED_LANGUAGES:
        return json.dumps({"error": "invalid to language"}), 400
    key = '-'.join([from_language.lower(),
                    to_language.lower(),
                    word.lower()])
    try:
        rdb.delete(key)
    except (ConnectionError, TimeoutError) as redis_error:
        return json.dumps({"error": "redis server error, containd admin"}), 500
    return json.dumps({"status": "success"})
