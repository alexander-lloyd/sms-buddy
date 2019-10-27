import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from twilio.twiml.messaging_response import MessagingResponse


# Emoji is hugging emoji
YOURE_ALL_SIGNED_UP = 'Hey {name}! You are all signed up! \U0001F917'

configs = {
  'development': 'config/development.py',
  'production': 'config/production.py'
}


def get_config(config_name):
    print(config_name, configs[config_name])
    return configs[config_name]


config_type = os.getenv('CONFIG_TYPE', 'production')

app = Flask(__name__)
app.config.from_pyfile(get_config(config_type))
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/new-user', methods=['POST'])
def new_user():
    from_number = request.vallues.get('From', None)
    name = request.values.get('Body', None)

    u = User(phone_number=from_number, name=name)
    db.session.add(u)
    try:
        db.session.commit()
    except Exception as e:
        app.logger.exception(e)
        db.session.rollback()
    resp = MessagingResponse()
    resp.message(YOURE_ALL_SIGNED_UP.format(name=name))

    return str(resp)


if __name__ == '__main__':
    app.run()
