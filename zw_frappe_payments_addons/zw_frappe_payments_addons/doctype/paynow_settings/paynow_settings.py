# Copyright (c) 2026, josphatndhlovu and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import call_hook_method, get_url
from payments.utils import create_payment_gateway
from urllib.parse import urlencode

class PaynowSettings(Document):
	supported_currencies = ("USD", "ZWL")

	def on_update(self):
		create_payment_gateway(
			"Paynow-" + self.gateway_name,
			settings="Paynow Settings",
			controller=self.name,
		)
		call_hook_method("payment_gateway_enabled", gateway="Paynow-" + self.gateway_name)

	def validate_transaction_currency(self, currency):
		if currency not in self.supported_currencies:
			frappe.throw(
				_("Please select another payment method. Paynow does not support transactions in currency '{0}'").format(currency)
			)

	def get_payment_url(self, **kwargs):
		from paynow import Paynow

		# Setup redirect and result URLs
		return_url = get_url(f"/payment-success?{urlencode({'doctype': kwargs.get('reference_doctype'), 'docname': kwargs.get('reference_docname')})}")
		result_url = get_url(f"/api/method/zw_frappe_payments_addons.api.paynow_webhook")

		paynow = Paynow(
			self.integration_id, 
			self.get_password("integration_key"),
			return_url, 
			result_url
		)

		payer_email = kwargs.get("payer_email") or frappe.session.user
		description = kwargs.get("description", "Payment")
		reference = f"{kwargs.get('reference_doctype')}-{kwargs.get('reference_docname')}"
		
		payment = paynow.create_payment(reference, payer_email)
		payment.add(description, kwargs.get("amount"))

		response = paynow.send(payment)

		if response.success:
			# Get the redirect URL and return it
			return response.redirect_url
		else:
			frappe.throw(_("Could not initiate Paynow transaction: {0}").format(response.error))

