from django.db import models
from django.contrib.auth.models import User


class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='enrollments')
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'enrollments'
        unique_together = ('user', 'course')
        ordering = ['-date_enrolled']

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course}"


class Discussion(models.Model):
    discussion_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='discussions')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='discussions')
    message = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'discussion'
        ordering = ['-date_created']

    def __str__(self):
        return f"Discussion {self.discussion_id} by {self.user.username}"


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='feedbacks')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='feedbacks')
    content = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'feedback'
        ordering = ['-date_created']

    def __str__(self):
        return f"Feedback {self.feedback_id} by {self.user.username}"
