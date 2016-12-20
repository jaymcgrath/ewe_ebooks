from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView

from people.forms import ProfileForm
from people.models import Profile


# Create your views here.

class ProfileCreateView(CreateView):
    # TODO: Delete if unused
    # Uses proxy method for storing extra user data
    model = Profile
    fields = [
             'offline_name',
             'email',
             'bio',
             'dob'
             ]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['member_form'] = context.get('form')
        user_form = UserCreationForm()
        context.update({'user_form': user_form})
        return context


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('settings:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserCreationForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def create_profile(request):
    if request.method == 'POST':
        user_form = UserCreationForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, 'Your profile was successfully created!')
            return redirect('/dashboard/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        # GET request.. return the form
        user_form = UserCreationForm()
        profile_form = ProfileForm()
    return render(request, 'people/create_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })