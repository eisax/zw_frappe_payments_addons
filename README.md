## Zw Frappe Payments Addons

Includes Zimbabwean payment methods (Ecocash & Paynow) for Frappe and ERPNext.

### Installation

To install this app on your Frappe environment, run the following commands:

```bash
bench get-app https://github.com/your-repo/zw_frappe_payments_addons.git
bench --site your_site_name install-app zw_frappe_payments_addons
```

### Configuration

#### 1. Ecocash
- Log in to your Frappe site.
- Search for **Ecocash Settings**.
- Create a new record:
  - **Gateway Name**: e.g. `Ecocash`
  - **API Key**: The `X-API-KEY` provided by Ecocash (e.g. `1wddI46HBW3pK7pH32wgr3st9wIM7E4w` for sandbox).
  - **Live Mode**: Check this box if you are using Live credentials.
- After saving, a new **Payment Gateway** named `Ecocash-Ecocash` will be created automatically. You can now select it when creating a Payment Request.

#### 2. Paynow
- Search for **Paynow Settings**.
- Create a new record:
  - **Gateway Name**: e.g. `Paynow`
  - **Integration ID**: Your Paynow Integration ID.
  - **Integration Key**: Your Paynow Integration Key.
  - **Live Mode**: Paynow determines live vs test based on the credentials, but the flag is available for completeness.
- After saving, a new **Payment Gateway** named `Paynow-Paynow` will be created automatically.

### Usage in Checkout
When a user selects "Ecocash" on the checkout page, they will be redirected to a custom form where they must input their **Ecocash Mobile Number**. They will then receive a push notification on their phone to complete the transaction by entering their PIN.

When a user selects "Paynow", they will be redirected to the secure Paynow checkout page where they can complete the payment using various local methods (ZimSwitch, Visa, etc.).

### Sandbox Testing
- **Ecocash**: Use any local mobile number in the format `26377...` and enter the testing PINs (`0000`, `1234`, or `9999`) on your phone (if a test simulator is provided) or via API responses.
- **Paynow**: Sandbox transactions can be viewed from your Paynow Developer Hub.

### License

mit
