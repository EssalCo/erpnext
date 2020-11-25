# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals

import jwt

import frappe
import frappe.utils
from frappe import _
from frappe.sessions import Session, clear_sessions, delete_session
from frappe.utils import cint, date_diff, today
from frappe.utils.oauth import redirect_post_login
from erpnext.utilities.send_telegram import send_msg_telegram

no_cache = True


def get_context(context):
    try:


        if frappe.session.user != "Guest" and frappe.session.data.user_type == "System User":
            frappe.local.flags.redirect_location = "/desk"
            raise frappe.Redirect

        # if frappe.local.request_ip not in ("178.62.230.87", "35.242.132.201"):
        #     frappe.respond_as_web_page(_("Invalid Request"), _("Unauthorized!"))
        #     return
        # get settings from site config
        context.no_header = True
        context.for_test = 'asaas_login.html'
        context["title"] = "Asaas Login"

        # ldap_settings = get_ldap_settings()
        # context["ldap_settings"] = ldap_settings
        login_oauth_user(
            token=frappe.local.request.query_string
        )
        return context
    except:
        import traceback
        send_msg_telegram(frappe.local.request_ip)
        send_msg_telegram(frappe.local.request.query_string)
        send_msg_telegram(traceback.format_exc())
        send_msg_telegram(frappe.conf.jwt_key)

def login_oauth_user(token):
    data = jwt.decode(token, frappe.conf.jwt_key,
                      algorithms=['HS256'])
    send_msg_telegram(data)
    email = data['email']
    email = frappe.get_value(
        "User",
        dict(
            email=email
        ), "name"
    )
    # password = data['password']
    try:
        frappe.clear_cache(user=email)
        login_manager = LoginManager()
    except frappe.AuthenticationError as e:
        frappe.respond_as_web_page(_("Invalid Request"), _("Invalid Token"), http_status_code=417)

    if not email:
        frappe.respond_as_web_page(_("Invalid Request"), _("Please ensure that your profile has an email address"))
        return

    user = frappe.get_doc("User", email)
    if not user.enabled:
        frappe.respond_as_web_page(_('Not Allowed'), _('User {0} is disabled').format(user.email))
        return
    frappe.local.login_manager = login_manager
    frappe.local.login_manager.user = user
    frappe.local.login_manager.post_login()

    # because of a GET request!
    frappe.db.commit()

    # login_token = frappe.generate_hash(length=32)
    # frappe.cache().set_value("login_token:{0}".format(login_token), frappe.local.session.sid, expires_in_sec=120)
    #
    # frappe.response["login_token"] = login_token

    redirect_post_login(desk_user=frappe.local.response.get('message') == 'Logged In')


