from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string


class EmailPusher(object):
    @classmethod
    def send_email_to_af_user_on_assignment_by_hl(cls,
                                                  request=None,
                                                  request_assignment=None):
        context_data = {
            "request": request,
            "request_assignment": request_assignment,
        }
        subject = "A volunteer has started working on your request."
        text_body = render_to_string(
            template_name="email_templates/email_notify_af_about_hl_assigned_request.txt",
            context=context_data
        )

        html_body = render_to_string(
            "email_templates/email_notify_af_about_hl_assigned_request.html",
            context_data
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            to=[request.owner.user.email],
            bcc=[settings.BCC_ADDRESS_FOR_ALL_EMAILS],
            body=text_body)
        msg.attach_alternative(html_body, "text/html")
        msg.send()
        return True
