from django.urls import path
from .endpoint import views, auth_views



urlpatterns = [

    # Google
    path('', auth_views.google_login),
    path('google-callback/', auth_views.google_auth),

    # Spotify
    path('spotify-login/', auth_views.spotify_login),
    path('spotify-callback/', auth_views.spotify_auth),

    path('me/', views.UserView.as_view({'get': 'retrieve', 'put': 'update'})),
    path('author/', views.AuthorView.as_view({'get': 'list'})),
    path('author/<int:pk>/', views.AuthorView.as_view({'get': 'retrieve'})),

    path('social/', views.SocialLinkView.as_view({'get': 'list', 'post': 'create'})),
    path('social/<int:pk>/', views.SocialLinkView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
