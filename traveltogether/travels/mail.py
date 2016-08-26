from django.core.mail import EmailMessage
from django.conf import settings
from traveltogether.settings import MEDIA_ROOT
from os.path import join


def mail_register(depart_time, start, end, user_email, file_name):
    BODY = """You have joined a travel!
You will travel from {} to {} on {}.
You can download the attrached file and import it to you calendar.
If you do that it will notify you one hour before the travel.
""".format(start, end, depart_time)
    file = join(MEDIA_ROOT, 'travels', 'export', file_name)
    content = open(file, 'rb').read()
    mimetype = 'application/ics'
    ATTACHMENT = (file_name, content, mimetype)

    email = EmailMessage(
        'Travel - Joined',
        BODY,
        settings.EMAIL_HOST_USER,
        [user_email, ],
        attachments=[ATTACHMENT]
    )
    return email
