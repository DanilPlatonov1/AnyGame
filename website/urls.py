from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name='pins'),
    path('pin/<int:pin_id>/', ShowPin.as_view(), name='pin'),
    path('collections/', CollectionsPage.as_view(), name='collections'),
    path('collection/<int:collection_id>/', ShowCollection.as_view(), name='collection'),
    path('add_project/', AddProject.as_view(), name='add_project'),

    path('profile/<int:profile_id>/', ProfilePage.as_view(), name='profile'),
    path('follow/<int:profile_id>/', follow, name='follow'),
    path('unfollow/<int:profile_id>/', unfollow, name='unfollow'),
    path('followers/', ShowFollowers.as_view(), name='followers'),
    path('following/', ShowFollowing.as_view(), name='following'),

    path('search/', SearchPage.as_view(), name='search'),
    path('change_profile/', ChangeProfile.as_view(), name='change_profile'),
    path('pin/<int:pk>/update/', UpdatePin.as_view(), name='pin_update'),
    path('pin/<int:pk>/delete/', DeletePin.as_view(), name='pin_delete'),

    path('pin/<int:pin_id>/like/', LikePin.as_view(), name='like_pin'),
    path('add_collection/', AddCollection.as_view(), name='add_collection'),
    path('collection/<int:pk>/delete/', DeleteCollection.as_view(), name='collection_delete'),

    path('add_comment/', add_comment, name='add_comment'),
    path('comment/<int:pk>/delete/', DeleteComment.as_view(), name='comment_delete'),
    path('pin/<int:pin_id>/report/', report_view, name='report_post'),

    path('notifications/', notifications_list, name='notifications_list'),
    path('notifications/read/<int:notification_id>/', mark_as_read, name='mark_as_read'),

    path('about_project/', about_project, name='about_project'),
]
