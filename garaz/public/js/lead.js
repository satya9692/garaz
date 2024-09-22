erpnext.LeadController = class LeadController extends frappe.ui.form.Controller {
    make_quotation() {
		frappe.model.open_mapped_doc({
			method: "garaz.garaz.doc_events.lead.create_quotation_from_lead",
			frm: cur_frm,
		});
	}
}

frappe.ui.form.on("Lead Schedule", {
	quantity: function(frm, cdt, cdn){
		var row = locals[cdt][cdn];
		if(row.quantity){
			row.amount = row.rate * row.quantity;
			refresh_field("amount", cdn, "lead_schedule");
		}
	},
	rate: function(frm, cdt, cdn){
		var row = locals[cdt][cdn];
		if(row.rate){
			row.amount = row.rate * row.quantity;
			refresh_field("amount", cdn, "lead_schedule");

		}
	}
})