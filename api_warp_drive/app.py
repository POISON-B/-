#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import jsonify


from config_load import config_dict
from app import create_app

app = create_app()


@app.route("/", methods=['GET'])
def get_root():
    return jsonify({'result': 'Hello World!'})


if __name__ == "__main__":
    app.run(
        host=config_dict['listen'],
        port=config_dict['port'],
        debug=config_dict['debug']
    )
