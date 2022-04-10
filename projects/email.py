from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def send_welcome_email(name,receiver):
    # Creating message subject and sender
    subject = 'Welcome to the Awwwards Website'
    sender = 'akumucollins001@gmail.com'

    #passing in the context vairables
    text_content = render_to_string('email/awwwardsemail.txt',{"name": name})
    html_content = render_to_string('email/awwwardsemail.html',{"name": name})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()