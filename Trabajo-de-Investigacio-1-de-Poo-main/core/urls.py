from django.urls import path
from core.views import (
    list_nomina, create_nomina, update_nomina, delete_nomina,
    login_view, register_view, logout_view
)
app_name = 'core'

urlpatterns = [
    path('list/<str:model_name>/', list_nomina, name='list_nomina'),
    path('create/<str:model_name>/', create_nomina, name='create_nomina'),
    path('update/<str:model_name>/<int:id>/', update_nomina, name='update_nomina'),
    path('delete/<str:model_name>/<int:id>/', delete_nomina, name='delete_nomina'),
    path('login/', login_view, name='login'),
    path('signup/', register_view, name='signup'),
    path('logout/', logout_view, name='logout'),
]