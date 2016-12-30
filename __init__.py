from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    message = os.environ.get('MESSAGE', 'Hello World!')
    return message


if __name__ == '__main__':
    app.run(host='0.0.0.0')
