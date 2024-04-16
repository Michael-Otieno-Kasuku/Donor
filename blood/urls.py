from django.contrib import admin
from django.urls import include, path

urlpatterns=[
    path("blood/donor/", include("donor.urls")),
    path("blood/donor/admin/",admin.site.urls),
]