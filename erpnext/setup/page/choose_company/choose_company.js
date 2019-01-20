frappe.pages['choose-company'].on_page_load = function(wrapper) {
	const parent = $('<div class="company_list"></div>').appendTo(wrapper);

	parent.html(frappe.render_template("company_list", {}));
	parent.find(".btn-choose-company").on("click", function() {
		if (company.value != null){
			frappe.boot.user.current_company = company.value;
			window.location.href = "#"
		}else{
			parent.find(".indicator").removeClass("blue").addClass("red").text("Please Select a Company to Continue")
		}
	});

	let options = null;
	let unscrub_option = frappe.model.unscrub("company");
	let user_permission = frappe.defaults.get_user_permissions();
	if(user_permission && user_permission[unscrub_option]) {
		options = user_permission[unscrub_option]["docs"];
	} else {
		options = $.map(locals[`:${unscrub_option}`], function (c) {
			return c.name;
		}).sort()
	}

	const company = frappe.ui.form.make_control({
		parent: parent.find(".choose-company"),
		df: {
			fieldtype: "Select",
			options: options
		}
	});
	company.refresh();
};