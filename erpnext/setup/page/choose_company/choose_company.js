frappe.pages['choose-company'].on_page_load = function(wrapper) {
	const parent = $('<div class="company_list"></div>').appendTo(wrapper);

	parent.html(frappe.render_template("company_list", {}));

	let companies = [];
	frappe.call({
		method: "erpnext.setup.doctype.company.get_allowed_companies.get_allowed_companies",
		args: {
			user: frappe.session.user
		},
		freeze: true,
		callback: function(r) {
			companies = r.message;
			companies.forEach(function (company) {
				if(company === localStorage.getItem("session_company")){
					parent.find(".choose-company").append(new Option(company, company, false, true));
				}else{
					parent.find(".choose-company").append(new Option(company, company));
				}
			})
		}
	});

	parent.find(".btn-choose-company").on("click", function() {
		let company = $(".choose-company").val();
		frappe.ui.toolbar.set_session_company(company);
		if (company !== null){
			frappe.ui.toolbar.set_session_company(company);
		}else{
			parent.find(".indicator").removeClass("blue").addClass("red").text("Please Select a Company to Continue")
		}
	});
};