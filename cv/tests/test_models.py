import pytest
from freezegun import freeze_time

from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model
from cv.models import CvContent, Certificate, Education, WorkExperience

USER = get_user_model()


@pytest.mark.django_db
class TestCvContent:

    @pytest.fixture
    def user(self):
        return USER.objects.create_user(
            email='tasty-tester@exaple.com',
        )

    @pytest.fixture
    def certificate(self):
        return Certificate.objects.create(
            name='Tester',
            credential_url='proof.link',
        )

    @pytest.fixture
    def education(self):
        return Education.objects.create(
            school='test_school',
            field_of_study='test_field',
        )

    @pytest.fixture
    def work_experience(self):
        return WorkExperience.objects.create(
            company='test_company',
            currently_working='False',
        )

    @pytest.fixture
    def cv_content(self, user, education, work_experience, certificate):
        return CvContent.objects.create(
            user=user,
            first_name='test',
            last_name='name',
            title='tester',
            summary='test',
            education=education,
            work_experience=work_experience,
            certificate=certificate,
        )

    def test_values(self, cv_content, user, education, work_experience, certificate):
        assert cv_content.user == user
        assert cv_content.first_name == 'test'
        assert cv_content.last_name == 'name'
        assert cv_content.title == 'tester'
        assert cv_content.summary == 'test'
        assert cv_content.education == education
        assert cv_content.work_experience == work_experience
        assert cv_content.certificate == certificate

    


class TestEducation:
    pass


class TestWorkExperience:
    pass


class TestCertificate:
    pass
