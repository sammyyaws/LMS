from rest_framework import serializers
from ..Models.course_models import courses, lessons, Assignment, Quiz, Submission

### Lessons nested inside the CourseSerializer
class CourseSerializer(serializers.ModelSerializer):
    lessons= serializers.SerializerMethodField()

    class Meta:
        model = courses
        fields = "__all__"
        read_only_fields = ["date_created", "date_modified"]

    def get_lessons(self, obj):
        #from ..Models.course_models import lessons
        lessons= lessons.objects.filter(course_id=obj.course_id)
        return LessonSerializer(lessons, many=True).data



### LessonSerializer with nested fields(assignments and quizzes)
class LessonSerializer(serializers.ModelSerializer):
    assignments = serializers.SerializerMethodField()
    quizzes = serializers.SerializerMethodField()
    
    class Meta:
        model = lessons
        fields = "__all__"
        
    def get_assignments(self, obj):
        #from ..Models.course_models import Assignment
        assignments = Assignment.objects.filter(lesson_id=obj.lesson_id)
        return AssignmentSerializer(assignments, many=True).data

    def get_quizzes(self, obj):
        #from ..Models.course_models import Quiz
        quizzes = Quiz.objects.filter(lesson_id=obj.lesson_id)
        return QuizSerializer(quizzes, many=True).data


###AssignmentSerializer with nested submissions
class AssignmentSerializer(serializers.ModelSerializer):
    submissions = serializers.SerializerMethodField()

    class Meta:
        model =Assignment
        fields = "__all__"
        read_only_fields = ["date_created", "date_modified"]

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"
        read_only_fields = ["date_submitted", "date_graded"]

    def get_submissions(self, obj):
        #from ..Models.course_models import Submission
        submissions = Submission.objects.filter(assignment_id=obj.assignment_id)
        return SubmissionSerializer(submissions, many=True).data




### Quiz Serializer
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"
        read_only_fields = ["date_created"]

