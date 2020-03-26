from django.urls import path

from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.acc_logout, name='logout'),
    path('account/', views.account, name='account'),
    path('account/edit/', views.account_edit, name='account_edit'),
    #path('email/edit/', views.email_edit, name='email_edit'),
    path('search/', views.search_result, name='search_results')
]
