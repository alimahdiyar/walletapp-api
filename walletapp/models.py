from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models, transaction
from django.db.models import Count, Q, Sum
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token

from .consts import (AccountInfoConsts, 
                     DateTimeRangeConsts, InvoiceConsts, UserProfileConsts)
from walletapp.helpers import generate_code, get_verification_text, send_verification_code, generate_table_token
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserProfile(models.Model):
    """
        User Profile object, one to one with django user
        additional info about the user
    """

    django_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")

    name = models.CharField(max_length=255, blank=True, null=True)

    phone_number = models.CharField(max_length=12, validators=[
        RegexValidator(
            regex="^(\+98|0)?9\d{9}$",
            message=_("Enter a valid phone number"),
            code='invalid_phone_number'
        ),
    ], unique=True)

    verification_status = models.CharField(max_length=1, choices=UserProfileConsts.states,
                                           default=UserProfileConsts.PENDING)

    @property
    def token(self):
        token, created = Token.objects.get_or_create(user=self.django_user)
        return token.key

    def __str__(self):
        return "%s (%s %s)" % (self.django_user.username, self.name, self.last_name)


class UserProfilePhoneVerificationObjectManager(models.Manager):
    def create(self, **kwargs):
        created = False

        with transaction.atomic():
            user_profile = kwargs.get('user_profile')

            # lock the user profile to prevent concurrent creations
            user_profile = UserProfile.objects.select_for_update().get(pk=user_profile.pk)

            time = timezone.now() - timezone.timedelta(minutes=UserProfilePhoneVerification.RETRY_TIME)

            # select the latest valid user profile phone verification object
            user_profile_phone = UserProfilePhoneVerification.objects.order_by('-create_date'). \
                filter(create_date__gte=time,
                       user_profile__phone_number=user_profile.phone_number) \
                .last()

            # create a new object if none exists
            if not user_profile_phone:
                obj = UserProfilePhoneVerification(**kwargs)
                obj.save()
                created = True

        if created:
            return {'status': 201, 'obj': obj}

        return {'status': 403,
                'wait': timezone.timedelta(minutes=UserProfilePhoneVerification.RETRY_TIME) +
                        (user_profile_phone.create_date - timezone.now())}


class UserProfilePhoneVerification(models.Model):
    """
        Used for phone verification by sms
        auto generates a 5 digit code
        limits select querying
        time intervals between consecutive creation
    """

    RETRY_TIME = 2
    MAX_QUERY = 5

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="phone_numbers")
    code = models.CharField(max_length=13, default=generate_code)
    create_date = models.DateTimeField(auto_now_add=True)
    query_times = models.IntegerField(default=0)
    used = models.BooleanField(default=False)
    burnt = models.BooleanField(default=False)

    objects = UserProfilePhoneVerificationObjectManager()


@receiver(post_save, sender=UserProfilePhoneVerification)
def send_verification_sms(sender, instance, created, **kwargs):
    """
        send the verification code if a new object is created
    """
    print(instance, instance.user_profile)
    if created:
        send_verification_code(instance.user_profile.phone_number, instance.code)

class AccountInfo(models.Model):
    """
        Banking Account Information
    """

    account_holder = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    account_number = models.CharField(max_length=255)


class Transaction(models.Model):
    sender = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE, related_name="outgoing_transactions")
    receiver = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE, related_name="incoming_transactions")
    reason = models.TextField()
    amount = models.IntegerField()