from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Education, Experience


class ExperienceSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id", "started_at", "ended_at"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        cleaned_value = strip_tags(value).strip()
        if not cleaned_value:
            raise serializers.ValidationError("Description cannot be empty.")
        return cleaned_value

    def validate_category(self, value):
        return strip_tags(value).strip()

    def validate_thumbnail(self, value):
        if value is None or value == "":
            return value
        return strip_tags(value).strip()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class EducationSerializer(serializers.ModelSerializer):
    year_started = serializers.SerializerMethodField()
    year_ended = serializers.SerializerMethodField()
    is_ongoing = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields = [
            "id",
            "institution",
            "degree",
            "field_of_study",
            "started_at",
            "ended_at",
            "year_started",
            "year_ended",
            "is_ongoing",
        ]
        read_only_fields = ["id", "started_at", "year_started", "year_ended", "is_ongoing"]

    def validate_institution(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Institution cannot be empty.")
        return value

    def validate_field_of_study(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Field of study cannot be empty.")
        return value

    def validate_degree(self, value):
        return strip_tags(value).strip()

    def get_year_started(self, obj):
        return obj.get_year_started()

    def get_year_ended(self, obj):
        return obj.get_year_ended()

    def get_is_ongoing(self, obj):
        return obj.is_ongoing


__all__ = ["EducationSerializer", "ExperienceSerializer"]
