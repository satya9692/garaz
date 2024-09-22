import frappe


import frappe
from frappe.model.mapper import get_mapped_doc

import frappe


def validate(self, method):
    for row in self.items:
        if row.qty and row.rate:
            row.amount = row.qty * row.rate

        
@frappe.whitelist()
def create_quotation_from_lead(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.run_method("set_missing_values")
        target.run_method("calculate_taxes_and_totals")


    def update_item(source_doc, target_doc, source_parent):
        target_doc.item_code = source_doc.item_code
        target_doc.description = source_doc.description
        target_doc.qty = source_doc.quantity
        target_doc.uom = source_doc.uom
        target_doc.rate = source_doc.rate
        target_doc.amount = source_doc.amount


    doclist = get_mapped_doc(
        "Lead",
        source_name,
        {
            "Lead": {
                "doctype": "Quotation",
                "field_map": {
                    "doctype": "quotation_to",
                    "name": "party_name",  # Example field mapping
                    "company": "company",
                },
            },
            "Lead Schedule": {
                "doctype": "Quotation Item",
                "field_map": {
                    "item_code": "item_code",
                    "description": "description",
                    "quantity": "qty",
                    "uom": "uom",
                    "rate": "rate",
                    "amount": "amount",
                },
                "postprocess": update_item,
            },
        },
        target_doc,
        set_missing_values,
    )
    if doclist:
        doclist.quotation_to = "Lead"  # Now we can safely assign this value

    return doclist
