from django.urls import path

from src.external.tools.generator.views import GenerateListView
urlpatterns = [
    path('random-list/', GenerateListView.as_view(), name="random-list")
]