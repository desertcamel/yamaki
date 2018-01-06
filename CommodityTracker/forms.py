from django import forms
from django.forms import ModelForm
from CommodityTracker.models import PurchaseCommodity 
from django.utils.translation import gettext_lazy as _


class PurchaseCommodityForm(forms.ModelForm):

    commodity_purchase_data  = forms.FileField(help_text = 'Upload csv file ')
    class Meta:
        model = PurchaseCommodity
        fields = ('company_name', 
                    'name', 
                    'description', 
                    'benchmark1', 
                    'weight1', 
                    'benchmark2', 
                    'weight2', 
                    'benchmark3', 
                    'weight3' 
        )

        labels = {
            'company_name': _('Enter Company Name'),
        }

        help_texts = {
            'company_name': _('Write Your Company Name.'),
        }

    
