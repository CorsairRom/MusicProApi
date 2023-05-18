from django.urls import path, include

urlpatterns = [
    path('', include('api.router'), name='musicPro_router'),
]