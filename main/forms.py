from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea, URLInput, DateTimeInput
from django.utils.html import strip_tags

from main.models import Experience, Education

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            'title',
            'description',
            'thumbnail',
            'ended_at',
        ]

        labels = {
            "title": "Nama Pengalaman",
            "description": "Deskripsi Pengalaman",
            "thumbnail": "URL Thumbnail Pengalaman",
            "ended_at": "Tanggal Selesai Pengalaman",
        }

        widgets = {
            'title': TextInput(
                attrs={
                    "placeholder": "Web Developer ARUNG",
                    "maxlength": 255,
                }
            ),
            'description': Textarea(
                attrs={
                    "placeholder": "Ceritakan Pengalamanmu",
                    "rows": 3,
                }
            ),
            'thumbnail': URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
            'ended_at': DateTimeInput(
                attrs={
                    "placeholder": "2026-12-31",
                    "format": "%Y-%m-%d",
                    "type": "datetime-local",
                }
            )
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama pengalaman tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            'institution',
            'degree',
            'field_of_study',
            'started_at',
            'ended_at',
        ]

        labels = {
            "institution": "Nama Institusi",
            "degree": "Jenjang Pendidikan",
            "field_of_study": "Nama Jurusan/Peminatan",
            "started_at": "Tanggal Mulai Pengalaman",
            "ended_at": "Tanggal Selesai Pengalaman",
        }

        widgets = {
            'institution': TextInput(
                attrs={
                    "placeholder": "Universitas Indonesia",
                    "maxlength": 255,
                }
            ),
            'degree': TextInput(
                attrs={
                    "placeholder": "Bachelor",
                    "maxlength": 20,
                }
            ),
            'field_of_study': TextInput(
                attrs={
                    "placeholder": "Ilmu Komputer",
                    "maxlength": 255,
                }
            ),
            'started_at': DateTimeInput(
                attrs={
                    "placeholder": "2025-08-25",
                    "format": "%Y-%m-%d",
                    "type": "datetime-local",
                }
            ),
            'ended_at': DateTimeInput(
                attrs={
                    "placeholder": "2029-6-28",
                    "format": "%Y-%m-%d",
                    "type": "datetime-local",
                }
            ),
        }