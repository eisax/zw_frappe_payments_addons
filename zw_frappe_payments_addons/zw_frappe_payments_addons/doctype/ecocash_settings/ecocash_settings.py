# Copyright (c) 2026, josphatndhlovu and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from urllib.parse import urlencode
from frappe.utils import call_hook_method, get_url
from payments.utils import create_payment_gateway

class EcocashSettings(Document):
	supported_currencies = ("USD", "ZWL")

	def on_update(self):
		create_payment_gateway(
			"Ecocash-" + self.gateway_name,
			settings="Ecocash Settings",
			controller=self.gateway_name,
		)
		call_hook_method("payment_gateway_enabled", gateway="Ecocash-" + self.gateway_name)

	def validate_transaction_currency(self, currency):
		if currency not in self.supported_currencies:
			frappe.throw(
				_("Please select another payment method. Ecocash does not support transactions in currency '{0}'").format(currency)
			)

	def get_payment_url(self, **kwargs):
		return get_url(f"/ecocash_checkout?{urlencode(kwargs)}")

