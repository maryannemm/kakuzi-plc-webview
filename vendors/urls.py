from django.urls import path
from .views import VendorFeedbackFormView,VendorHomeTemplateView,RegisterView,CatalogueListView,EditProfileFormView
app_name='vendors'
urlpatterns = [
    path('', VendorHomeTemplateView.as_view(), name='index'),
    path('sign-up', RegisterView.as_view(), name='sign-up'),
    path('catalogue',CatalogueListView.as_view(), name='catalogue'),
    path('edit-profile',EditProfileFormView.as_view(), name='edit-profile'),
    path('farmer/feedback',VendorFeedbackFormView.as_view(), name='vendor-feedback'),
]
