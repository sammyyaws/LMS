from django.db import models

#####roles by vic
class Role(models.Model):
    
    role_name = models.CharField(max_length=255,unique=True)
    role_description = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.role_name
