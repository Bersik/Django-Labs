from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import Shop.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', Shop.views.home),
    url(r'^home/', Shop.views.home),
    url(r'^home', Shop.views.home),

    url(r'^order', Shop.views.order),
    url(r'^complete', Shop.views.complete),

    url(r'^buy', Shop.views.buy),
    url(r'^remove', Shop.views.remove),

    #  Filtration
    url(r'^producer', Shop.views.producer),
    url(r'^operation_systems', Shop.views.operation_systems),
    url(r'^type_phone', Shop.views.type_phone),
    url(r'^cost', Shop.views.cost),
    url(r'^multimedia', Shop.views.multimedia),
]

urlpatterns += staticfiles_urlpatterns()
