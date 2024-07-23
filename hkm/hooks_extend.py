from hkm.erpnext___custom.letterhead import letterhead_query
from hkm.erpnext___custom.extend.cost_center import set_cost_center


def before_save(self, method=None):
    set_cost_center(self, method=None)
    letterhead_query(self, method=None)
