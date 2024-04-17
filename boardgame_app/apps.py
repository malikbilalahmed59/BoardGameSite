# your_project_name/your_app_name/apps.py
from django.apps import AppConfig
from django.contrib.auth.decorators import login_required as auth_login_required

class BoardgameAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'boardgame_app'

    def ready(self):
        # Importing models here to avoid circular import
        from .models import Game, Reservation, Cafe
        from django.contrib.auth.forms import UserCreationForm

        def index(request):
            games = Game.objects.all()
            return render(request, 'index.html', {'games': games})

        @auth_login_required
        def profile(request):
            user_games = Game.objects.filter(time__gt=timezone.now())
            return render(request, 'profile.html', {'user_games': user_games})

        @auth_login_required
        def reserve(request):
            if request.method == 'POST':
                form = ReservationForm(request.POST)
                if form.is_valid():
                    # Process the reservation logic here
                    # e.g., Save reservation to the database
                    form.save()
                    messages.success(request, 'Reservation successful!')
                    return redirect('profile')
            else:
                form = ReservationForm()

            return render(request, 'reserve.html', {'form': form})

        @auth_login_required
        def cafe_profile(request):
            if request.method == 'POST':
                form = CafeProfileForm(request.POST)
                if form.is_valid():
                    # Process the cafe profile update logic here
                    # e.g., Update cafe details in the database
                    form.save()
                    messages.success(request, 'Cafe details updated successfully!')
                    return redirect('cafe_profile')
            else:
                form = CafeProfileForm()

            return render(request, 'cafe_profile.html', {'form': form})

        def user_login(request):
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('profile')
                else:
                    messages.error(request, 'Invalid username or password. Please try again.')

            return render(request, 'signin.html')

        def user_logout(request):
            logout(request)
            return redirect('index')

        def user_register(request):
            if request.method == 'POST':
                form = UserCreationForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Account created successfully! Please log in.')
                    return redirect('signin')
            else:
                form = UserCreationForm()

            return render(request, 'register.html', {'form': form})

        @auth_login_required
        def cafe_register(request):
            # Add logic for cafe registration (if needed)
            return render(request, 'cafe_register.html')
