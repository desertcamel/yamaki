from django import forms
from django.forms import ModelForm
from CommodityTracker.models import PurchaseCommodity 
from django.utils.translation import gettext_lazy as _

def myvalidate(value):
    print ('###############inside myvalidate function')
    print (value.file)
    # Do something here

        
class PurchaseCommodityForm(forms.ModelForm):

    commodity_purchase_data  = forms.FileField(help_text = 'Upload csv file ', validators=[myvalidate],)
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

    def clean(self):
        cleaned_data = super().clean()
        print ('###############inside clean function')
        

