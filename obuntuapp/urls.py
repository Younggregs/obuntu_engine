from django.conf.urls import url
from rest_framework.authtoken import views as drf_views

from . import views
app_name = 'guide'

urlpatterns = [
    #auth/
    url(r'^auth/$', drf_views.obtain_auth_token, name='auth'),

    #obuntu/login
    url(r'^login/$',views.Login.as_view(), name = 'login'),

    #obuntu/superuser
    url(r'^superuser/$',views.IsSuperUser.as_view(), name = 'is-superuser'),

    #obuntu/lgas
    url(r'^lgas/$',views.LgaView.as_view(), name = 'lga-view'),

    #obuntu/admin
    url(r'^admin/$',views.AdminView.as_view(), name = 'admin-view'),

    #obuntu/user
    url(r'^user/$',views.UserView.as_view(), name = 'user-view'),

    #obuntu/location
    url(r'^location/$',views.LocationView.as_view(), name = 'location-view'),

    #obuntu/recordpolls
    url(r'^recordpolls/$',views.RecordPollingUnits.as_view(), name = 'record-polling-units'),

    #obuntu/ward
    url(r'^ward/(?P<lga>\w+)/$',views.WardView.as_view(), name = 'ward-view'),

    #obuntu/pollingunits
    url(r'^pollingunits/(?P<ward>\w+)/$',views.PolllingUnitView.as_view(), name = 'polling-unit-view'),

]