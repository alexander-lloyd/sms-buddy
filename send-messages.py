import os
import random

from twilio.rest import Client

from app import User


QUOTES = open('quotes.txt').read().split('\n')[0:-1]  # Last is an empty line.
NUMBER_QUOTES = len(QUOTES)
QUOTE_FORMAT = 'Hey {name}! Here\'s your daily motivational quote: {quote}'

CHALLENGE_PROBABILIIY = 5
CHALLENGES = open('challenges.txt').read().split('\n')[0:-1]
NUMBER_CHALLENGES = len(CHALLENGES)
CHALL_FORMAT = 'Hey {name}! Today, we challenge yourself today: {challenge}'

FROM_NUMBER = os.environ['PHONE_NUMBER']
ACCOUNT_SID = os.environ['ACCOUNT_SID']
AUTH_TOKEN = os.environ['ACCOUNT_TOKEN']
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_message(from_number, to_number, message):
    return CLIENT.messages.create(
      body=message,
      from_=from_number,
      to=to_number
    )


def send_messages():
    users = User.query.all()

    for user in users:
        name = user.name
        number = user.phone_number
        quote_or_challenge = random.randint(0, CHALLENGE_PROBABILIIY)
        if quote_or_challenge:
            quote_number = random.randint(0, NUMBER_QUOTES)
            quote = QUOTES[quote_number]
            message = QUOTE_FORMAT.format(name=name, quote=quote)
        else:
            challenge_number = random.randint(0, NUMBER_CHALLENGES)
            challenge = CHALLENGES[challenge_number]
            message = CHALL_FORMAT.format(name=name, challenge=challenge)
        send_message(FROM_NUMBER, number, message)


if __name__ == '__main__':
    send_messages()
