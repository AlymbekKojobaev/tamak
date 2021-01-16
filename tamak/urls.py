"""tamak URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from main import views as main_views
from reservation import views as order_views
from teams import views as teams_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('teams/', include('teams.urls')),
    path('reservation/', include('reservation.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logout.html'), name='logout'),
    path('registration/', main_views.registration, name='registration'),
    path('feedbacks/', main_views.FeedbackListView.as_view(), name='feedback'),
    path('feedback/<int:pk>/', main_views.FeedbackDetailView.as_view(), name='feedback-details'),
    path('feedback/delete/<int:pk>/', main_views.FeedbackDeleteView.as_view(), name='feedback-delete'),
    path('feedback/create/', main_views.FeedbackCreateView.as_view(), name='feedback-create'),
    path('feedback/update/<int:pk>/', main_views.FeedbackUpdateView.as_view(), name='feedback-update'),

##########################################################################################################

    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/get_create_user/', main_views.UserCreateAPIView.as_view(), name='get-create-users-api'),
    path('api/v1/get_all_user/', main_views.UserListAPIView.as_view(), name='get-all-users-api'),
    path('api/v1/get_update_user/', main_views.UserUpdateAPIView.as_view(), name='get-update-users-api'),
    path('api/v1/get_delete_user/', main_views.UserDeleteAPIView.as_view(), name='get-delete-users-api'),
    path('api/v1/all_feedback/', main_views.FeedbackCreateAPIView.as_view(), name='all-feedback-api'),
    path('api/v1/update_feedback/', main_views.FeedbackUpdateAPIView.as_view(), name='update_feedback'),
    path('api/v1/delete_feedback/', main_views.FeedbackDeleteAPIView.as_view(), name='delete_feedback'),
    path('api/v1/all_comment/', main_views.CommentCreateAPIView.as_view(), name='all-comment-api'),
    path('api/v1/update_comment/', main_views.CommentUpdateAPIView.as_view(), name='update_comment'),
    path('api/v1/delete_comment/', main_views.CommentDeleteAPIView.as_view(), name='delete_comment'),
    path('api/v1/all_order/', order_views.OrderCreateAPIView.as_view(), name='all-order-api'),
    path('api/v1/update_order/', order_views.OrderUpdateAPIView.as_view(), name='update_order'),
    path('api/v1/delete_order/', order_views.OrderDeleteAPIView.as_view(), name='delete_order'),
    path('api/v1/all_teams/', teams_views.CookCreateAPIView.as_view(), name='all-teams-api'),
    path('api/v1/update_teams/', teams_views.CookUpdateAPIView.as_view(), name='update_teams'),
    path('api/v1/delete_teams/', teams_views.CookDeleteAPIView.as_view(), name='delete_teams')
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)
