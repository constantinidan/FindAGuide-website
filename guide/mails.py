import sendgrid

"""
	This file is a module for sending emails using sendgrid
"""

# send email with sendgrid
def send_email(dest,subject,message,sender='tommyboy@findaguide.com'):
	
	sg = sendgrid.SendGridClient('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')
	msg = sendgrid.Mail()
	msg.add_to(dest)
	msg.set_subject(subject)
	msg.set_html(message)
	msg.set_from(sender)
	status, msg = sg.send(msg)


# add some text before sending email with sendgrid
def send_contact_email(dest,subject,message,sender,senderUsername):
	
	subject = "FindAGuide : " + subject
	message = "You have been contacted by " + senderUsername + " on findAGuide :\r\r" + message

	send_email(dest,subject,message,sender)