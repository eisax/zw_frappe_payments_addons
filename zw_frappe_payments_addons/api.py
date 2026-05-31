import frappe
from frappe import _
import requests
import uuid
import json

@frappe.whitelist(allow_guest=True)
def initiate_ecocash_payment(reference_doctype, reference_docname, amount, currency, msisdn):
    # Get the payment gateway controller
    doc = frappe.get_doc(reference_doctype, reference_docname)
    gateway_controller = frappe.db.get_value("Payment Gateway", doc.payment_gateway, "gateway_controller")
    settings = frappe.get_doc("Ecocash Settings", gateway_controller)
    
    # Base URL depends on live_mode
    base_url = "https://developers.ecocash.co.zw/api/ecocash_pay" # Base URL
    endpoint = "/api/v2/payment/instant/c2b/live" if settings.live_mode else "/api/v2/payment/instant/c2b/sandbox"
    url = f"{base_url}{endpoint}"
    
    headers = {
        "X-API-KEY": settings.get_password("api_key"),
        "Content-Type": "application/json"
    }
    
    payload = {
        "customerMsisdn": msisdn,
        "amount": float(amount),
        "reason": "Payment",
        "currency": currency,
        "sourceReference": str(uuid.uuid4()),
        "resultUrl": frappe.utils.get_url("/api/method/zw_frappe_payments_addons.api.ecocash_webhook")
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        
        if response.status_code == 200:
            # Payment success or pending
            return frappe.redirect_to_message(_("Payment Initiated"), _("Please check your phone and enter your PIN to complete the transaction."))
        else:
            frappe.log_error(message=response.text, title="Ecocash Payment Failed")
            return frappe.redirect_to_message(_("Payment Failed"), _("Failed to initiate payment. Please try again."))
            
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Ecocash Payment Error"))
        return frappe.redirect_to_message(_("Error"), _("An error occurred while processing your payment."))


@frappe.whitelist(allow_guest=True)
def paynow_webhook():
    # To handle Paynow webhook updates
    # This requires processing the data sent back from Paynow to verify the transaction
    # Since Paynow sends a POST request with the updated status
    pass

@frappe.whitelist(allow_guest=True)
def ecocash_webhook():
    """
    Handle incoming webhook from Ecocash for transaction updates.
    """
    # The payload will contain transaction details and status
    data = frappe.request.get_json() if frappe.request else None
    if not data:
        return {"status": "error", "message": "No payload"}
        
    # Process the callback data and update Frappe Payment Request status
    # ...
    
    return {"status": "success"}
