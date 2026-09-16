from django.forms import ModelForm, TextInput, Textarea, URLInput, DateTimeInput

from main.models import Experience

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