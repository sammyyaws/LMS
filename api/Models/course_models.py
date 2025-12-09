from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

######courses



class Course_categories(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    category_description = models.TextField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Course Category"
        verbose_name_plural = "Course Categories"
        ordering = ["category_name"]   # always sorted alphabetically

    def __str__(self):
        return self.category_name


class Courses(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Course_categories, on_delete=models.SET_NULL, null=True, related_name="courses")
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_courses")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="approved_courses")
    approved_at = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    #Method to get the creator's name
    def get_creator_name(self):
        return self.creator.get_full_name() 

    def __str__(self):
        return self.title




######grades by vic
class Grade(models.Model):
 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lessons', on_delete=models.CASCADE, related_name='grades')
    score = models.IntegerField()




#####progress by vic
class Progress(models.Model):
   
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('Courses', on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lessons', on_delete=models.CASCADE)





### Lessons by jermie

class Lessons(models.Model):

   course=models.ForeignKey("Courses",on_delete=models.CASCADE,related_name='lessons') 
   lesson_title=models.CharField(max_length=255)

   #JSON field for storing lesson type
   lesson_type = models.JSONField()
   content_url = models.CharField(max_length=255, blank=True, null=True)
   order_position = models.IntegerField()  # recommended numeric, not char
   date_created = models.DateTimeField(auto_now_add=True)
   date_modified = models.DateTimeField(auto_now=True)

   class Meta:
       ordering = ['order_position']

   def __str__(self):
       return self.lesson_title


### Assignments by jermie
class Assignment(models.Model):

   course= models.ForeignKey("Courses",on_delete=models.CASCADE, related_name="course_assignments")
   lesson = models.ForeignKey("Lessons",on_delete=models.CASCADE, related_name="lesson_assignments")
   assignment_title = models.CharField(max_length=255)
   assignment_description = models.CharField(max_length=500)
   due_date = models.DateTimeField()
   max_score = models.IntegerField()
   date_created = models.DateTimeField(auto_now_add=True)
   date_modified = models.DateTimeField(auto_now=True)

   def __str__(self):
      return self.assignment_title





### Quizzes by jermie
class Quiz(models.Model):

   course = models.ForeignKey("Courses",on_delete=models.CASCADE, related_name="course_quizzes")
   lesson = models.ForeignKey("Lessons",on_delete=models.CASCADE,related_name="lesson_quizzes")

   quiz_title = models.CharField(max_length=255)
   quiz_content = models.JSONField()
   max_score = models.IntegerField()
   date_created = models.DateTimeField(auto_now_add=True)
   date_modified = models.DateTimeField(auto_now=True)


   def __str__(self):
      return self.quiz_title




## Submissions by jermie

class Submission(models.Model):

   assignment= models.ForeignKey("Assignment",on_delete=models.CASCADE, related_name="submissions")
   user_id = models.ForeignKey("userProfile",on_delete=models.CASCADE)

   status = models.IntegerField()
   submission_content = models.CharField(max_length=500)
   date_submitted = models.DateTimeField()

   score = models.IntegerField()
   date_graded = models.DateTimeField()
   graded_by = models.IntegerField()

   def __str__(self):
      return f"Submission {self.id} - User {self.user_id}"








