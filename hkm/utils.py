import frappe

def validate_child_single_field_duplicacy(doc, child_table, child_field):
    documents = []
    for d in doc.get(child_table):
        field_value = d.get(child_field, None)
        if field_value and (field_value in documents):
            frappe.throw(
                "Row#{0} Duplicate record not allowed for {1}".format(
                    d.idx, field_value
                )
            )
        documents.append(field_value)

@frappe.whitelist()
def get_absolute_path(file_name):
	if(file_name.startswith('/files/')):
		file_path = f'{frappe.utils.get_bench_path()}/sites/{frappe.utils.get_site_base_path()[2:]}/public{file_name}'
	if(file_name.startswith('/private/')):
		file_path = f'{frappe.utils.get_bench_path()}/sites/{frappe.utils.get_site_base_path()[2:]}{file_name}'
	return file_path
