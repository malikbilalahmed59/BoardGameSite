from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.utils import timezone  # Add this line
from .models import Game, Reservation, Cafe, User, GameReview
from .forms import ReservationForm, CafeProfileForm, CustomUserCreationForm, GameForm


def index(request):
    if request.user.is_staff:
        # Retrieve games available for the cafe owned by the staff user
        games = Game.objects.filter(cafe=request.user.cafe)
        return render(request, 'cafe_owner.html', {'games': games})

    # Retrieve all games if the user is not staff
    games = Game.objects.all()
    # for game in games:
    #     print("Game ID:", game.id)
    #     print("Name:", game.name)
    #     print("Description:", game.description)
    #     print("Location:", game.location)
    #     print("Time:", game.time)
    #     print("Available Slots:", game.available_slots)
    #     print("Average Rating:", game.average_rating)
    #     print("Total Ratings:", game.total_ratings)
    return render(request, 'index.html', {'games': games})


@login_required
def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    # Check if the user has already reviewed the game
    user_review = GameReview.objects.filter(user=request.user, game=game).exists()

    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')

        # Only allow users to review the game if they haven't already reviewed it
        if not user_review:
            GameReview.objects.create(user=request.user, game=game, rating=rating, comment=comment)
            game.total_ratings += 1
            game.average_rating = (game.average_rating * (game.total_ratings - 1) + rating) / game.total_ratings
            game.save()
            return redirect('index')
        else:
            # Optionally, you can display a message here indicating that the user has already reviewed the game
            return HttpResponse("You have already reviewed this game.")

    return render(request, 'game_detail.html', {'game': game, 'user_review': user_review})





@login_required
def profile(request):
    if request.user.is_staff:
        cafe = request.user.cafe
        return render(request, 'cafe_profile.html', {'cafe': cafe})
    else:
        user_games = Reservation.objects.filter(user=request.user, reservation_time__gt=timezone.now())
        return render(request, 'profile.html', {'user_games': user_games})


@login_required
def reserve(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST, user=request.user)
        if form.is_valid():
            game = form.cleaned_data['game']
            reservation_time = form.cleaned_data['reservation_time']

            if Game.objects.filter(id=game.id, time=reservation_time).exists():
                reservation = form.save(commit=False)
                reservation.user = request.user
                reservation.save()

                messages.success(request, 'Reservation successful!')
                return redirect('profile')
            else:
                messages.error(request, 'Selected time is not available. Please choose another time.')
        else:
            messages.error(request, 'Invalid form submission. Please check your inputs.')
    else:
        form = ReservationForm(user=request.user)

    return render(request, 'reserve.html', {'form': form})


@login_required
def cafe_profile(request):
    cafe = Cafe.objects.get(owner=request.user)

    if request.method == 'POST':
        form = CafeProfileForm(request.POST, instance=cafe)
        if form.is_valid():
            form.save()
            return redirect('cafe_owner')
    else:
        form = CafeProfileForm(instance=cafe)

    return render(request, 'cafe_profile.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            messages.success(request, 'Login successful!')
            if user.is_staff:
                login(request, user)
                return redirect('cafe_profile')  # Redirect staff users to cafe profile
            else:
                login(request, user)
                return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')


from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['is_staff']:
                user.is_staff = True
                user.save()
                # Create a corresponding cafe instance for staff user
                try:
                    cafe = Cafe.objects.create(owner=user)
                    messages.success(request, 'Account created successfully! Please log in.')
                    # Redirect to the cafe profile page
                    return redirect('cafe_profile')
                except Exception as e:
                    messages.error(request, 'An error occurred while creating cafe profile. Please try again later.')
                    # Log the exception for further investigation
                    print("Error creating cafe profile:", e)
                    return redirect('user_register')
            else:
                user.save()
                messages.success(request, 'Account created successfully! Please log in.')
                # Redirect to the login or home page
                return redirect('index')
    else:
        form = CustomUserCreationForm()

    # Display form errors to the user (if any)
    print("Form errors:", form.errors)
    for field, errors in form.errors.items():
        for error in errors:
            messages.error(request, f'{field}: {error}')

    return render(request, 'register.html', {'form': form})



# def user_register(request):
#     if request.method == 'POST':
#         form = CombinedRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#
#             is_cafe_owner = form.cleaned_data.get('is_cafe_owner', False)
#
#             if is_cafe_owner:
#                 cafe_form = CafeProfileForm(request.POST)
#                 if cafe_form.is_valid():
#                     cafe = cafe_form.save(commit=False)
#                     cafe.owner = user
#                     cafe.save()
#                     messages.success(request, 'Cafe registration successful!')
#                     return redirect('cafe_profile')
#                 else:
#                     messages.error(request, 'Invalid cafe details. Please check your inputs.')
#
#             messages.success(request, 'Account created successfully! Please log in.')
#             return redirect('login')
#         else:
#             messages.error(request, 'Invalid form submission. Please check your inputs.')
#     else:
#         form = CombinedRegistrationForm()
#
#     return render(request, 'register.html', {'form': form})
# def cafe_register(request):
#     if request.method == 'POST':
#         form = CombinedRegistrationForm(request.POST)
#         cafe_form = CafeProfileForm(request.POST)
#
#         if form.is_valid() and cafe_form.is_valid():
#             user = form.save()
#
#             is_cafe_owner = form.cleaned_data.get('is_cafe_owner', False)
#
#             if is_cafe_owner:
#                 cafe = cafe_form.save(commit=False)
#                 cafe.owner = user  # Assign owner after ensuring both forms are valid
#                 cafe.save()
#                 messages.success(request, 'Cafe registration successful!')
#                 return redirect('cafe_profile')
#             else:
#                 messages.error(request, 'Invalid form submission. Please check your inputs.')
#         else:
#             messages.error(request, 'Invalid form submission. Please check your inputs.')
#     else:
#         form = CombinedRegistrationForm()
#         cafe_form = CafeProfileForm()
#
#     return render(request, 'cafe_register.html', {'form': form, 'cafe_form': cafe_form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'Login successful!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)



@login_required
def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('cafe_owner')
    else:
        form = GameForm(request.user)
    return render(request, 'add_game.html', {'form': form})


@login_required
def edit_game(request, game_id):
    # Retrieve the game instance
    game = get_object_or_404(Game, pk=game_id)

    if game.cafe.owner == request.user:

        if request.method == 'POST':
            form = GameForm(request.user,request.POST, instance=game)
            if form.is_valid():
                print("hello!")

                form.save()
                return redirect('cafe_owner')  # Redirect to the cafe owner page
        else:
            # Populate the form with the existing game instance data
            form = GameForm(instance=game)

        # Render the edit game form template with the form
        return render(request, 'edit_game.html', {'form': form})
    else:
        # Redirect to the cafe profile page if the user is not the owner of the cafe
        return redirect('cafe_profile')


@login_required
def delete_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if game.cafe.owner == request.user:
        game.delete()
        return redirect('cafe_profile')
    else:
        # Redirect or show error message if user is not the owner of the cafe
        return redirect('cafe_profile')
