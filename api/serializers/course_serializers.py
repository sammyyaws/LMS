from rest_framework import serializers
from ..Models.course_models import Courses, Lessons, Assignment, Quiz, Submission



    ##submission serializer    
class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"
        read_only_fields = ["date_submitted", "date_graded"]

###AssignmentSerializer with nested submissions
class AssignmentSerializer(serializers.ModelSerializer):
    submissions = SubmissionSerializer(many=True, read_only=True, )

    class Meta:
        model =Assignment
        fields = "__all__"
        read_only_fields = ["date_created", "date_modified"]



    




### Quiz Serializer
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"
        read_only_fields = ["date_created"]




### Lesson Serializer with nested assignments and quizzes
class LessonSerializer(serializers.ModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True, )
    quizzes = QuizSerializer(many=True, read_only=True, )

    class Meta:
        model = Lessons
        fields = "__all__"




### Lessons nested inside the CourseSerializer
class CourseSerializer(serializers.ModelSerializer):
    lessons= LessonSerializer(many=True, read_only=True, source='lessons_set')

    class Meta:
        model = Courses
        fields = "__all__"
        read_only_fields = ["date_created", "date_modified"]

    



