import os
import random

from twilio.rest import Client

from app import User


QUOTES = open('quotes.txt').read().split('\n')[0:-1]  # Last is an empty line.
NUMBER_QUOTES = len(QUOTES)
MESSAGE_FORMAT = 'Hey {name}! Here\'s your daily motivational quote: {quote}'
FROM_NUMBER = ''
ACCOUNT_SID = os.environ['ACCOUNT_SID']
AUTH_TOKEN = os.environ['AUTH_TOKEN']
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_message(from_number, to_number, message):
    return Client.messages.create(
      body=message,
      from_=from_number,
      to=to_number
    )


def send_messages():
    users = User.query.all()

    for user in users:
        name = user.name
        number = user.phone_number
        quote_number = random.randint(0, NUMBER_QUOTES)
        quote = QUOTES[quote_number]
        send_message(FROM_NUMBER, number, MESSAGE_FORMAT.format(
            name=name,
            quote=quote
        ))


if __name__ == '__main__':
    send_messages()
