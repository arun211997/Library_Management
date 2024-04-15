from django import forms
global name

class LoginForm(forms.Form):
    username=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','label':None}))
    password=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'password','label':None}))
    
    def clean(self):
        cleaned_data = super().clean()
        name_data=self.cleaned_data['name']
        password_data=self.cleaned_data['password']
        if any(c.isupper() for c in email_data):  
            raise forms.ValidationError("email should not contain an uppercase")
        
        if len(password_data)<8:
           raise forms.ValidationError("paassword should contain min 8 characters")

        if sum(c.isdigit() for c in password_data) < 1:
            raise forms.ValidationError("paassword should contain a number")

        if not any(c.isupper() for c in password_data):  
            raise forms.ValidationError("paassword should contain an uppercase")
        
        if not any(char in Special for char in password_data):
            raise forms.ValidationError('Password should have at least one of the symbols $@#')