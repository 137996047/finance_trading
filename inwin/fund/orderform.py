'''
Created on 2013/2/13

@author: yhuang
'''
from django import forms
 
from django.utils.translation import ugettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, MultiField, Div, Field,Button
from crispy_forms.bootstrap import AppendedText,FormActions

TSTYPE_CHOICES = (
                                ('1', _('purchase')),
                                ('2', _('withdraw')),
                                ('3', _('dividend')),
                                ('4', _('interest')),
                           )
class orderform(forms.Form):
    F_Date= forms.DateTimeField(label=_('Trading Date'),)
    F_SKID= forms.CharField(label=_('FundID'),max_length=8)
    F_TSType= forms.ChoiceField(label=_('Trading Type'),choices=TSTYPE_CHOICES)
    F_CurID=forms.CharField(label=_('Currency'),max_length=8)
    F_Amt=forms.DecimalField(label=_('Amount'),max_digits=28, decimal_places=4)
    F_Qty=forms.DecimalField(label=_('Quantity'),max_digits=28, decimal_places=4)
    F_Rate=forms.DecimalField(label=_('Rate'),max_digits=28, decimal_places=4)
    F_Nav=forms.DecimalField(label=_('Nav'),max_digits=28, decimal_places=4)
    F_Fee=forms.DecimalField(label=_('Fee'),max_digits=10, decimal_places=4)
    F_Exp=forms.DecimalField(label=_('Expense'),max_digits=10, decimal_places=4)
    F_Payable=forms.DecimalField(label=_('Pay Amount'),max_digits=28, decimal_places=4)
    F_Receivable=forms.DecimalField(label=_('Receive Amount'),max_digits=28, decimal_places=4)
    F_Note=forms.CharField(label=_('Note'),max_length=128)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'orderform'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.layout = Layout(
             MultiField(
                'first arg is the legend of the fieldset',
                Div('F_Date',
                style="background: white;", title="Explication title", css_class="bigdivs"
                ),
                'F_SKID',
                'F_TSType',
                'F_CurID',
                'F_Qty',
                'F_Rate',
                'F_Nav',
                'F_Fee',
                'F_Exp',
                'F_Payable',
                'F_Receivable',
            ),

            AppendedText('F_Amt', '$', active=True),
            Field('F_Note', id="password-field", css_class="passwordfields", title="Explanation"),
            #Field('slider', template="custom-slider.html"),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            ),
            FormActions(
                        Submit('save', 'Save changes'),
                        Button('cancel', 'Cancel')
                        )
        )
        super(orderform, self).__init__(*args, **kwargs)