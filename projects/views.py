from django.shortcuts import render

#home view to render projects on the index page
def index(request):
    projects = Project.get_projects()
    context={
        'projects' : projects,
    }
    return render(request,"index.html", context)

#profile view to query users by id and display them
@login_required(login_url='/accounts/login/')
def profile(request,profile_id):
    profile = Profile.objects.get(pk = profile_id)
    project = Project.objects.filter(profile_id=profile).all()
    
    context = {
        'profile':profile,
        'project':project
    }
    return render(request,"profile.html", context)

#profile view funcion with a for loopto loop through all profiles and display them by id
@login_required(login_url='/accounts/login/')
def project(request):
    current_user = request.user
    profiles = Profile.get_profile()
    for profile in profiles:
        if profile.user.id == current_user.id:
            if request.method == 'POST':
                form = ProjectForm(request.POST,request.FILES)
                if form.is_valid():
                    new_project = form.save(commit=False)
                    new_project.author = current_user
                    new_project.profile = profile
                    new_project.save()
                    return redirect('home')
            else:
                form = ProjectForm()
                
            context = {
                'user':current_user,
                'form':form
            }
            return render(request,'project.html', context)

@login_required(login_url='/accounts/login/')
def project(request):
    current_user = request.user
    profiles = Profile.get_profile()
    for profile in profiles:
        if profile.user.id == current_user.id:
            if request.method == 'POST':
                form = ProjectForm(request.POST,request.FILES)
                if form.is_valid():
                    project = form.save(commit=False)
                    project.author = current_user
                    project.profile = profile
                    project.save()
                    return redirect('home')
            else:
                form = ProjectForm()
                
                context = {
                    'user':current_user,
                    'form':form
                }
            return render(request,'project.html', context)

@login_required(login_url='/accounts/login/')
def new_profile(request):
    project = Project.objects.filter(author=request.user).order_by('-date_posted')
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'project' : project
    }
    return render(request, 'profile/profile.html', context)