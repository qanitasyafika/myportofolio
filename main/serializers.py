from django.utils.html import strip_tags
from rest_framework import serializers
from main.models import Experience, Project

class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "tech_stack",
            "project_url", "project_image_url",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_tech_stack(self, value):
        return strip_tags(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())

class ExperienceSerializer(serializers.ModelSerializer):
    # field hasil hitungan, otomatis read-only jadi nggak bisa dipalsukan dari request
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id", "title", "category", "description",
            "start_date", "end_date",
            "star_count", "is_starred",
        ]
        read_only_fields = ["id"]

    # helper sanitasi, logikanya sama kayak clean_<field> di forms.py Tugas 5
    @staticmethod
    def _clean_text(value, empty_message):
        cleaned = strip_tags(value).strip()
        if not cleaned:
            raise serializers.ValidationError(empty_message)
        return cleaned

    def validate_title(self, value):
        return self._clean_text(value, "Posisi tidak boleh kosong atau hanya berisi tag HTML.")

    def validate_category(self, value):
        return self._clean_text(value, "Kategori tidak boleh kosong atau hanya berisi tag HTML.")

    def validate_description(self, value):
        return self._clean_text(value, "Deskripsi tidak boleh kosong atau hanya berisi tag HTML.")

    def validate(self, attrs):
        # kalau PATCH cuma kirim salah satu tanggal, tanggal satunya diambil dari data lama
        start_date = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end_date = attrs.get("end_date", getattr(self.instance, "end_date", None))
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError(
                {"end_date": "Tanggal selesai tidak boleh lebih awal dari tanggal mulai."}
            )
        return attrs

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        # pengunjung yang belum login selalu dianggap belum ngasih star
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()