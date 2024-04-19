# your_project_name/your_app_name/urls.py
# your_project_name/your_app_name/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from .views import index, profile, reserve, cafe_profile, user_login, user_logout, CustomLoginView, register, add_game, \
    edit_game, delete_game, game_detail

urlpatterns = [
    path('', index, name='index'),
    path('cafe_owner/', index, name='cafe_owner'),
    path('profile/', profile, name='profile'),
    path('reserve/', reserve, name='reserve'),
    path('cafe_profile/', cafe_profile, name='cafe_profile'),
    path('register/', register, name='user_register'),
    # path('cafe_register/', cafe_register, name='cafe_register'),
    path('login/', user_login, name='login'),
     path('logout/', user_logout, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('add_game/', add_game, name='add_game'),
    path('edit_game/<int:game_id>/', edit_game, name='edit_game'),
    path('delete_game/<int:game_id>/', delete_game, name='delete_game'),
    path('game/<int:game_id>/', game_detail, name='game_detail'),

]

