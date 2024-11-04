import frappe
from frappe.utils import nowdate, getdate, add_days, today, now_datetime, format_datetime, get_datetime
from datetime import timedelta


def send_bid_start_email():
    # Query for leads where the bid start date is today
    leads = frappe.get_all('Lead', filters={
        'custom_bidding_start_date': nowdate()
    }, fields=['name', 'lead_owner', 'custom_department_email', 'custom_bidding_start_date'])

    for lead in leads:
        if lead.custom_department_email and lead.lead_owner:
            # Fetch the lead owner's email address
            lead_owner_email = frappe.get_value('User', lead.lead_owner, 'email')
            lead_owner_name = frappe.get_value('User', lead.lead_owner, 'full_name')

            # Get the email template
            template = frappe.get_doc("Email Template", "Bid Start Notification")
            bidding_start_date = getdate(lead.custom_bidding_start_date).strftime("%B %d, %Y")

            # Render the template with the lead data
            subject = f"Bid Start for Lead {lead.name}"
            message = f"Dear {lead_owner_name}, the bid for Lead {lead.name} is starting on {bidding_start_date}."
            # message = frappe.render_template(template.response, {"doc": lead})
            # subject = frappe.render_template(template.subject, {"doc": lead})

            # Send the email using the template
            frappe.sendmail(
                recipients=[lead.custom_department_email],
                cc=[lead_owner_email],
                subject=subject,
                message=message
                )
            frappe.db.commit()



def send_tender_reminder():
    leads = frappe.get_all('Lead', filters={
        'custom_tender_closing_date_and_time': ['>=', now_datetime()]
    }, fields=['name', 'custom_tender_closing_date_and_time', 'lead_owner', 'custom_department_email'])

    for lead in leads:
        tender_date = lead['custom_tender_closing_date_and_time']
        current_date = now_datetime() # Extract only the current date part
        
        # Check if the reminder should be sent (3 days, 2 days, 1 day, or same day)
        days_left = (tender_date - current_date).days
        if days_left in [3, 2, 1, 0]:
            send_email_reminder(lead['name'], lead['custom_tender_closing_date_and_time'], lead['lead_owner'], lead['custom_department_email'], days_left)

def send_email_reminder(lead_name, tender_date, lead_owner, custom_department_email, days_left):
    formatted_tender_date = format_datetime(tender_date, "dd-MM-yyyy HH:mm:ss")

    # Prepare the email content
    if days_left == 0:
        subject = f"Reminder: Tender closing today for Lead {lead_name}"
    else:
        subject = f"Reminder: Tender closing in {days_left} days for Lead {lead_name}"

    # Construct the message
    message = f"The Tender for Lead {lead_name} is closing on {formatted_tender_date}. Please take necessary actions."

    # Send email to department and CC lead owner
    frappe.sendmail(
        recipients=[custom_department_email],
        cc=[lead_owner],
        subject=subject,
        message=message
    )
    frappe.db.commit()


from frappe.utils import add_months, now_datetime, getdate, format_datetime

def send_completion_reminder():
    leads = frappe.get_all('Lead', filters={
        'custom_tender_closing_date_and_time': ['>=', now_datetime()]
    }, fields=['name', 'custom_tender_closing_date_and_time', 'custom_period_of_completion', 'lead_owner', 'custom_department_email'])

    for lead in leads:
        # Get tender closing date and period of completion
        tender_date = getdate(lead['custom_tender_closing_date_and_time'])
        period_of_completion = lead['custom_period_of_completion']  # Assuming this is in months
        
        try:
            period_of_completion = int(lead['custom_period_of_completion'])  # Cast to int
        except (ValueError, TypeError):
            period_of_completion = 0  # Default to 0 if there's an issue

        # Calculate the completion date by adding the period of completion
        completion_date = add_months(tender_date, period_of_completion)
        # Get today's date
        current_date = getdate(now_datetime())
        
        # Check if today is the completion date
        if current_date == completion_date:
            send_completion_email(lead['name'], completion_date, lead['lead_owner'], lead['custom_department_email'])

def send_completion_email(lead_name, completion_date, lead_owner, custom_department_email):
    # Format completion date to 'DD-MM-YYYY'
    formatted_completion_date = format_datetime(completion_date, "dd-MM-yyyy")
    
    # Prepare the email subject and message
    subject = f"Completion Reminder for Lead {lead_name} ({formatted_completion_date})"
    message = f"The period of completion for Lead {lead_name} is completed on {formatted_completion_date}. Please take necessary actions."

    # Send email to department and CC lead owner
    frappe.sendmail(
        recipients=[custom_department_email],
        cc=[lead_owner],
        subject=subject,
        message=message
    )
    frappe.db.commit()


def schedule_tender_emails():
    # Fetch all leads with a tender date
    leads = frappe.get_all('Lead', filters={
        'custom_tender_closing_date_and_time': ['>', now_datetime()]
    }, fields=['name', 'lead_owner', 'custom_tender_closing_date_and_time', 'custom_validity_of_offer_days', 'custom_department_email'])

    for lead in leads:
        if lead.custom_tender_closing_date_and_time and lead.custom_validity_of_offer_days:
            tender_date = get_datetime(lead.custom_tender_closing_date_and_time)
            
            # Convert the validity_of_offer field to an integer (assuming it's in days)
            validity_days = int(lead.custom_validity_of_offer_days)
            
            # Calculate the email dates based on tender closing date
            email_15_days_after = add_days(tender_date, 15)
            email_30_days_after = add_days(tender_date, 30)
            email_45_days_after = add_days(tender_date, 45)
            email_60_days_after = add_days(tender_date, 60)
            # Enqueue email jobs at the required intervals
            schedule_email(lead, email_15_days_after, "15 days after Tender Closing")
            schedule_email(lead, email_30_days_after, "30 days after Tender Closing")
            schedule_email(lead, email_45_days_after, "45 days after Tender Closing")
            schedule_email(lead, email_60_days_after, "60 days after Tender Closing")

def schedule_email(lead, scheduled_date, email_subject_suffix):
    # Check if the current date is after the scheduled date

    if now_datetime() >= scheduled_date:
        # Fetch the lead owner's email address
        lead_owner_email = frappe.get_value('User', lead.lead_owner, 'email')
        
        # Format the tender date for email
        formatted_tender_date = lead.custom_tender_closing_date_and_time.strftime('%B %d, %Y, %H:%M %p')

        # Email subject
        subject = f"Tender Closing Notification - {email_subject_suffix}"
        
        # Email body (customize as per your requirement)
        message = f"""
        Dear {lead.lead_owner},
        
        This is a reminder that {email_subject_suffix} for Lead {lead.name}.
        
        Tender Closing Date: {formatted_tender_date}
        
        Regards,
        Mr. Garaz Private Limited
        """
        
        # Enqueue the email to be sent at the scheduled date
        frappe.enqueue(
            method=frappe.sendmail,
            queue='long',
            recipients=[lead.custom_department_email],
            cc=[lead_owner_email],
            subject=subject,
            message=message,
            schedule_time=scheduled_date  # Email will be sent on this date
        )
