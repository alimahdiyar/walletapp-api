from django.contrib import admin
from walletapp.models import UserProfile, UserTransactionTag, Transaction
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserTransactionTag)
admin.site.register(Transaction)