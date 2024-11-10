# Copyright (c) 2024, bhaliyadhruvin8@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BasicSalaryCalculator(Document):
	pass


@frappe.whitelist()
def get_basic_salary_data(basic_salary_calculator):
    return frappe.get_all(
        "Basic Salary Calculator Criteria",
        filters={"parent": basic_salary_calculator},
        fields=["level", "year", "basic_salary", "name"],
        # order_by="level asc, year asc"
    )

@frappe.whitelist()
def update_basic_salary(name, new_salary):
    # Update the basic salary field in Basic Salary Calculator Criteria
    frappe.db.set_value("Basic Salary Calculator Criteria", name, "basic_salary", new_salary)
    frappe.db.commit()