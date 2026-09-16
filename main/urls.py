from django.urls import path

from main.views import (
    show_main, 
    show_experience,
    create_experience,
    show_education,
    get_experiences_json,
    delete_experience
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/create/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("education/", show_education, name="show_education"),
    path("api/experience/", get_experiences_json, name="get_experiences_json")
]