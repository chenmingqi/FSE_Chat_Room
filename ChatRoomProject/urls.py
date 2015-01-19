from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ChatRoomProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^logout$', 'ChatRoom.views.logout_view'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'ChatRoom.views.welcome', name='welcome'),
    url(r'^sign$', 'ChatRoom.views.sign', name='sign'),
    url(r'^chatroom$', 'ChatRoom.views.chatroom', name='chatroom'),
    url(r'^ajax_refresh/(?P<last_updated>\d+)$', 'ChatRoom.views.ajax_refresh'),
    url(r'^max_chat_id', 'ChatRoom.views.max_chat_id'),
)
