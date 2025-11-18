from django.db import models
from django.contrib.auth.models import User
############### users model extensions

class userProfile(models.Model):
   user=models.OneToOneField(User,on_delete=models.CASCADE)
   token_id=models.IntegerField()
   date_created=models.DateField(auto_now_add=True)
   date_modified=models.DateTimeField(auto_now=True)
   activated_at=models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.user.username

   

######courses
class courses(models.Model):
   course_id=models.AutoField(primary_key=True)
   course_title=models.CharField(max_length=255)
   category_id=models.IntegerField()
   description=models.CharField(max_length=255)
   status=models.CharField(max_length=255)
   creator_id=models.IntegerField()
   approved_by=models.IntegerField()
   approved_at=models.DateField(auto_now_add=True)
   date_created=models.DateField(auto_now_add=True)
   date_modified=models.DateField(auto_now=True)

    