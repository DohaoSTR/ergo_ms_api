from django.urls import path
from src.external.learning_analytics.forecasting_module.views import (
    SpecialityGetView,
    SendSpecialityView,
    DisciplineGetView,
    SendDisciplineView,
    AcademicCompetenceMatrixGetView,
    SendAcademicCompetenceMatrixView,
    CompetencyProfileOfVacancyGetView,
    SendCompetencyProfileOfVacancy
)

urlpatterns = [
    path('specialities/', SpecialityGetView.as_view(), name='specialities'),
    path('send_specialitiy/', SendSpecialityView.as_view(), name='send_speciality'),
    path('disciplines/', DisciplineGetView.as_view(), name='disciplines'),
    path('send_disciplines/', SendDisciplineView.as_view(), name='send_discipline'),
    path('academic_competence_matrix/', AcademicCompetenceMatrixGetView.as_view(), name='academic_competence_matrix'),
    path('send_academic_competence_matrix/', SendAcademicCompetenceMatrixView.as_view(), name='send_academic_competence_matrix'),
    path('competency_profiles_of_vacancies/', CompetencyProfileOfVacancyGetView.as_view(), name='competency_profiles_of_vacancies'),
    path('send_competency_profiles_of_vacancies/', SendCompetencyProfileOfVacancy.as_view(), name='send_competency_profiles_of_vacancies'),
]