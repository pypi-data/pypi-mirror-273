import logging

from django.conf import settings
from django.db.models import Exists, OuterRef
from django.utils import timezone

from huscy.subjects.models import Child, Contact, Inactivity, Patient, Subject

logger = logging.getLogger('huscy.subjects')


AGE_OF_MAJORITY = getattr(settings, 'HUSCY_SUBJECTS_AGE_OF_MAJORITY', 18)


def create_contact(first_name, last_name, gender, date_of_birth,
                   country, city, postal_code, street,
                   display_name='',
                   email='', phone_emergency='', phone_home='', phone_mobile='', phone_work=''):
    contact = Contact.objects.create(
        city=city,
        country=country,
        date_of_birth=date_of_birth,
        display_name=display_name if display_name else f'{first_name} {last_name}',
        email=email,
        first_name=first_name,
        gender=gender,
        last_name=last_name,
        phone_emergency=phone_emergency,
        phone_home=phone_home,
        phone_mobile=phone_mobile,
        phone_work=phone_work,
        postal_code=postal_code,
        street=street,
    )
    return contact


def update_contact(contact, first_name, last_name, gender, date_of_birth,
                   country, city, postal_code, street,
                   display_name='',
                   email='', phone_emergency='', phone_home='', phone_mobile='', phone_work=''):
    contact.country = country
    contact.city = city
    contact.date_of_birth = date_of_birth
    contact.display_name = display_name if display_name else contact.display_name
    contact.email = email
    contact.first_name = first_name
    contact.gender = gender
    contact.last_name = last_name
    contact.phone_emergency = phone_emergency
    contact.phone_home = phone_home
    contact.phone_mobile = phone_mobile
    contact.phone_work = phone_work
    contact.postal_code = postal_code
    contact.street = street
    contact.save()
    return contact


def create_subject(contact, is_patient=False):
    subject = Subject.objects.create(contact=contact)

    logger.info('Subject id:%d has been created', subject.id)

    if subject.age_in_years < AGE_OF_MAJORITY:
        Child.objects.create(subject=subject)

    if is_patient:
        Patient.objects.create(subject=subject)

    return subject


def delete_subject(subject):
    for guardian in subject.guardians.all():
        remove_guardian(subject, guardian)
    subject.delete()
    subject.contact.delete()


def get_subjects(include_children=False, include_patients=False):
    queryset = Subject.objects

    if include_children is False:
        queryset = queryset.exclude(Exists(Child.objects.filter(subject=OuterRef('pk'))))

    if include_patients is False:
        queryset = queryset.exclude(Exists(Patient.objects.filter(subject=OuterRef('pk'))))

    return (queryset.select_related('contact')
                    .prefetch_related('child_set', 'guardians', 'inactivity_set', 'patient_set')
                    .order_by('contact__last_name', 'contact__first_name'))


def update_subject(subject, is_patient):
    if subject.age_in_years < AGE_OF_MAJORITY and subject.is_child is False:
        Child.objects.create(subject=subject)

    if is_patient is True and subject.is_patient is False:
        Patient.objects.create(subject=subject)
    elif is_patient is False and subject.is_patient is True:
        subject.patient_set.get().delete()

    return subject


def set_inactivity(subject, until=None):
    if until and until < timezone.now().date():
        raise ValueError(f'Until ({until}) cannot be in the past.')

    inactivity, created = Inactivity.objects.get_or_create(subject=subject,
                                                           defaults={'until': until})
    if not created:
        inactivity.until = until
        inactivity.save()

    return inactivity


def unset_inactivity(subject):
    subject.inactivity_set.all().delete()


def add_guardian(subject, contact):
    if subject.contact == contact:
        raise ValueError('Cannot add contact as guardian because it\'s the subject itself!')

    subject.guardians.add(contact)
    return contact


def remove_guardian(subject, guardian):
    subject.guardians.remove(guardian)
    if not guardian.subjects.exists():
        guardian.delete()
