import requests
import frappe

def send_msg_telegram(msg):

    try:
        from frappe.utils import get_site_name
        try:
            msg = msg.decode('utf-8')
        except:
            msg = str(msg).decode('utf-8')
        site_name = get_site_name(frappe.local.request.host)
        bot_token = "610849820:AAGNJDomC3j7gF-XNxWEW9D23qYd8EiRzlg"
        chat_id = "-285634604"
        requests.post(
            "https://api.telegram.org/bot{0}/sendMessage?chat_id={1}".format(bot_token, chat_id),
            {
                "text": "Site: {0}\nAPI: {1}\nMessage: {2}".format(
                site_name,
                    frappe.request.path,
                msg
            )}
        )
    except:
        pass
    return