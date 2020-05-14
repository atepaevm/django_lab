from django.db import models


class LabUser(models.Model):
    email = models.EmailField()
    name = models.TextField(default='Иван Иванов')
    hash = models.TextField()
    role = models.TextField(default='user')


class LabReport(models.Model):
    user = models.ForeignKey(LabUser, on_delete=models.DO_NOTHING)
    text = models.TextField()
    photo = models.ImageField(blank=True, null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    status = models.TextField()
    likes = models.IntegerField(default=0)
    comment = models.TextField()


class LabComment(models.Model):
    user = models.ForeignKey(LabUser, on_delete=models.DO_NOTHING)
    report = models.ForeignKey(LabReport, on_delete=models.DO_NOTHING)
    text = models.TextField()
    time = models.DateTimeField()


class LabUserReport(models.Model):
    user = models.ForeignKey(LabUser, models.DO_NOTHING, blank=True, null=True)
    report = models.ForeignKey(LabReport, models.DO_NOTHING, blank=True, null=True)
