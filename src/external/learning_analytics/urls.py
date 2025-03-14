from django.urls import path

# Импортируем представления данных для определения путей к ним
from src.external.learning_analytics.views import (
    TechnologyGetView,
    CompetentionGetView,
    EmployerGetView,
    SendTechnologyView,
    SendCompetentionView,
    SendEmployerView
)

urlpatterns = [
    path('technologies/', TechnologyGetView.as_view(), name='technologies'),
    path('send_technologies/', SendTechnologyView.as_view(), name='send_technologies'),
    path('competentions/', CompetentionGetView.as_view(), name='competentions'),
    path('send_competentions/', SendCompetentionView.as_view(), name='send_competentions'),
    path('employers/', EmployerGetView.as_view(), name='employers'),
    path('send_employers/', SendEmployerView.as_view(), name='send_employers'),
]