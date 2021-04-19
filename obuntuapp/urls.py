from django.conf.urls import url
from rest_framework.authtoken import views as drf_views

from . import views
app_name = 'guide'

urlpatterns = [
    #auth/
    url(r'^auth/$', drf_views.obtain_auth_token, name='auth'),

    #obuntu/login
    url(r'^login/$',views.Login.as_view(), name = 'login'),

    #obuntu/signin
    url(r'^signin/$',views.Signin.as_view(), name = 'signin'),

    #obuntu/signup
    url(r'^signup/$',views.Signup.as_view(), name = 'signup'),

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
    url(r'^ward/(?P<lga>[0-9]+)$',views.WardView.as_view(), name = 'ward-view'),

    #obuntu/pollingunits
    url(r'^pollingunits/(?P<ward>[0-9]+)/$',views.PolllingUnitView.as_view(), name = 'polling-unit-view'),

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

    #obuntu/follow
    url(r'^follow/(?P<id>[0-9]+)/$',views.FollowView.as_view(), name = 'follow-view'),

    #obuntu/update_account
    url(r'^update_account/$',views.UpdateAccount.as_view(), name = 'update-account'),

    #obuntu/user_search
    url(r'^user_search/$',views.UserSearch.as_view(), name = 'user-search'),

    #obuntu/video_category
    url(r'^video_category/$',views.VideoCategoryView.as_view(), name = 'video-category-view'),
    
    #obuntu/chat
    url(r'^chat/(?P<id>[0-9]+)/$',views.ChatView.as_view(), name = 'chat-view'),

]