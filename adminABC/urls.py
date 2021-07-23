from django.conf.urls import url
from rest_framework.authtoken import views as drf_views

from . import views
app_name = 'adminABC'

urlpatterns = [
    #auth/
    url(r'^auth/$', drf_views.obtain_auth_token, name='auth'),

    #apc/recordpolls
    url(r'^recordpolls/$',views.RecordPollingUnits.as_view(), name = 'record-polling-units'),

    #apc/signup
    url(r'^signup/$',views.Signup.as_view(), name = 'signup'),

    #apc/signin
    url(r'^signin/$',views.Signin.as_view(), name = 'signin'),

    #apc/userdata
    url(r'^userdata/$',views.FetchUser.as_view(), name = 'userdata'),

    #apc/lgas
    url(r'^lgas/$',views.LgaView.as_view(), name = 'lga-view'),

    #apc/ward
    url(r'^ward/(?P<lga>[0-9]+)$',views.WardView.as_view(), name = 'ward-view'),

    #apc/pollingunits
    url(r'^pollingunits/(?P<ward>[0-9]+)/$',views.PolllingUnitView.as_view(), name = 'polling-unit-view'),

    #apc/update
    url(r'^update/$',views.UpdateAccount.as_view(), name = 'update-account'),

    #apc/user
    url(r'^user/$',views.UserView.as_view(), name = 'user-view'),

    #apc/filterbylga
    url(r'^filterbylga/$',views.FilterByLga.as_view(), name = 'filter-by-lga'),

    #apc/filterbyward
    url(r'^filterbyward/$',views.FilterByWard.as_view(), name = 'filter-by-ward'),

    #apc/filterbylga
    url(r'^filterbypoll/$',views.FilterByPoll.as_view(), name = 'filter-by-poll'),

]