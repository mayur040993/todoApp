try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .views import lists_view,task_list,task_edit,task_view,task_create

urlpatterns=[
        url(r'^list/$',lists_view,name='dashboard'),
        url(r'^tasks/(?P<list_id>[\d-]+)$',task_list,name='task_list'),
        url(r'^create/(?P<list_id>[\d-]+)$',task_create,name='task_create'),
        url(r'^edit/(?P<list_id>[\w-]+)/(?P<task>[\w-]+)$',task_edit,name='task_edit'),
        url(r'^details/(?P<list_id>[\w-]+)/(?P<task>[\w-]+)$',task_view,name='task_view')
]
