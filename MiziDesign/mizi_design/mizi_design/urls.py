"""mizi_design URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from mizi_app import views
import mizi_app
from django.conf.urls import include 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$',views.store,name='main'),
    url(r'^cart/',views.cart,name='cart'),
    url(r'^contact/',views.contact,name='contact'),
    url(r'^desc/(?P<id>\d+)/$',views.desc,name='desc'),
    url(r'^cust/(?P<id>\d+)/$',views.cust,name='cust'),
    url(r'^login/',views.loginPage,name='login'),
    url(r'^logout/',views.logoutUser,name='logout'),
    url(r'^sign_up/',views.sign_up,name='sign_up'),
    url(r'^forgot_password/',views.forgot_password,name='forgot_password'),
    url(r'^checkout/',views.checkout,name='checkout'),
    url(r'^update_item/',views.updateItem,name='update_item'),
    url(r'^process_order/',views.processOrder,name='process_order'),
    url(r'^admin/', admin.site.urls),
]

urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)