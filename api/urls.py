from django.urls import path, include
from api.views import Login, Logout


urlpatterns = [
    path('', include('api.router'), name='musicPro_router'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]