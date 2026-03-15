from django import forms


class ExcelImportForm(forms.Form):
    file = forms.FileField(label="Arquivo Excel (.xlsx)")
