import requests
import os

discord_webhook_test = os.environ.get("discord_webhook_test")
discord_webhook_stats = os.environ.get("discord_webhook_stats")


def msg_discord_test(message, bot_name):
    data = {
        "content": message,
        "username": bot_name,
    }

    response = requests.post(discord_webhook_test, json=data)

    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print(
            f"Failed to send message. Status code: {response.status_code}, response: {response.text}"
        )


def msg_discord_stats(message, bot_name):
    data = {
        "content": message,
        "username": bot_name,
    }

    response = requests.post(discord_webhook_stats, json=data)

    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print(
            f"Failed to send message. Status code: {response.status_code}, response: {response.text}"
        )
