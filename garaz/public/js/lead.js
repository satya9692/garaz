erpnext.LeadController = class LeadController extends frappe.ui.form.Controller {
    make_quotation() {
		frappe.model.open_mapped_doc({
			method: "garaz.garaz.doc_events.lead.create_quotation_from_lead",
			frm: cur_frm,
		});
	}
}