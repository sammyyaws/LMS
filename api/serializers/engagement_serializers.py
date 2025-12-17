from rest_framework import serializers
from django.contrib.auth.models import User
from ..Models.engagement_models import Enrollment, Discussion, Feedback



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            'enrollment_id',
            'user',
            'course',
            'date_enrolled',
        ]

    # Ensure a user cannot enroll in the same course twice
    def validate(self, data):
        user = self.context['request'].user
        course = self.initial_data.get('course')

        if Enrollment.objects.filter(user=user, course_id=course).exists():
            raise serializers.ValidationError("You are already enrolled in this course.")
        return data


class DiscussionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = serializers.StringRelatedField(read_only=True)
    lesson = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Discussion
        fields = [
            'discussion_id',
            'user',
            'course',
            'lesson',
            'message',
            'date_created',
            'date_modified',
        ]

    def validate_message(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Message is too short.")
        return value


class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = serializers.StringRelatedField(read_only=True)
    lesson = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Feedback
        fields = [
            'feedback_id',
            'user',
            'course',
            'lesson',
            'content',
            'date_created',
            'date_modified',
        ]

    def validate_content(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Feedback content must be more than 5 characters.")
        return value
