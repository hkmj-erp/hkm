# Copyright (c) 2023, Narahari Dasa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from firebase_admin import messaging
from datetime import datetime, timedelta


class AppNotification(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        app: DF.Link
        is_route: DF.Check
        message: DF.Text
        notify: DF.Check
        read: DF.Check
        route: DF.Data | None
        subject: DF.Data
        tag: DF.Data | None
        user: DF.Link

    # end: auto-generated types
    def after_insert(self):
        # TODO Review this as it can't be dependent on Dhananjaya App.
        # mobile_app_notifications = frappe.db.get_single_value(
        #     "Dhananjaya Settings",
        #     "mobile_app_notifications",
        # )
        mobile_app_notifications = 1
        if self.notify and mobile_app_notifications:
            self.send_app_notification()

    def send_app_notification(self):
        tokens = frappe.get_all(
            "Firebase App Token",
            pluck="token",
            filters={"user": self.user},
        )
        if len(tokens) > 0:
            # See documentation on defining a message payload.
            # frappe.errprint(self.message)
            # frappe.errprint(str(self.is_route))
            # frappe.errprint(self.route)
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=self.subject,
                    body=self.message,
                ),
                data={"is_route": str(self.is_route), "screen": str(self.route)},
                tokens=tokens,
                android=messaging.AndroidConfig(
                    ttl=timedelta(seconds=3600),
                    priority="normal",
                    notification=messaging.AndroidNotification(
                        icon="stock_ticker_update", color="#f45342"
                    ),
                ),
            )
            fa_doc = frappe.get_doc("Firebase Admin App", self.app)
            response = messaging.send_multicast(message, app=fa_doc.instance)
            return response


def delete_old_app_notifications():
    one_month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    eligible_notiifcations = frappe.get_all(
        "App Notification",
        filters=[["creation", "<", one_month_ago]],
        page_length=5000,
        order_by="creation",
        pluck="name",
    )
    for n in eligible_notiifcations:
        frappe.delete_doc("App Notification", n)
