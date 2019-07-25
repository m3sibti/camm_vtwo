from django.urls import path
from .views import PaperListView, PaperListView2, PaperListView3
from . import views

urlpatterns = [
    path('', PaperListView.as_view(), name='camm-home'),
    path('graphPrac', PaperListView2.as_view(), name='camm-graph'),
    path('graphRef', PaperListView3.as_view(), name='camm-graph-ref'),
    path('about', views.about_view, name='camm-about'),
]
