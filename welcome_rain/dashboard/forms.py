


from django import forms

class hostForms(forms.Form):
    ip = forms.IPAddressField(
        label = 'Ip',
    )
    description = forms.Field(
        label = 'Description',
        widget = forms.TextInput()
    )