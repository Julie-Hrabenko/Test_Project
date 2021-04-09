from django.urls import path
from .views import (HomePagesView,
                    AboutPagesView,
                    ServicesPagesView,
                    TeamPagesView,
                    ContactPagesView,
                    )

urlpatterns = [
    path('contact/', ContactPagesView.as_view(), name='contact'),
    path('services/', ServicesPagesView.as_view(), name='services'),
    path('about/', AboutPagesView.as_view(), name='about'),
    path('team/', TeamPagesView.as_view(), name='team'),
    path('', HomePagesView.as_view(), name='home'),
]
