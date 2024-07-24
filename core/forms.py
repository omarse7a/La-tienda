from django import forms
from .models.bag_models import ShippingInfo

class ShippingInfoForm(forms.ModelForm):
    class Meta:
        model = ShippingInfo
        fields = ['customer_name', 'customer_email', 'customer_number', 'building_no', 'street', 'city', 'governorate', 'landmark']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control square-border', 'placeholder': 'Name', 'required': 'required'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control square-border', 'placeholder': 'Email', 'required': 'required'}),
            'customer_number': forms.TextInput(attrs={'class': 'form-control square-border', 'placeholder': 'Phone', 'required': 'required'}),
            'building_no': forms.NumberInput(attrs={'class': 'form-control square-border', 'placeholder': 'Building no.', 'required': 'required'}),
            'street': forms.TextInput(attrs={'class': 'form-control square-border', 'placeholder': 'Street', 'required': 'required'}),
            'city': forms.TextInput(attrs={'class': 'form-control square-border', 'placeholder': 'City', 'required': 'required'}),
            'governorate': forms.Select(attrs={'class': 'form-select square-border', 'required': 'required'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control square-border', 'placeholder': 'Landmark (optional)'}),
        }
