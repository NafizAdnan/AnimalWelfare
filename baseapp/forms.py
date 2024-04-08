from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Search')
    sort_by = forms.ChoiceField(choices=[('price_low_to_high', 'Price (Low to High)'), ('price_high_to_low', 'Price (High to Low)')], required=False)
