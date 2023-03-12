from django.conf import settings
from django.db import models


class CvContent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    title = models.CharField(max_length=30)
    summary = models.TextField()
    location = models.CharField(max_length=100, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    github_url = models.URLField(max_length=200, blank=True, null=True)
    skills = models.TextField(help_text='Comma separated list of skills',
                              max_length=500, blank=True)
    education = models.ForeignKey('cv.Education', on_delete=models.CASCADE,
                                  blank=True, null=True,
                                  related_name='educations')
    work_experience = models.ForeignKey('cv.WorkExperience',
                                        on_delete=models.CASCADE, blank=True,
                                        null=True,
                                        related_name='work_experiences')
    certificate = models.ForeignKey('cv.Certificate', on_delete=models.CASCADE,
                                    related_name='certificates')

    def __str__(self):
        return f'{self.user}_CV'


class Education(models.Model):
    school = models.CharField(max_length=100)
    degree = models.CharField(max_length=100, blank=True, null=True)
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __self__(self):
        return self.school


class WorkExperience(models.Model):
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    currently_working = models.BooleanField(default=False)

    def __self__(self):
        return self.company


class Certificate(models.Model):
    name = models.CharField(max_length=100)
    organisation = models.CharField(max_length=100, blank=True, null=True)
    issue_date = models.DateField(blank=True, null=True)
    credential_url = models.URLField()

    def __self__(self):
        return self.name
