from django.utils.translation import gettext as _


class InvoiceConsts():
    
    # balance types
    DEBIT = '0'
    CREDIT = '1'

    # states
    DONE = '0'
    CREATED = '1'
    IN_PAYMENT = '2'
    REJECTED = '3'

    balance_types = (
        (DEBIT, _('Debit')),
        (CREDIT, _('Credit'))
    )

    states = (
        (DONE, _('Done')),
        (CREATED, _('Created')),
        (IN_PAYMENT, _('In Payment')),
        (REJECTED, _('Rejected'))
    )


class AccountInfoConsts():

    VERIFIED = '0'
    PENDGIN = '1'
    REJECTED = '2'

    _account_verification_states = ((VERIFIED, _('Verified')),
                                    (PENDGIN, _('Pending')),
                                    (REJECTED, _('Rejected')))



class UserProfileConsts():
    
    PENDING = '0'
    VERIFIED = '1'

    states = (
        (PENDING, "Pending"),
        (VERIFIED, "Verified"),
    )

class DateTimeRangeConsts():
    
    SATURDAY = '0'
    SUNDAY = '1'
    MONDAY = '2'
    TUESDAY = '3'
    WEDNESDAY = '4'
    THURSDAY = '5'
    FRIDAY = '6'

    days = (
        (SATURDAY, "Saturday"),
        (SUNDAY, "Sunday"),
        (MONDAY, "Monday"),
        (TUESDAY, "Tuesday"),
        (WEDNESDAY, "Wednesday"),
        (THURSDAY, "Thursday"),
        (FRIDAY, "Friday")
    )
