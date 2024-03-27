from hkm.erpnext___custom.doctype.freeze_transaction_settings.freeze_transaction_settings import (
    validate_transaction_against_frozen_date,
)
from hkm.erpnext___custom.letterhead import letterhead_query

from hkm.whatsapp.utils import run_server_script_for_doc_event


def before_insert():
    validate_transaction_against_frozen_date()
    run_server_script_for_doc_event()


def before_cancel():
    validate_transaction_against_frozen_date()
    run_server_script_for_doc_event()


def before_save():
    letterhead_query()
    run_server_script_for_doc_event()
