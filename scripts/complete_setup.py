import frappe

def execute():
    frappe.db.set_single_value("System Settings", "setup_complete", 1)
    frappe.db.set_single_value("System Settings", "time_zone", "Asia/Kolkata")
    frappe.db.set_single_value("System Settings", "country", "India")
    frappe.db.set_single_value("System Settings", "currency", "INR")
    frappe.db.set_single_value("System Settings", "app_name", "PC CRM")
    frappe.db.sql("UPDATE `tabInstalled Application` SET is_setup_complete = 1")
    frappe.db.set_default("desktop:home_page", "workspace")
    frappe.db.commit()
    frappe.clear_cache()
    print("Setup completed successfully!")

if __name__ == "__main__":
    frappe.init("crm.localhost", "/home/frappe/frappe-bench/sites")
    frappe.connect()
    execute()
