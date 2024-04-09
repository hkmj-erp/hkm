from hkm.erpnext___custom.doctype.freeze_transaction_settings.freeze_transaction_settings import (
    validate_transaction_against_frozen_date,
)
from hkm.erpnext___custom.letterhead import letterhead_query

from hkm.whatsapp.utils import run_server_script_for_doc_event


def before_insert(self,method):
    validate_transaction_against_frozen_date(self,method)
    run_server_script_for_doc_event(self,method)


def before_cancel(self,method):
    validate_transaction_against_frozen_date(self,method)
    run_server_script_for_doc_event(self,method)


def before_save(self,method):
    letterhead_query(self,method)
    run_server_script_for_doc_event(self,method)

def after_insert(self,method):
    run_server_script_for_doc_event(self,method)


def before_validate(self,method):
    run_server_script_for_doc_event(self,method)


def validate(self,method):
    run_server_script_for_doc_event(self,method)


def on_update(self,method):
    run_server_script_for_doc_event(self,method)


def before_submit(self,method):
    run_server_script_for_doc_event(self,method)


def on_submit(self,method):
    run_server_script_for_doc_event(self,method)


def on_cancel(self,method):
    run_server_script_for_doc_event(self,method)


def on_trash(self,method):
    run_server_script_for_doc_event(self,method)


def after_delete(self,method):
    run_server_script_for_doc_event(self,method)


def before_update_after_submit(self,method):
    run_server_script_for_doc_event(self,method)


def on_update_after_submit(self,method):
    run_server_script_for_doc_event(self,method)


