# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime 
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True) 
    middlename = models.CharField("Middle Name", max_length=50,blank=True)
    

    def __str__(self):
        return("{} {} ({})".format(self.user.first_name,self.user.last_name,self.user.username))


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

    
class Level(models.Model):
    levelid = models.AutoField(db_column='levelID', primary_key=True)  # Field name made lowercase.
    levelname = models.CharField(db_column='levelName', unique=True, max_length=255)  # Field name made lowercase.

    class Meta:
        db_table = 'level'
        verbose_name = "Subject Level"
        verbose_name_plural = "Subject Levels"

    def __str__(self):
        return self.levelname
    

class Question(models.Model):
    questionid = models.AutoField("Question ID", db_column='questionID', primary_key=True)  # Field name made lowercase.
    questiontext = models.CharField("Question Text", db_column='questionText', max_length=500)  # Field name made lowercase.
    questionanswer = models.CharField("Question Answer", db_column='questionAnswer', max_length=1000)  # Field name made lowercase.
    topicid = models.ForeignKey('Topic', on_delete=models.PROTECT, db_column='topicID', verbose_name='Topic')  # Field name made lowercase.
    subjectid = models.ForeignKey('Subject', on_delete=models.PROTECT, db_column='subjectID', verbose_name='Subject')  # Field name made lowercase.
    # topicid = models.IntegerField("Topic ID", db_column='topicID')  # Field name made lowercase.
    # subjectid = models.IntegerField("Subject ID", db_column='subjectID')  # Field name made lowercase.


    class Meta:
        db_table = 'questions'
        unique_together = (('questiontext', 'topicid', 'subjectid'),)
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return str(self.questionid)

    def question_details(self):
        return self.questiontext,self.questionanswer, self.topicid, self.subjectid

    def subject(self):
        return self.subjectid
 


class Subject(models.Model):
    subjectid = models.AutoField('Subject ID', db_column='subjectID', primary_key=True)  # Field name made lowercase.
    subjectname = models.CharField('Subject Name', db_column='subjectName', unique=True, max_length=255,)  # Field name made lowercase.

    class Meta:
        db_table = 'subject'
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"        

    def __str__(self):
        return self.subjectname
    
  

class Topic(models.Model):
    topicid = models.AutoField('Topic ID',db_column='topicID', primary_key=True)  # Field name made lowercase.
    topicname = models.CharField('Topic Name', db_column='topicName', unique=True, max_length=255)  # Field name made lowercase.

    class Meta:
        db_table = 'topics'
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        

    def __str__(self):
        return self.topicname





  
class Document(models.Model):

    

    document_id = models.AutoField(db_column='documentID', primary_key = True,verbose_name = "File ID (internal)")
    description = models.CharField('File Description', max_length=255)
    subject =  models.ForeignKey('Subject', on_delete=models.PROTECT, db_column='subjectID')  
    # document = models.FileField(upload_to='upload/%Y/%m/%d', verbose_name = 'File Name')
    
    # User information
    def subject_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/subject/datetime/<filename>
        now = datetime.now()
        upload_path = 'upload/{0}/{1}/{2}/{3}/{4}'.format(instance.subject,now.year, now.month, now.day, filename)
        return upload_path
    
    document = models.FileField(upload_to=subject_directory_path, verbose_name = 'File Name')
    uploaded_at = models.DateTimeField('Date Uploaded', auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null = True, related_name='uploadedby')
    
    def __str__(self):
        return str(self.document.name)

    def get_file_name(self):
        file_name = str(self.document).split("/")[-1]
        return str(file_name)
        

    def get_file_path(self):
        file_name = str(self.document).split("/")[0:-1]
        file_names = "/".join([x for x in file_name])
        return str(file_names + "/")
        

    get_file_name.short_description = 'File Name'
    get_file_path.short_description = 'File Path'
    

class ProcessDocument(models.Model):
    processed_id = models.AutoField(db_column='processedID', primary_key = True,)
    processed_at = models.DateTimeField('Date Processed', auto_now_add=True)
    processed_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null = True)
    document_id = models.OneToOneField(Document, on_delete=models.CASCADE, unique=True, blank=True, null = True, verbose_name = "File")
    
    class Meta:
        verbose_name = 'Processed File'
        verbose_name_plural = 'Processed Files'

    def __str__(self):
        return str(self.processed_id)




#############################OTHER SHIT################################
class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
