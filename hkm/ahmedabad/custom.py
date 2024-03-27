import frappe


def get_purchase_order_details(pi):
    purchase_orders = []
    pi_doc = frappe.get_doc("Purchase Invoice", pi)
    for item in pi_doc.items:
        if item.purchase_order:
            purchase_orders.append(item.purchase_order)

    purchase_orders = list(set(purchase_orders))

    po_data = {}

    for po in purchase_orders:
        po_doc = frappe.get_doc("Purchase Order", po)
        po_data.setdefault(
            po,
            {
                "extra_description": po_doc.extra_description,
                "recommender": po_doc.recommended_by,
                "first_approver": po_doc.first_approving_authority,
                "final_approver": po_doc.final_approving_authority,
            },
        )
    return po_data
