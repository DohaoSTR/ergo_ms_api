from django.urls import path
from src.external.learning_analytics.views import (
    TechnologyGetView,
    CompetentionGetView,
    SendTechnologyView,
    SendCompetentionView
)

urlpatterns = [
    path('technologies/', TechnologyGetView.as_view(), name='technologies'),
    path('send_technologies/', SendTechnologyView.as_view(), name='send_technologies'),
    path('competentions/', CompetentionGetView.as_view(), name='competentions'),
    path('send_competentions/', SendCompetentionView.as_view(), name='send_competentions'),
]