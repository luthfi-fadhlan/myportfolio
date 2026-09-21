from django.urls import path

from main.views import (
    show_main, 
    show_experience,
    create_experience,
    update_experience,
    delete_experience,
    show_education,
    create_education,
    update_education,
    delete_education,
    get_experiences_json,
    get_educations_json
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),

    path("experience/", show_experience, name="show_experience"),
    path("experience/create/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/update/", update_experience, name="update_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),

    path("education/", show_education, name="show_education"),
    path("education/create/", create_education, name="create_education"),
    path("education/<uuid:education_id>/update/", update_education, name="update_education"),
    path("education/<uuid:education_id>/delete/", delete_education, name="delete_education"),

    path("api/experience/", get_experiences_json, name="get_experiences_json"),
    path("api/education/", get_educations_json, name="get_educations_json")
]