class LoginManager:
    def __init__(self):
        self.user = None
        self.info = None
        self.full_name = None
        self.user_type = None

        # if self.login() == False: return
        # self.resume = False
        #
        # # run login triggers
        # self.run_trigger('on_session_creation')
        try:
            self.resume = True
            self.make_session(resume=True)
            self.get_user_info()
            self.set_user_info(resume=True)
        except AttributeError:
            self.user = "Guest"
            self.get_user_info()
            self.make_session()
            self.set_user_info()

    def login(self):
        # clear cache
        frappe.clear_cache(user=frappe.form_dict.get('usr'))
        self.post_login()

    def post_login(self):
        self.run_trigger('on_login')
        self.user = self.user.name
        self.validate_ip_address()
        self.validate_hour()
        self.get_user_info()
        self.make_session()
        self.set_user_info()

    def get_user_info(self, resume=False):
        self.info = frappe.db.get_value("User", self.user,
                                        ["user_type", "first_name", "last_name", "user_image"], as_dict=1)

        self.user_type = self.info.user_type

    def set_user_info(self, resume=False):
        # set sid again
        frappe.local.cookie_manager.init_cookies()

        self.full_name = " ".join(filter(None, [self.info.first_name,
                                                self.info.last_name]))

        frappe.local.cookie_manager.set_cookie("system_user", "yes")
        if not resume:
            frappe.local.response['message'] = 'Logged In'
            frappe.local.response["home_page"] = "/desk"

        if not resume:
            frappe.response["full_name"] = self.full_name

        # redirect information
        redirect_to = frappe.cache().hget('redirect_after_login', self.user)
        if redirect_to:
            frappe.local.response["redirect_to"] = redirect_to
            frappe.cache().hdel('redirect_after_login', self.user)

        frappe.local.cookie_manager.set_cookie("full_name", self.full_name)
        frappe.local.cookie_manager.set_cookie("user_id", self.user)
        frappe.local.cookie_manager.set_cookie("user_image", self.info.user_image or "")

    def make_session(self, resume=False):
        # start session
        frappe.local.session_obj = Session(user=self.user, resume=resume,
                                           full_name=self.full_name, user_type=self.user_type)

        # reset user if changed to Guest
        self.user = frappe.local.session_obj.user
        frappe.local.session = frappe.local.session_obj.data
        self.clear_active_sessions()

    def clear_active_sessions(self):
        """Clear other sessions of the current user if `deny_multiple_sessions` is not set"""
        if not (cint(frappe.conf.get("deny_multiple_sessions")) or cint(
                frappe.db.get_system_setting('deny_multiple_sessions'))):
            return

        if frappe.session.user != "Guest":
            clear_sessions(frappe.session.user, keep_current=True)

    def force_user_to_reset_password(self):
        if not self.user:
            return

        reset_pwd_after_days = cint(frappe.db.get_single_value("System Settings",
                                                               "force_user_to_reset_password"))

        if reset_pwd_after_days:
            last_password_reset_date = frappe.db.get_value("User",
                                                           self.user, "last_password_reset_date") or today()

            last_pwd_reset_days = date_diff(today(), last_password_reset_date)

            if last_pwd_reset_days > reset_pwd_after_days:
                return True

    def run_trigger(self, event='on_login'):
        for method in frappe.get_hooks().get(event, []):
            frappe.call(frappe.get_attr(method), login_manager=self)

    def validate_ip_address(self):
        return
        """check if IP Address is valid"""
        user = frappe.get_doc("User", self.user.name)
        # ip_list = user.get_restricted_ip_list()
        # if not ip_list:
        #     return

        bypass_restrict_ip_check = 0
        # check if two factor auth is enabled
        enabled = int(frappe.get_system_settings('enable_two_factor_auth') or 0)
        if enabled:
            # check if bypass restrict ip is enabled for all users
            bypass_restrict_ip_check = int(frappe.get_system_settings('bypass_restrict_ip_check_if_2fa_enabled') or 0)
            if not bypass_restrict_ip_check:
                # check if bypass restrict ip is enabled for login user
                bypass_restrict_ip_check = int(
                    frappe.db.get_value('User', self.user, 'bypass_restrict_ip_check_if_2fa_enabled') or 0)
        # for ip in ip_list:
        #     if frappe.local.request_ip.startswith(ip) or bypass_restrict_ip_check:
        #         return

        frappe.throw(_("Not allowed from this IP Address"), frappe.AuthenticationError)

    def validate_hour(self):
        """check if user is logging in during restricted hours"""
        login_before = int(frappe.db.get_value('User', self.user, 'login_before', ignore=True) or 0)
        login_after = int(frappe.db.get_value('User', self.user, 'login_after', ignore=True) or 0)

        if not (login_before or login_after):
            return

        from frappe.utils import now_datetime
        current_hour = int(now_datetime().strftime('%H'))

        if login_before and current_hour > login_before:
            frappe.throw(_("Login not allowed at this time"), frappe.AuthenticationError)

        if login_after and current_hour < login_after:
            frappe.throw(_("Login not allowed at this time"), frappe.AuthenticationError)

    def login_as_guest(self):
        """login as guest"""
        self.login_as("Guest")

    def login_as(self, user):
        self.user = user.name
        self.post_login()

    def logout(self, arg='', user=None):
        if not user: user = frappe.session.user.name
        self.run_trigger('on_logout')

        if user == frappe.session.user:
            delete_session(frappe.session.sid, user=user, reason="User Manually Logged Out")
            self.clear_cookies()
        else:
            clear_sessions(user)

    def clear_cookies(self):
        clear_cookies()


def clear_cookies():
    if hasattr(frappe.local, "session"):
        frappe.session.sid = ""
    frappe.local.cookie_manager.delete_cookie(["full_name", "user_id", "sid", "user_image", "system_user"])
