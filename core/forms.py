from django import forms
from core.models import ProductReview
 
class ProductReviewForm(forms.ModelForm):
  review=forms.CharField(widget=forms.Textarea(attrs={'placeholder':'write a review'}))

  class Meta:
    model=ProductReview
    fields=['review', 'ratings']

