from django.urls import path

from .views import AddMicropostView, MicropostDetailView

app_name = 'microposts'

urlpatterns = [
    path('add-post', AddMicropostView.as_view(), name='add_micropost'),
    path('<slug:micropost_slug>', MicropostDetailView.as_view(), name='micropost_detail'),
]
