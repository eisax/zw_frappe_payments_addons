import frappe

def get_context(context):
    context.no_cache = 1
    context.amount = frappe.form_dict.get("amount")
    context.currency = frappe.form_dict.get("currency")
    context.reference_doctype = frappe.form_dict.get("reference_doctype")
    context.reference_docname = frappe.form_dict.get("reference_docname")
