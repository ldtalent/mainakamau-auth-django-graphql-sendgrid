# authentication/send_email.py
import jwt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string
from SendgridDjangoDemo.settings import SECRET_KEY, DOMAIN, SENDGRID_API_KEY


def send_confirmation_email(email, username):

    token = jwt.encode({'user': username}, SECRET_KEY,
                       algorithm='HS256').decode('utf-8')
    context = {
        'small_text_detail': 'Thank you for '
                             'creating an account. '
                             'Please verify your email '
                             'address to set up your account.',
        'email': email,
        'domain': DOMAIN,
        'token': token,
    }
    # locates our email.html in the templates folder
    msg_html = render_to_string('email.html', context)
    message = Mail(
        # the email that sends the confirmation email
        from_email='confirm_email@test.com',
        to_emails=[email],  # list of email receivers
        subject='Account activation',  # subject of your email
        html_content=msg_html)
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        return str(e)
