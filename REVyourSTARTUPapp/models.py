from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

#TODO: create appropriate models for rev form applicable to the json interface

class MainForm(models.Model):
    # This model will work as the 'Hub' for attaching all the different forms onto
    # by a specific user's id as a primary key. All of the seperate forms will be a foriegn key
    
    main_form_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    form_name = models.TextField(blank=True, null=True)
    rev_form = models.ForeignKey('RevForm', models.DO_NOTHING, blank=True, null=True)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return str(self.form_name)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(MainForm, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'main_form'


class RevForm(models.Model):
    rev_form_id = models.AutoField(primary_key=True)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)
    class Meta:
        managed = True
        db_table = 'rev_form'