from django.urls import path, register_converter
from datetime import datetime
from . import views
from django.conf.urls.static import static
from django.conf import settings

class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value

register_converter(DateConverter, 'yyyy')

urlpatterns = [
    path('', views.home, name='home'),
    path('user', views.user, name='user'),
    path('log_in/', views.log_in, name='log_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('log_out', views.log_out, name='log_out'),
    path('index', views.index, name='index'),
    path('blogs', views.blog, name='blog'),
    path('create_blog/', views.create_blog, name='create_blog'),
    path('blog/<int:pk>', views.blog_content, name='blog_content'),
    path('post/<int:pk>', views.post_content, name='post_content'),
    path('create_post/<int:pk>', views.create_post, name='create_post'),
    path('add_comment/<int:pk>', views.add_comment, name='add_comment'),
    path('delete_post/<int:pk>', views.delete_post, name='delete_post'),
    path('delete_blog/<int:pk>', views.delete_blog, name='delete_blog'),
    path('edite_post/<int:pk>', views.edite_post, name='edite_post'),
    path('edite_blog/<int:pk>', views.edite_blog, name='edite_blog'),
    path('search', views.search_s, name='search_s'),
    path('search_form', views.search_form, name='search_form'),
    path('search/<str:str>', views.search_results, name='search_results'),
    path('search/<str:title>/<str:author>/<date>', views.search_ss, name='search_ss'),
    path('author/<str:str>', views.user, name='user'),
    path('get_password/<int:pk>', views.get_password, name='get_password'),
    path('post_password/<int:pk>', views.post_password, name='post_password'),
    path('edite_password/<int:pk>', views.edite_password, name='edite_password'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)