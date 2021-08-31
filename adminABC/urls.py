from django.conf.urls import url
from rest_framework.authtoken import views as drf_views

from . import views
app_name = 'adminABC'

urlpatterns = [
    #auth/
    url(r'^auth/$', drf_views.obtain_auth_token, name='auth'),

    #apc/recordpolls
    url(r'^recordpolls/$',views.RecordPollingUnits.as_view(), name = 'record-polling-units'),

    #apc/onboard
    url(r'^onboard/$',views.Onboard.as_view(), name = 'onboard'),

    #apc/unboard
    url(r'^unboard/$',views.Unboard.as_view(), name = 'onboard'),

    #apc/membercount
    url(r'^membercount/$',views.MemberCountView.as_view(), name = 'member-count'),

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
    url(r'^pollingunits/(?P<ward>[0-9]+)/$',views.PollingUnitView.as_view(), name = 'polling-unit-view'),

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

    #apc/searchbyname
    url(r'^searchbyname/$',views.SearchByName.as_view(), name = 'search-by-name'),

    #apc/superuser
    url(r'^superuser/$',views.IsSuperUser.as_view(), name = 'is-superuser'),

    #apc/data_entry
    url(r'^data_entry/$',views.DataEntry.as_view(), name = 'data-entry'),



    # Demo urls
    #apc/demo_signup
    url(r'^demo_signup/$',views.DemoSignup.as_view(), name = 'demo-signup'),

    #apc/signin
    url(r'^demo_signin/$',views.DemoSignin.as_view(), name = 'demo-signin'),

    #obuntu/post
    url(r'^post/$',views.PostView.as_view(), name = 'post-view'),

    #obuntu/update_post
    url(r'^update_post/(?P<id>[0-9]+)/$',views.UpdatePost.as_view(), name = 'update-post'),

    #obuntu/like_post
    url(r'^like_post/(?P<id>[0-9]+)/$',views.LikePost.as_view(), name = 'like-post'),

    #obuntu/comment
    url(r'^comment/(?P<id>[0-9]+)/$',views.CommentView.as_view(), name = 'comment-view'),

    #obuntu/remove_comment
    url(r'^remove_comment/(?P<id>[0-9]+)/$',views.RemoveComment.as_view(), name = 'remove-comment'),

    #obuntu/update_account
    url(r'^demo_update_account/$',views.DemoUpdateAccount.as_view(), name = 'demo-update-account'),

    #obuntu/user_search
    url(r'^demo_user_search/$',views.DemoUserSearch.as_view(), name = 'demo-user-search'),

]