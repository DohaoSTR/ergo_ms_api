from django.urls import path
from src.external.learning_analytics.forecasting_module.views import (
    SpecialityGetView,
    SendSpecialityView,
    DisciplineGetView,
    SendDisciplineView,
    AcademicCompetenceMatrixGetView,
    SendAcademicCompetenceMatrixView
)

urlpatterns = [
    path('specialities/', SpecialityGetView.as_view(), name='specialities'),
    path('send_specialitiy/', SendSpecialityView.as_view(), name='send_speciality'),
    path('disciplines/', DisciplineGetView.as_view(), name='disciplines'),
    path('send_disciplines/', SendDisciplineView.as_view(), name='send_discipline'),
    path('academic_competence_matrix/', AcademicCompetenceMatrixGetView.as_view(), name='academic_competence_matrix'),
    path('send_academic_competence_matrix/', SendAcademicCompetenceMatrixView.as_view(), name='send_academic_competence_matrix')
]