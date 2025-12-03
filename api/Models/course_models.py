from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

######courses



class course_categories(models.Model):
    category_id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=255)
    category_description = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField(db_column='date modified')
class courses(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(course_categories, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    status = models.CharField(max_length=50, default="pending") 
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_courses")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="approved_courses")
    approved_at = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title




######grades by vic
class grade(models.Model):
    grade_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey('lessons', on_delete=models.CASCADE)
    score = models.IntegerField()




#####progress by vic
class progress(models.Model):
    progress_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('courses', on_delete=models.CASCADE)
    lesson = models.ForeignKey('lessons', on_delete=models.CASCADE)





### Lessons by jermie

class lessons(models.Model):
  
   course=models.ForeignKey("courses",on_delete=models.CASCADE) 
   lesson_title=models.CharField(max_length=255)

   #JSON field for storing lesson type
   lesson_type = models.JSONField()
   
   content_url = models.CharField(max_length=255)
   content_url = models.CharField(max_length=255, blank=True, null=True)
   order_position = models.IntegerField()  # recommended numeric, not char
   date_created = models.DateTimeField(auto_now_add=True) 
   def __str__(self):
      return self.lesson_title
   

### Assignments by jermie
class Assignment(models.Model):
   assignment_id = models.AutoField(primary_key=True)
   course_id = models.ForeignKey("courses",on_delete=models.CASCADE)
   lesson_id = models.ForeignKey("lessons",on_delete=models.CASCADE)

   assignment_title = models.CharField(max_length=255)
   assignment_description = models.CharField(max_length=500)

   due_date = models.DateTimeField()
   max_score = models.IntegerField()

   date_created = models.DateTimeField()
   date_modified = models.DateTimeField(auto_now=True)

   def __str__(self):
      return self.assignment_title





### Quizzes by jermie
class Quiz(models.Model):
   quiz_id = models.AutoField(primary_key=True)
   course_id = models.ForeignKey("courses",on_delete=models.CASCADE)
   lesson_id = models.ForeignKey("lessons",on_delete=models.CASCADE)

   quiz_title = models.CharField(max_length=255)
   quiz_content = models.JSONField()
   max_score = models.IntegerField()
   date_created = models.DateTimeField()
   created_by = models.IntegerField()
   date_modified = models.DateTimeField(auto_now=True)

   def __str__(self):
      return self.quiz_title




## Submissions by jermie

class Submission(models.Model):
   submission_id = models.AutoField(primary_key=True)
   assignment_id = models.ForeignKey("Assignment",on_delete=models.CASCADE)
   user_id = models.ForeignKey("userProfile",on_delete=models.CASCADE)

   status = models.IntegerField()
   submission_content = models.CharField(max_length=500)
   date_submitted = models.DateTimeField()

   score = models.IntegerField()
   date_graded = models.DateTimeField()
   graded_by = models.IntegerField()

   def __str__(self):
      return f"Submission {self.submission_id} - User {self.user_id}"




####course categories by vic





