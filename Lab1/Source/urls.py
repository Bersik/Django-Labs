from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.models import User, Group
from rest_framework import routers, serializers, viewsets
import Shop.views


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

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

    # REST
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/profile/', Shop.views.login),
]

urlpatterns += staticfiles_urlpatterns()
