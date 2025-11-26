from django.db import models


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
   date_created=models.DateField()
   date_modified=models.DateField(auto_now=True)




######grades by vic
class grade(models.Model):
    grade_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_id')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, db_column='lesson_id')
    score = models.IntegerField()




#####progress by vic
class progress(models.Model):
    progress_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_id')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, db_column='course_id')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, db_column='lesson_id')





### Lessons by jermie

class lessons(models.Model):
   lesson_id=models.AutoField(primary_key=True)
   course_id=models.ForeignKey("courses",on_delete=models.CASCADE) 
   lesson_title=models.CharField(max_length=255)

   #JSON field for storing lesson type
   lesson_type = models.JSONField()
   content_url = models.CharField(max_length=255)
   order_position = models.CharField(max_length=255)
   date_created = models.DateTimeField()

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
   #JSON field to match longtext and also CHECK json_valid
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








