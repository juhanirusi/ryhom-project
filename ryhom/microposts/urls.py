from django.urls import path

from .views import (AddMicropostView, AllMicropostsListView,
                    DeleteMicropostView, MicropostDetailView)

app_name = 'microposts'

urlpatterns = [
    path('all', AllMicropostsListView.as_view(), name='all_microposts'),
    path('add-post', AddMicropostView.as_view(), name='add_micropost'),
    path('delete-post/<uuid:micropost_uuid>', DeleteMicropostView.as_view(), name='delete_post'),
    path('<slug:micropost_slug>', MicropostDetailView.as_view(), name='micropost_detail'),
]
