import pytest
from freezegun import freeze_time

from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model
from cv.models import CvContent, Certificate, Education, WorkExperience
from django.db import IntegrityError

USER = get_user_model()


@pytest.mark.django_db
class TestCvContent:

    @pytest.fixture
    def certificate(self):
        return Certificate.objects.create(
            name='tester',
            credential_url='proof.link',
        )

    @pytest.fixture
    def cv_content(self, user, education, work_experience, certificate):
        return CvContent.objects.create(
            title='tester',
            summary='test',
            certificate=certificate,
        )

    def test_values(self, cv_content, user, education, work_experience, certificate):
        assert cv_content.title == 'tester'
        assert cv_content.summary == 'test'
        assert cv_content.certificate == certificate

    def test_title_length(self, cv_content):
        errors = []
        max_length = cv_content._meta.get_field("title").max_length
        min_length = cv_content._meta.get_field("title").validators
        if not max_length == 30:
            errors.append('max length error')
        if not min_length[0] == MinLengthValidator(3):
            errors.append('validator error')
        assert not errors

    def test_cv_without_title_creation(self, certificate):
        with pytest.raises(IntegrityError):
            CvContent.objects.create(
                title=None,
                summary='test',
                certificate=certificate,
            )


@pytest.mark.django_db
class TestEducation:

    @pytest.fixture
    def education(self):
        return Education.objects.create(
            school='test_school',
            field_of_study='test_field',
        )

    def test_values(self, education):
        assert education.school == 'test_school'
        assert education.field_of_study == 'test_field'

    def test_school_length(self, education):
        errors = []
        max_length = education._meta.get_field("school").max_length
        min_length = education._meta.get_field("school").validators
        if not max_length == 100:
            errors.append('max length error')
        if not min_length[0] == MinLengthValidator(2):
            errors.append('validator error')
        assert not errors

    def test_education_without_school_creation(self):
        with pytest.raises(IntegrityError):
            Education.objects.create(
                school=None,
                field_of_study='test',
            )


@pytest.mark.django_db
class TestWorkExperience:
    @pytest.fixture
    def work_experience(self):
        return WorkExperience.objects.create(
            company='test_company',
        )

    def test_values(self, work_experience):
        assert work_experience.company == 'test_company'
        assert work_experience.currently_working is False

    def test_company_length(self, work_experience):
        errors = []
        max_length = work_experience._meta.get_field("company").max_length
        min_length = work_experience._meta.get_field("company").validators
        if not max_length == 100:
            errors.append('max length error')
        if not min_length[0] == MinLengthValidator(2):
            errors.append('validator error')
        assert not errors

    def test_work_experience_without_company_creation(self):
        with pytest.raises(IntegrityError):
            WorkExperience.objects.create(
                company=None,
            )


@pytest.mark.django_db
class TestCertificate:
    @pytest.fixture
    def certificate(self):
        return Certificate.objects.create(
            name='tester',
            credential_url='proof.link',
        )

    def test_values(self, certificate):
        assert certificate.name == 'tester'
        assert certificate.credential_url == 'proof.link'

    def test_certificate_without_name_creation(self):
        with pytest.raises(IntegrityError):
            Certificate.objects.create(
                name=None,
                credential_url='proof.link',
            )
