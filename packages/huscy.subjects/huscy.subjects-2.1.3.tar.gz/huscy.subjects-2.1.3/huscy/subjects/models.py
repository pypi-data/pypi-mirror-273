import uuid
from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _

from dateutil import relativedelta
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    class GENDER(models.IntegerChoices):
        female = 0, _('female')
        male = 1, _('male')
        diverse = 2, _('diverse')

    id = models.UUIDField(_('ID'), primary_key=True, default=uuid.uuid4, editable=False)

    first_name = models.CharField(_('First name'), max_length=128)  # without middle names
    last_name = models.CharField(_('Last name'), max_length=128)  # without middle names

    # full name with prefixes (titles) and suffixes
    display_name = models.CharField(_('Display name'), max_length=255)

    gender = models.PositiveSmallIntegerField(_('Gender'), choices=GENDER.choices)

    date_of_birth = models.DateField(_('Date of birth'))

    city = models.CharField(_('City'), max_length=128)
    country = CountryField(_('Country'), default='DE')
    postal_code = models.CharField(_('Postal code'), max_length=16)
    street = models.CharField(_('Street'), max_length=255)  # street name & number + additional info

    email = models.EmailField(_('Email'), blank=True, default='')
    phone_mobile = PhoneNumberField(_('Phone mobile'), blank=True, default='')
    phone_home = PhoneNumberField(_('Phone home'), blank=True, default='')
    phone_work = PhoneNumberField(_('Phone work'), blank=True, default='')
    phone_emergency = PhoneNumberField(_('Phone emergency'), blank=True, default='')

    def __str__(self):
        return f'{self.display_name}'

    class Meta:
        ordering = 'last_name', 'first_name'
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')


class Subject(models.Model):
    id = models.UUIDField(_('ID'), primary_key=True, default=uuid.uuid4, editable=False)

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='+',
                                verbose_name=_('Contact'))
    guardians = models.ManyToManyField(Contact, blank=True, related_name='subjects',
                                       verbose_name=_('Guardians'))

    @property
    def age_in_months(self):
        delta = relativedelta.relativedelta(date.today(), self.contact.date_of_birth)
        return delta.years * 12 + delta.months

    @property
    def age_in_years(self):
        return relativedelta.relativedelta(date.today(), self.contact.date_of_birth).years

    @property
    def is_active(self):
        # I used inactivity.all() instead of inactivity.get() because .get() would make extra
        # database queries
        inactivity = self.inactivity_set.all()
        if inactivity and (inactivity[0].until is None or inactivity[0].until >= date.today()):
            return False
        return True

    @property
    def is_child(self):
        return self.child_set.exists()

    @property
    def is_patient(self):
        return self.patient_set.exists()

    def __str__(self):
        return str(self.contact)

    class Meta:
        ordering = 'contact__last_name', 'contact__first_name'
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')


class Child(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_('Subject'))

    def __str__(self):
        return str(self.subject)

    class Meta:
        ordering = 'subject__contact__last_name', 'subject__contact__first_name'
        verbose_name = _('Child')
        verbose_name_plural = _('Children')


class Patient(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_('Subject'))

    def __str__(self):
        return str(self.subject)

    class Meta:
        ordering = 'subject__contact__last_name', 'subject__contact__first_name'
        verbose_name = _('Patient')
        verbose_name_plural = _('Patients')


class Inactivity(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_('Subject'))
    until = models.DateField(_('Until'), null=True)  # until = null means inactive with open end

    class Meta:
        ordering = 'subject__contact__display_name',
        verbose_name = _('Inactivity')
        verbose_name_plural = _('Inactivities')
