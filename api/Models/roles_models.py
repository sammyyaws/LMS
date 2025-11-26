from django.db import models

#####roles by vic
class roles(models.Model):
    id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255)
    role_description = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField()

   

####course categories by vic
class course_categories(models.Model):
    category_id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=255)
    category_description = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField(db_column='date modified')