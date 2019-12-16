from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, status

from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView

from walletapp.consts import UserProfileConsts
from walletapp.serializers import SendVerificationCodeSerializer, UserProfilePhoneVerificationSerializer, \
    UserProfileDataSerializer, TransactionBulkCreateSerializer
from walletapp.models import UserProfile, UserProfilePhoneVerification, Transaction
from rest_framework.response import Response
from django.db import transaction

# Create your views here.
from walletapp_api import settings


class TransactionBulkCreateView(ListBulkCreateUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionBulkCreateSerializer

class SendVerificationCodeView(generics.GenericAPIView):
    """
        Send verification code
        if send failed respond with wait time
    """

    serializer_class = SendVerificationCodeSerializer

    def get_object(self):
        phone_number = self.request.data.get('phone_number')

        try:
            return UserProfile.objects.get(phone_number=phone_number)
        except UserProfile.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        user_profile = self.get_object()

        if not user_profile:
            try:
                with transaction.atomic():
                    user_profile = UserProfile.objects.create(phone_number=self.request.data.get('phone_number'),
                                                              django_user=User.objects.create(
                                                                  username=self.request.data.get('phone_number')))
            except:
                return Response({'detail': _("Phone number not valid")}, status=status.HTTP_400_BAD_REQUEST)

        upv = UserProfilePhoneVerification.objects.create(user_profile=self.get_object())

        if upv['status'] != 201:
            return Response({'detail': _("Code not sent"), 'wait': upv['wait']}, status=upv['status'])

        if settings.DEBUG:
            return Response({'detail': _("Code sent"), 'code': upv['code']})

        return Response({'detail': _("Code sent")})


class RetrieveUserProfileDataView(generics.RetrieveAPIView):
    serializer_class = UserProfileDataSerializer

    def get_object(self):
        return self.request.user.user_profile


class UserProfileAuthTokenView(generics.CreateAPIView):
    """
        match phone number and verification code
        return user token on success
    """

    serializer_class = UserProfilePhoneVerificationSerializer

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone_number')
        code = request.data.get('code')

        user_profile_phone_ = UserProfilePhoneVerification.objects.order_by('create_date'). \
            filter(
            query_times__lt=UserProfilePhoneVerification.MAX_QUERY,
            used=False,
            burnt=False,
            user_profile__phone_number=phone
        )
        user_profile_phone = user_profile_phone_.last()

        if not user_profile_phone:
            return Response({'detail': _('Phone number not found')}, status=status.HTTP_404_NOT_FOUND)

        if code != user_profile_phone.code:
            user_profile_phone.query_times += 1
            user_profile_phone.save()

            return Response({'detail': _('Invalid verification code'),
                             'allowed_retry_times':
                                 UserProfilePhoneVerification.MAX_QUERY -
                                 user_profile_phone.query_times},
                            status=status.HTTP_403_FORBIDDEN)

        user_profile_phone.user_profile.verification_status = UserProfileConsts.VERIFIED
        user_profile_phone.user_profile.save()
        token, created = Token.objects.get_or_create(user=user_profile_phone.user_profile.django_user)

        user_profile_phone.used = True
        user_profile_phone.save()

        # mark all other codes as burnt
        user_profile_phone_.update(burnt=True)

        return Response({'phone_number': phone, 'token': token.key})
