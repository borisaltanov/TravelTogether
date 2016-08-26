import re
from os.path import join
from traveltogether.settings import MEDIA_ROOT


def date_time_format(date_time):
    year = date_time[0:4]
    month = date_time[5:7]
    day = date_time[8:10]
    hour = date_time[11:13]
    minute = date_time[14:16]

    return "{}{}{}T{}{}00".format(year, month, day, hour, minute)


def duration_format(duration):
    values = re.findall('\d+', duration)
    if len(values) == 1:
        minute = values[0]
        return 'PT0H{}M0S'.format(minute)
    else:
        hour = values[0]
        minute = values[1]
        return 'PT{}H{}M0S'.format(hour, minute)


def travel_export(
        travel_id, depart_time, duration, start, end, user_email, usename,
        write=False):
    event = """BEGIN:VCALENDAR
BEGIN:VEVENT
DTSTART:{}
DURATION:{}
LOCATION:{}
SUMMARY:Travel from {} to {}
BEGIN:VALARM
ACTION:EMAIL
DESCRIPTION:This is an event reminder
SUMMARY:Alarm notification
ATTENDEE:mailto:{}
TRIGGER:-P0DT1H0M0S
END:VALARM
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:This is an event reminder
TRIGGER:-P0DT1H0M0S
END:VALARM
END:VEVENT
END:VCALENDAR""".format(depart_time, duration, start, start, end, user_email)
    file_name = 'travel_{}_for_{}.ics'.format(travel_id, usename)
    path = join(MEDIA_ROOT, 'travels', 'export', file_name)
    if write:
        with open(path, 'w') as export_ics:
            export_ics.write(event)

    return event, file_name
