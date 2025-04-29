from django.urls import path
from .import views


app_name= 'blog'

urlpatterns = [
    path('',views.landing,name='landing'),
    path('register/',views.register,name='register'),
    path('home/', views.home, name='home'),
    path('about/',views.about,name='about'),
    path('details/<int:pk>/',views.details,name='details'),
    path('contact/',views.contact,name='contact'),
    path('contact/submit/',views.contact_submit,name='contact-submit'),
    path('archives/', views.archives, name='archives'),
    path('popular/', views.popular_posts, name='popular_posts'),
    path('login/',views.login,name='login'),
    path('logout/', views.logout,name='logout'),
    path('create-post/', views.create_post,name='create-post'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete-post/<int:pk>', views.delete_post, name='delete-post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/review/', views.add_review, name='add_review'),

]