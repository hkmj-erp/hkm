from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
    get_accounting_dimensions,
)


relevant_documents = [
    "Purchase Order",
    "Purchase Invoice",
    "Sales Invoice",
    "Stock Entry",
    "Purchase Receipt",
]


def set_cost_center(doc, method=None):
    if doc.doctype in relevant_documents:
        dimensions = get_accounting_dimensions()
        dimensions.extend(["cost_center", "project"])
        for dim in dimensions:
            if doc.get(dim):
                for item in doc.items:
                    item.set(dim, doc.get(dim))
