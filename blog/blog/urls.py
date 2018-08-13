from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('',
        views.post_list,
        name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>',
        views.post_detail,
        name='post_detail'),
]

# slug: a string consisting of ASCII letters or numbers, plus the hyphen and underscore characters