import random
from django.utils.translation import ugettext as _
from sms.models import Operator, Message


def generate_code():
    return str(random.randint(1000, 9999))



def get_verification_text(code):
    return _("به walletapp خوش آمدید: %s" % code)


def send_verification_code(to, code):
    print("to:", to)
    message = Message.objects.create(to=to, message=get_verification_text(code))
    if(Operator.objects.exists()):
        Operator.objects.first().send_message(message)
    else:
        print('No operator defined')
