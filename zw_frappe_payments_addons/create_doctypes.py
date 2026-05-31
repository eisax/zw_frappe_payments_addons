import frappe

def create_doctypes():
    frappe.init(site="apk.local")
    frappe.connect()
    if not frappe.db.exists("DocType", "Ecocash Settings"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "module": "Zw Frappe Payments Addons",
            "custom": 0,
            "name": "Ecocash Settings",
            "is_single": 0,
            "fields": [
                {"fieldname": "gateway_name", "fieldtype": "Data", "label": "Gateway Name", "reqd": 1, "unique": 1},
                {"fieldname": "api_key", "fieldtype": "Password", "label": "API Key", "reqd": 1},
                {"fieldname": "live_mode", "fieldtype": "Check", "label": "Live Mode", "default": "0"},
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
            ]
        })
        doc.insert()
        print("Created Ecocash Settings Doctype")

    if not frappe.db.exists("DocType", "Paynow Settings"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "module": "Zw Frappe Payments Addons",
            "custom": 0,
            "name": "Paynow Settings",
            "is_single": 0,
            "fields": [
                {"fieldname": "gateway_name", "fieldtype": "Data", "label": "Gateway Name", "reqd": 1, "unique": 1},
                {"fieldname": "integration_id", "fieldtype": "Data", "label": "Integration ID", "reqd": 1},
                {"fieldname": "integration_key", "fieldtype": "Password", "label": "Integration Key", "reqd": 1},
                {"fieldname": "live_mode", "fieldtype": "Check", "label": "Live Mode", "default": "0"},
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
            ]
        })
        doc.insert()
        print("Created Paynow Settings Doctype")

    frappe.db.commit()

if __name__ == "__main__":
    create_doctypes()
