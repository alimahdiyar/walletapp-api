import random
from django.utils.translation import ugettext as _
from sms.models import Operator, Message


def generate_code():
    return str(random.randint(10000, 99999))


def generate_table_token():
    return str(random.randint(100000000000, 999999999999))


def get_verification_text(code):
    return _("به walletapp خوش آمدید: %s" % code)


def send_verification_code(to, code):
    print("to:", to)
    message = Message.objects.create(to=to, message=get_verification_text(code))
    return Operator.objects.first().send_message(message)
