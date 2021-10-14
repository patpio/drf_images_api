from rest_framework.routers import SimpleRouter

from images import views


router = SimpleRouter()
router.register('images', views.ImageViewSet, basename='images')
router.register('thumbnails', views.ThumbnailViewSet, basename='thumbnails')

urlpatterns = router.urls
