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