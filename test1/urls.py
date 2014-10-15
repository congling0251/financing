from django.conf.urls import include, url
from django.contrib import admin
import settings
from test1 import views


urlpatterns = [
    # Examples:
    # url(r'^$', 'test1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.home),
    url(r'^login/', views.login),
    url(r'^login-form/', views.login_form),
    url(r'^logout/', views.logout),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', views.home),
    url(r'^decide/$', views.decide),
    url(r'^decide-form/$', views.decide_form),
    url(r'^count/$', views.count),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_URL}),
]