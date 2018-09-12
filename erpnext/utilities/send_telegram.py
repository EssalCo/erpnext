import requests


def send_msg_telegram(msg):
    bot_token = "610849820:AAGNJDomC3j7gF-XNxWEW9D23qYd8EiRzlg"
    chat_id = "-285634604"
    requests.post(
        "https://api.telegram.org/bot{0}/sendMessage?chat_id={1}".format(bot_token, chat_id),
        {"text": msg}
    )
    return