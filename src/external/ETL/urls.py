from django.urls import path, include

urlpatterns = [
    path('api/analyze/', include('src.external.ETL.analyze.urls')),
]
