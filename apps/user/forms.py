from django import forms

from .models import Customer


class CreateProfileForm(forms.ModelForm):
    first_name=forms.CharField(
        widget=forms.TextInput(attrs={"placeholder":"First Name","class":"form-control"}),
        required=True,
    )
    last_name=forms.CharField(
        widget=forms.TextInput(attrs={"placeholder":"Last Name","class":"form-control"}),
        required=True,
    )
    email=forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder":"Email","class":"form-control"}),
        required=True,
    )
    age=forms.IntegerField(
        widget=forms.TextInput(attrs={"placeholder":"Age","class":"form-control"}),
        required=True,
    )
    gender=forms.ChoiceField(
        choices=Customer.Gender,
        widget=forms.Select(attrs={"placeholder":"Gender","class":"form-control genderDropdown"}),
        required=True,
    )
    intrest=forms.CharField(
        widget=forms.TextInput(attrs={"placeholder":"Interest","class":"form-control"}),
        required=True,
    )

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        if commit:
            user_profile.save()
        return user_profile

    class Meta:
        model = Customer  # Replace UserProfile with your actual user profile model
        fields = "__all__"
