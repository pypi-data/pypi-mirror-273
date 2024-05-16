from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from . import views
from .sitemaps import PostSitemap, StaticViewSitemap

app_name = 'mediciodental'

sitemaps = {
    "posts": PostSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    # robots.txt는 반드시 가장 먼저
    path('robots.txt', views.robots),
    path('', views.home, name='home'),
    path('mdeditor/', include('mdeditor.urls')),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap",),

    path('terms_of_use/', views.terms, name='terms'),
    path('privacy_policy/', views.privacy, name='privacy'),

    path('<slug>/', views.PostDetailView.as_view(), name='post_detail'),
]
