from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import PredictImageView

urlpatterns = [
    path("predict/", csrf_exempt(PredictImageView.as_view()), name="predict_image"),
]
