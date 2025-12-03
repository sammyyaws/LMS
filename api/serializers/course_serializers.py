from rest_framework import serializers
from ..Models.course_models import courses, lessons, Assignment, Quiz, Submission



    ##submission serializer    
class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"
        read_only_fields = ["date_submitted", "date_graded"]

###AssignmentSerializer with nested submissions
class AssignmentSerializer(serializers.ModelSerializer):
    submissions = SubmissionSerializer(many=True, read_only=True, source='submission_set')

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
    assignments = AssignmentSerializer(many=True, read_only=True, source='assignment_set')
    quizzes = QuizSerializer(many=True, read_only=True, source='quiz_set')

    class Meta:
        model = lessons
        fields = "__all__"






















### Lessons nested inside the CourseSerializer
class CourseSerializer(serializers.ModelSerializer):
    lessons= LessonSerializer(many=True, read_only=True, source='lessons_set')

    class Meta:
        model = courses
        fields = "__all__"
        read_only_fields = ["date_created", "date_modified"]

    



