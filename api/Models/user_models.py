from django.db import models
from django.contrib.auth.models import User
from .roles_models import Role
############### users model extensions

class userProfile(models.Model):
   user=models.OneToOneField(User,on_delete=models.CASCADE)
   token_id = models.IntegerField(default=0)
   role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
   date_created=models.DateField(auto_now_add=True)
   date_modified=models.DateTimeField(auto_now=True)
   activated_at=models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.user.username



