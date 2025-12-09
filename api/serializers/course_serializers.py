from rest_framework import serializers
from ..Models.course_models import Courses, Lessons, Assignment, Quiz, Submission,Course_categories
from django.utils import timezone



    ##submission serializer    
class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"
        read_only_fields = ["date_submitted", "date_graded"]

###AssignmentSerializer with nested submissions
class AssignmentSerializer(serializers.ModelSerializer):
    # Optional: show readable info instead of just IDs
    course_title = serializers.CharField(source="course.title", read_only=True)
    lesson_title = serializers.CharField(source="lesson.lesson_title", read_only=True)

    class Meta:
        model = Assignment
        fields = [
            "id",
            "course",
            "course_title",
            "lesson",
            "lesson_title",
            "assignment_title",
            "assignment_description",
            "due_date",
            "max_score",
            "date_created",
            "date_modified",
        ]
        read_only_fields = ["date_created", "date_modified"]

    # ------- FIELD LEVEL VALIDATIONS -------

    def validate_assignment_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Assignment title must be at least 3 characters long.")
        return value

    def validate_max_score(self, value):
        if value <= 0:
            raise serializers.ValidationError("Max score must be greater than zero.")
        if value > 100:
            raise serializers.ValidationError("Max score cannot exceed 100.")
        return value

    def validate_due_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

    # ------- OBJECT LEVEL VALIDATION -------
    def validate(self, data):
        course = data.get("course")
        lesson = data.get("lesson")

        # Ensure the lesson actually belongs to the selected course
        if lesson and course and lesson.course_id != course.id:
            raise serializers.ValidationError(
                {"lesson": "Selected lesson does not belong to this course."}
            )

        return data





### Quiz Serializer
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"
        read_only_fields = ["date_created"]




### Lesson Serializer with nested assignments and quizzes
class LessonSerializer(serializers.ModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True, source='lesson_assignments')
    quizzes = QuizSerializer(many=True, read_only=True, source='lesson_quizzes')
    assignment_count = serializers.SerializerMethodField()
    quiz_count = serializers.SerializerMethodField()
    course_title = serializers.ReadOnlyField(source='course.title')

    class Meta:
        model = Lessons
        fields = "__all__"

    def get_assignment_count(self, obj):
        return obj.lesson_assignments.count()

    def get_quiz_count(self, obj):
        return obj.lesson_quizzes.count()

    def validate_lesson_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Lesson title cannot be empty.")
        return value

    def validate_order_position(self, value):
        if value < 0:
            raise serializers.ValidationError("Order position must be a positive integer.")
        return value





######################  course category serializer  ###############
class CategorySerializer(serializers.ModelSerializer):
    course_count = serializers.SerializerMethodField()

    class Meta:
        model = Course_categories
        fields = [
            "id",
            "category_name",
            "category_description",
            "date_created",
            "date_modified",
            "course_count",
        ]
        read_only_fields = ["date_created", "date_modified"]

    def get_course_count(self, obj):
        return obj.courses_set.count() if hasattr(obj, "courses_set") else 0

    def validate_category_name(self, value):
        """Ensure category name is unique even during updates."""
        category_id = getattr(self.instance, "id", None)
        if Course_categories.objects.filter(category_name=value).exclude(id=category_id).exists():
            raise serializers.ValidationError("A category with this name already exists.")
        return value


######################  course serializer  ###############
class CourseSerializer(serializers.ModelSerializer):
    # Nested read-only fields
    lessons = LessonSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    # Write-only field for category assignment
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Course_categories.objects.all(),
        source='category',
        write_only=True
    )

    # Extra information fields
    creator_name = serializers.SerializerMethodField()
    lesson_count = serializers.SerializerMethodField()
    creator_id = serializers.ReadOnlyField(source='creator.id')

    class Meta:
        model = Courses
        fields = [
            "id", "title", "description", "status",
            "category", "category_id",
            "creator_id", "creator_name",
            "approved_by", "approved_at",
            "date_created", "date_modified",
            "lessons", "lesson_count"
        ]

        read_only_fields = [
            "status",          # creators cannot set this
            "approved_by",
            "approved_at",
            "date_created",
            "date_modified",
            "creator_id"
        ]

  

    def get_creator_name(self, obj):
        return obj.get_creator_name()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

   
    # VALIDATIONS
   

    def validate_title(self, value):
        """Ensure title is unique even during updates."""
        course_id = getattr(self.instance, "id", None)
        if Courses.objects.filter(title=value).exclude(id=course_id).exists():
            raise serializers.ValidationError(
                "A course with this title already exists."
            )
        return value

    def validate_status(self, value):
        """Protect against someone sending random status during hacking."""
        allowed = ["pending", "approved", "rejected"]
        if value not in allowed:
            raise serializers.ValidationError("Invalid status value.")
        return value

