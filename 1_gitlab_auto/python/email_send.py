from locale import format_string
from log import logger


def send_emails(
        emails_list: list
    ) -> None:
    """
    Dummy function for demonstration
    """
    for email in emails_list:
        logger.info(f'Email from template {email.get("template")} will be sent to {email.get("dst_email")}')

# In real cases it should be something like this
# import smtplib
# import ssl
# import typing as t
# from config import src_email, smtp_pass,\
#                    smtp_server, smtp_server_port,\
#                    email_rename_templ,\
#                    email_update_templ

# def send_emails(
#         emails_list: list
#     ) -> None:
#     context = ssl.create_default_context()
#     with smtplib.SMTP_SSL(smtp_server, smtp_server_port, context=context) as server:
#         server.login(src_email, smtp_pass)
#         for email in emails_list:
#             server.sendmail(
#                 src_email,
#                 email.get('dst_email'),
#                 make_templ(email.get('template')).format(
#                                                     branch=email.get('branch'),
#                                                     ),
#             )

# def make_templ(templ_name: str) -> t.Union[str, None]:
#     if templ_name == 'rename':
#         return email_rename_templ
#     if templ_name == 'update':
#         return email_update_templ
#     return None


