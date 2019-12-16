from rest_framework import serializers
from walletapp.models import UserProfile, UserTransactionTag, Transaction
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
    ListBulkCreateUpdateDestroyAPIView,
)
from rest_framework.fields import CurrentUserDefault

class TransactionBulkCreateSerializer(BulkSerializerMixin, serializers.ModelSerializer):

    def save(self, **kwargs):
        self.validated_data['owner'] = self.context['request'].user.user_profile
        super(TransactionBulkCreateSerializer, self).save()

    class Meta(object):
        model = Transaction
        fields = ['amount', 'reason', 'tags', 'is_income']
        # only necessary in DRF3



class UserTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['reason', 'amount', 'is_income']


class UserTransactionTagSerializer(serializers.ModelSerializer):
    user_tag_transactions = UserTransactionSerializer(many=True)

    class Meta:
        model = UserTransactionTag
        fields = ['title', 'user_tag_transactions']


class UserProfileDataSerializer(serializers.ModelSerializer):
    user_tags = UserTransactionTagSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'user_tags']


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


class UserProfilePhoneVerificationSerializer(serializers.Serializer):
    """
        Used for verifying phone numbers
    """

    phone_number = serializers.CharField(max_length=12)
    code = serializers.CharField(max_length=10)
