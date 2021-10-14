from django.urls import path

from expiring_links.views import ExpiringLinkView

expiring_link_create = ExpiringLinkView.as_view({'post': 'create'})
expiring_link = ExpiringLinkView.as_view({'get': 'retrieve'})
urlpatterns = [
    path('links/', expiring_link_create),
    path('links/<str:token>', expiring_link),
]
