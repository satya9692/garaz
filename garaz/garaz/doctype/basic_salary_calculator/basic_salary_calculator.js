frappe.ui.form.on('Basic Salary Calculator', {
    refresh: function(frm) {
        renderEditableSalaryGrid(frm);
    }
});

function renderEditableSalaryGrid(frm) {
    frm.fields_dict.basic_salary_grid.$wrapper.html("");

    // HTML structure for the table
    let html = `
        <div style="text-align: center; margin-top: 20px;">
            <h3 style="color: #ff704d; font-weight: bold;">Basic Salary Calculation Based on Position Level and Year Of Experiance</h3>
            <table style="width: 100%; border-collapse: collapse; text-align: center;">
                <thead>
                    <tr style="background-color: #ff704d; color: white;">
                        <th style="padding: 10px; border: 1px solid #ddd;">Position Level / Year Of Experiance</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">1 Year</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">2 Years</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">3 Years</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">4 Years</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">5 Years</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">6 Years</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">7 Years</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">8 Years</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">9 Years</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">10 Years</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">11 Years</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">12 Years</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">13 Years</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">14 Years</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">15 Years</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">16 Year</th>
                    </tr>
                </thead>
                <tbody id="salary-grid-body">
                </tbody>
            </table>
        </div>`;

    // Injecting the HTML into the wrapper
    frm.fields_dict.basic_salary_grid.$wrapper.html(html);

    // Fetching data for rendering the table
    frappe.call({
        method: "garaz.garaz.doctype.basic_salary_calculator.basic_salary_calculator.get_basic_salary_data",  // Adjust this path to your app and module
        args: { basic_salary_calculator: frm.doc.name },
        callback: function(response) {
            if (response.message) {
                const data = response.message;
                let maxDegree = 14;
                let maxYear = 17
                // Populate table rows based on levels and years
                for (let level = 1; level < maxDegree; level++) {
                    let rowHTML = `<tr style="background-color: ${level % 2 == 0 ? '#e6f7ff' : '#b3e0ff'};">`;
                    rowHTML += `<td style="padding: 10px; font-weight: bold; border: 1px solid #ddd;">Level ${level}</td>`;

                    for (let year = 1; year < maxYear; year++) {
                        const cellData = data.find(d => d.level === `Level ${level}` && d.year === `${year} Year${year > 1 ? 's' : ''}`);
                        rowHTML += `<td contenteditable="true" data-name="${cellData ? cellData.name : ''}" data-level="Level ${level}" data-year="${year} Year${year > 1 ? 's' : ''}" style="padding: 10px; border: 1px solid #ddd;">${cellData ? cellData.basic_salary : '-'}</td>`;
                    }

                    rowHTML += "</tr>";
                    $("#salary-grid-body").append(rowHTML);
                }

                // Reattach the event listener for capturing edits after rendering the table
                $("#salary-grid-body").on("blur", "td[contenteditable=true]", function() {
                    const newSalary = $(this).text().trim();
                    const name = $(this).data("name");
                    console.log("Cell edited: ", { newSalary, name });  // Debugging line

                    // Update the salary only if there is a valid record name
                    if (name && newSalary) {
                        frappe.call({
                            method: "garaz.garaz.doctype.basic_salary_calculator.basic_salary_calculator.update_basic_salary",  // Adjust this path
                            args: {
                                name: name,
                                new_salary: newSalary
                            },
                            callback: function(r) {
                                if (r.message) {
                                    frappe.show_alert({
                                        message: "Salary updated successfully!",
                                        indicator: "green"
                                    });
                                }
                            }
                        });
                    }
                });
            }
        }
    });
}
