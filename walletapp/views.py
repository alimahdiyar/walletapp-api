from django.shortcuts import render
from rest_framework import generics, status
from walletapp.serializers import SendVerificationCodeSerializer

# Create your views here.

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
            return Response({'detail': _("User profile not found")}, status=status.HTTP_404_NOT_FOUND)

        upv = UserProfilePhoneVerification.objects.create(user_profile=self.get_object())

        if upv['status'] != 201:
            return Response({'detail': _("Code not sent"), 'wait': upv['wait']}, status=upv['status'])

        return Response({'detail': _("Code sent")})