import frappe


import frappe
from frappe.model.mapper import get_mapped_doc

import frappe


def validate(self, method):
    calculate_escl(self, method)
    self.set_status()

 

def calculate_escl(self, method):
    for row in self.items:
        if row.qty and row.rate and not row.custom_escl and not row.custom_escl_percentage:
            row.amount = row.qty * row.rate

        if row.qty and row.rate and row.custom_escl == "At Par":
            row.custom_escl_percentage = ''
            row.amount = row.qty * row.rate

        if row.qty and row.rate and row.custom_escl == "Below" and row.custom_escl_percentage:
            amount = row.qty * row.rate
            escl_amount = (row.qty * row.rate) * row.custom_escl_percentage / 100
            row.amount = amount - escl_amount

        if row.qty and row.rate and row.custom_escl == "Above" and row.custom_escl_percentage:
            amount = row.qty * row.rate
            escl_amount = (row.qty * row.rate) * row.custom_escl_percentage / 100
            row.amount = amount + escl_amount
