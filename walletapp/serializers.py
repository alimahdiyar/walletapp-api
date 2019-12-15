from rest_framework import serializers
from walletapp.models import UserProfile

class SendVerificationCodeSerializer(serializers.ModelSerializer):
    """
        Used to fetch phone number and send verification code to it
        if a user profile with the given phone number exists then only
        a verification code will be sent to it
        if not, one will be created
    """

    class Meta:
        model = UserProfile
        fields = ['phone_number', ]