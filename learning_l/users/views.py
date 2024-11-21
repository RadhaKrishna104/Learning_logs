from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    # If the method is GET, create a blank form
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        
        # If the form is valid, save the new user and log them in
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('learning_logs:index')  # Redirect to a different page after login
        else:
            # If the form is invalid, re-render with errors
            
            return render(request, 'registration/register.html', context)
    
    # If it's a GET request, render with the blank form]
    context = {'form': form}
    return render(request, 'registration/register.html', {'form': form})

def logout(request):
    return render(request, 'registration/logged_out.html')