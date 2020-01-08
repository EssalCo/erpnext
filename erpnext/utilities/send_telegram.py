import requests
import frappe

def send_msg_telegram(msg):
    from frappe.utils import get_site_name
    site_name = get_site_name(frappe.local.request.host)
    bot_token = "610849820:AAGNJDomC3j7gF-XNxWEW9D23qYd8EiRzlg"
    chat_id = "-285634604"
    requests.post(
        "https://api.telegram.org/bot{0}/sendMessage?chat_id={1}".format(bot_token, chat_id),
        {
            "text": "Site: {0}\nMessage: {1}".format(
            site_name,
            msg.decode('utf-8')
        )}
    )
    return