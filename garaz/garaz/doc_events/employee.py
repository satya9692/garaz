import frappe
from frappe import _



# This script will run before saving the Employee document
# and fetch the basic_salary from the Basic Salary Calculator Criteria child table

# Define the function to fetch basic salary
def validate(doc, method):
    if doc.custom_level and doc.custom_year:
        # Query the Basic Salary Calculator Criteria for the matching level and year
        basic_salary_data = frappe.db.get_value(
            'Basic Salary Calculator Criteria',
            {'parenttype': 'Basic Salary Calculator', 'level': doc.custom_level, 'year': doc.custom_year},
            'basic_salary'
        )
        
        # Set the basic_salary if data is found
        if basic_salary_data:
            doc.ctc = basic_salary_data
        else:
            frappe.throw(_('No matching salary found in Basic Salary Calculator Criteria'))

# Link the function to the document event
