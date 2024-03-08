from django.urls import path
from django.views.decorators.cache import cache_page

from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='blog'),
    path('contacts/', cache_page(60)(ContactsPageView.as_view()), name='contacts'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('view/<int:pk>/', PostDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', PostUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='delete'),
    path('subscription/', SubscriptionPageView.as_view(), name='subscription'),
    path('subscription_success/', SubscriptionSuccessPageView.as_view(), name='subscription_success')
]
