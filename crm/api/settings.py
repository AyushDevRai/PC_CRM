import frappe


@frappe.whitelist()
def create_email_account(data: dict):
	if isinstance(data, str):
		data = frappe.parse_json(data)

	service = data.get("service")
	service_config = email_service_config.get(service)
	if not service_config:
		frappe.throw(frappe._("Service '{0}' is not supported").format(service))

	try:
		password = data.get("password") or ""
		if isinstance(password, str):
			password = password.strip()
			if service == "GMail":
				# Google App Passwords are 16 characters, often formatted with spaces like 'abcd efgh ijkl mnop'
				cleaned = password.replace(" ", "")
				if len(cleaned) == 16:
					password = cleaned

		enable_incoming = 1 if data.get("enable_incoming") else 0
		enable_outgoing = 1 if data.get("enable_outgoing") else 0
		create_lead = 1 if data.get("create_lead_from_incoming_email") else 0

		email_doc = frappe.get_doc(
			{
				"doctype": "Email Account",
				"email_id": (data.get("email_id") or "").strip(),
				"email_account_name": (data.get("email_account_name") or "").strip(),
				"service": service,
				"enable_incoming": enable_incoming,
				"enable_outgoing": enable_outgoing,
				"default_incoming": 1 if data.get("default_incoming") else 0,
				"default_outgoing": 1 if data.get("default_outgoing") else 0,
				"create_lead_from_incoming_email": create_lead,
				"create_contact": create_lead,
				"email_sync_option": "ALL",
				"initial_sync_count": 100,
				"track_email_status": 1,
				"use_tls": 1,
				"use_imap": 1,
				"smtp_port": 587,
				**service_config,
			}
		)
		if service == "Frappe Mail":
			email_doc.api_key = data.get("api_key")
			email_doc.api_secret = data.get("api_secret")
			email_doc.frappe_mail_site = data.get("frappe_mail_site")
			if create_lead:
				email_doc.append_to = "CRM Lead"
		else:
			if enable_incoming:
				email_doc.append(
					"imap_folder",
					{
						"append_to": "CRM Lead" if create_lead else None,
						"folder_name": "INBOX",
					},
				)
			email_doc.password = password

		# EmailAccount.validate automatically checks IMAP connection if enable_incoming,
		# and SMTP connection if enable_outgoing.
		email_doc.save()
	except Exception as e:
		err_str = str(e)
		is_cred_error = (
			"AUTHENTICATIONFAILED" in err_str
			or "Invalid credentials" in err_str
			or "Authentication failed" in err_str
			or "Please check your email login credentials" in err_str
			or isinstance(e, frappe.email.smtp.InvalidEmailCredentials)
		)
		if is_cred_error:
			frappe.clear_messages()
			if service == "GMail":
				frappe.throw(
					frappe._(
						"Invalid credentials for Gmail. Google requires a 16-character App Password (not your normal Google account password). Please enable 2-Step Verification in your Google Account security settings, create an App Password at https://myaccount.google.com/apppasswords, and paste it here."
					)
				)
			elif service == "Outlook":
				frappe.throw(
					frappe._(
						"Invalid credentials for Outlook. If 2FA is enabled on your Microsoft account, please generate an App Password in your Microsoft Account security settings."
					)
				)
			else:
				frappe.throw(
					frappe._("Invalid credentials for {0}. Please verify your username and password.").format(service)
				)
		frappe.throw(err_str)


email_service_config = {
	"Frappe Mail": {
		"domain": None,
		"password": None,
		"awaiting_password": 0,
		"ascii_encode_password": 0,
		"login_id_is_different": 0,
		"login_id": None,
		"use_imap": 0,
		"use_ssl": 0,
		"validate_ssl_certificate": 0,
		"use_starttls": 0,
		"email_server": None,
		"incoming_port": 0,
		"always_use_account_email_id_as_sender": 1,
		"use_tls": 0,
		"use_ssl_for_outgoing": 0,
		"smtp_server": None,
		"smtp_port": None,
		"no_smtp_authentication": 0,
	},
	"GMail": {
		"email_server": "imap.gmail.com",
		"use_ssl": 1,
		"smtp_server": "smtp.gmail.com",
	},
	"Outlook": {
		"email_server": "imap-mail.outlook.com",
		"use_ssl": 1,
		"smtp_server": "smtp-mail.outlook.com",
	},
	"Sendgrid": {
		"smtp_server": "smtp.sendgrid.net",
		"smtp_port": 587,
	},
	"SparkPost": {
		"smtp_server": "smtp.sparkpostmail.com",
	},
	"Yahoo": {
		"email_server": "imap.mail.yahoo.com",
		"use_ssl": 1,
		"smtp_server": "smtp.mail.yahoo.com",
		"smtp_port": 587,
	},
	"Yandex": {
		"email_server": "imap.yandex.com",
		"use_ssl": 1,
		"smtp_server": "smtp.yandex.com",
		"smtp_port": 587,
	},
}
