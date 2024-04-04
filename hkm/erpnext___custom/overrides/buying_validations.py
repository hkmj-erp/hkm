import frappe
from frappe import _
def validate_work_order_item(self):
    if not self.meta.get_field("for_a_work_order") or not self.for_a_work_order: 
        return
    invalid_work_order_items = []

    non_stock_items = frappe.get_list('Item', pluck='name', filters={'disabled':0, 'is_stock_item':0})
    for d in self.get("items"):
        if d.item_code not in non_stock_items:
            invalid_work_order_items.append(d)

    for d in invalid_work_order_items:
        frappe.throw(
            _('Row#{0}: Stock Item {1} is not allowed for Work Order.<br>Please select non stock item.')
            .format(
                d.idx,
                frappe.bold(d.item_name),
            ), 
            title=_("Invalid Item")
        )
    return

def check_items_are_not_from_template(self):
    for item in self.items:
        if frappe.get_value("Item",item.item_code,'has_variants') == 1:
            self.validate = False
            frappe.throw("Item Code : {} is a Template. It can not be used in Transactions".format(item.item_code))
    return