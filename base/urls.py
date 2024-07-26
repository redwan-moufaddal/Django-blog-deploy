
from django.urls import path
from . import views

app_name = "base"

urlpatterns = [
    path('', views.home_page, name="home"),
    path('auth/register', views.register, name="register"),
    path('auth/login', views.login_view, name="login"),
    path('auth/logout', views.logout_user, name="logout"),
    path('news/', views.blog_style1_page, name="all_news_default"),
    path('custom-news/', views.blog_style2_page, name="all_news_custom"),
    path('article/<title>?<aid>/', views.article_detail, name="article_detail"),
    path('contact/', views.contact_page, name="contact"),
    path('about/', views.about_page, name="about"),
    path('articles/<str:category>/', views.articles_by_category, name='articles_by_category'),
    path('search/', views.search_results, name='search_results'),
]
