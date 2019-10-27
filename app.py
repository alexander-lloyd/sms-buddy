import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from twilio.twiml.messaging_response import MessagingResponse


# Emoji is hugging emoji
YOURE_ALL_SIGNED_UP = 'Hey {name}! You are all signed up! \U0001F917.' \
                      ' To unsubscribe reply \'Unsubscribe\''
UNSUBSCRIBED_MESSAGE = 'Sorry to see you go \U0001F641'
ALREADY_SIGNED_UP = 'Hey {name}, you\' already signed up!'
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
    resp = MessagingResponse()

    user_exists = User.query.filter_by(phone_number=from_number).first()
    if user_exists:
        if name.strip().lower() == 'unsubscribe':
            # remove user from DB
            db.session.remove(user_exists)
            resp.message = UNSUBSCRIBED_MESSAGE
        else:
            name = user_exists.name
            resp.message = ALREADY_SIGNED_UP.format(name=name)
    else:
        u = User(phone_number=from_number, name=name)
        db.session.add(u)
        resp.message(YOURE_ALL_SIGNED_UP.format(name=name))

    try:
        db.session.commit()
    except Exception as e:
        app.logger.exception(e)
        db.session.rollback()

    return str(resp)


if __name__ == '__main__':
    app.run()
