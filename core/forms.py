from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

region = {

    ('Ar', 'Arusha'),
    ('Dar', 'Dar es salaam'),
    ('Mw', 'Mwanza'),
    ('Mb', 'Mbeya'),

}


class CheckoutForm(forms.Form):
    country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    region = forms.ChoiceField(choices=region)
    payment_option = forms.CharField()
