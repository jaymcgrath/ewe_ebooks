from django import forms

class MemberForm(forms.ModelForm):
    class Meta:
        model = 'people.Member'
        fields = ('offline_name', 'email', 'bio', 'dob')
