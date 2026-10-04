from django.urls import path
from .views import (
    SkillListingListView,
    SkillListingDetailView,
    SkillListingCreateView,
    SkillListingUpdateView,
    SkillListingDeleteView,
)

urlpatterns = [
    path('', SkillListingListView.as_view(), name='listing_list'),
    path('create/', SkillListingCreateView.as_view(), name='listing_create'),
    path('<int:pk>/', SkillListingDetailView.as_view(), name='listing_detail'),
    path('<int:pk>/edit/', SkillListingUpdateView.as_view(), name='listing_update'),
    path('<int:pk>/delete/', SkillListingDeleteView.as_view(), name='listing_delete'),
]
