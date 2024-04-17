# your_project_name/your_app_name/forms.py
from django import forms

from .models import Game, Reservation, Cafe, User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    is_staff = forms.BooleanField(required=False, label="Register as Cafe Owner")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('is_staff',)


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['game', 'reservation_time']
        widgets = {
            'reservation_time': forms.DateTimeInput(
                attrs={'class': 'form-control datetimepicker-input', 'id': 'id_time'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Retrieve the user instance from kwargs
        super().__init__(*args, **kwargs)

        if user:
            # Check if the user is a cafe owner
            if hasattr(user, 'cafe'):
                # If the user is a cafe owner, query games offered by the cafe owner and populate the dropdown
                cafe_owner = Cafe.objects.get(owner=user)
                self.fields['game'].queryset = cafe_owner.games_available.all()
            else:
                # If the user is not a cafe owner, display all available games
                self.fields['game'].queryset = Game.objects.all()


class CafeProfileForm(forms.ModelForm):
    class Meta:
        model = Cafe
        fields = ['name', 'location', 'owner', 'description', 'address', 'phone_number', 'email',
                  'website', 'image']
        widgets = {'owner': forms.HiddenInput()}

    # games_offered = forms.ModelMultipleChoiceField(
    #     queryset=Game.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False,
    # )
    # new_game_name = forms.CharField(max_length=255, required=False, label='New Game Name')
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['owner'].disabled = True  # Make the owner field read-only
    #     self.fields['owner'].initial = self.instance.owner  # Set the initial value


#
# class CombinedRegistrationForm(UserCreationForm):
#     is_cafe_owner = forms.BooleanField(
#         label='Register as Cafe Owner',
#         required=False,
#     )
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#
#         # Save the is_cafe_owner field to the user profile
#         user.is_cafe_owner = self.cleaned_data['is_cafe_owner']
#
#         if commit:
#             user.save()
#         return user


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'description', 'location', 'time', 'available_slots']

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.cafe = self.user.cafe
        if commit:
            instance.save()
        return instance
