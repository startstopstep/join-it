import pytest
from django.core.validators import MinLengthValidator
from cv.models import CvContent, Certificate, Education, WorkExperience


class TestCertificate:
    @staticmethod
    def set_up():
        Certificate.objects.create(name='Best Developer', organisation='GeekBox',
                                   issue_date='2001-01-01', credential_url='http://proof.com')

    @pytest.mark.django_db
    def test_certificate_name_length(self):
        self.set_up()
        errors = []
        certificate = Certificate.objects.get(id=1)
        name_max_length = certificate._meta.get_field('name').max_length
        name_min_length = certificate._meta.get_field('name').validators
        if name_max_length != 100:
            errors.append('max length error')
        if not MinLengthValidator(2) == name_min_length[0]:
            errors.append('validator error')
        assert not errors

    @pytest.mark.django_db
    def test_certificate_organisation_length(self):
        self.set_up()
        errors = []
        certificate = Certificate.objects.get(id=1)
        name_max_length = certificate._meta.get_field('organisation').max_length
        name_min_length = certificate._meta.get_field('organisation').validators
        if name_max_length != 100:
            errors.append('max length error')
        if not MinLengthValidator(2) == name_min_length[0]:
            errors.append('validator error')
        assert not errors


