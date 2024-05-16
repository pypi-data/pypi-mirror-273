from django.urls import path

from juntagrico_pg import views

app_name = 'jpg'
urlpatterns = [
    path('jpg/home', views.home, name='home'),
    path('jpg/sql', views.execute_sql, name='sql')
]
