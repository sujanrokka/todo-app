from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import TodoForm
from .models import TODO
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q



# Create your views here.
@login_required(login_url="login")
def create(request): 
    form=TodoForm()
    if request.method=='POST':
        # print(request.POST)
        form=TodoForm(request.POST)
        if form.is_valid():
            todo= form.save(commit=False)
            todo.user=request.user
            form.save()
            return redirect('/retrieve')
    return render(request,'create.html',{'form':form})

#retrive operation
def retrieve(request):
    #todos=TODO.objects.all()
    try:
        todos=TODO.objects.filter(user=request.user)
    except:
        todos=[]
    return render(request,'retrieve.html',{'todos':todos})


def update(request,id):
    todos=TODO.objects.get(id=id)
    form=TodoForm(instance=todos)
    if request.user == todos.user:
    
        if request.method=='POST':
                # print(request.POST)
            form=TodoForm(request.POST,instance=todos)
            if form.is_valid():
                form.save()
                return redirect('/retrieve')
        return render(request,'create.html',{'form':form})
    else:
        return HttpResponse("cannot update")

def delete(request,id):
    todos=TODO.objects.get(id=id)
    if request.user == todos.user:
        todos.delete()
        return redirect('retrieve')
    else:
        return redirect('login')
    
    
def register(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        User.objects.create_user(username=username,
                                 password=password,
                                 email=email,
        )
        return redirect('retrieve')
    return render(request, 'register.html')    
    
def loginn(request):
    if request.user.is_authenticated:
        return redirect('retrieve')
    else:
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            user =authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('retrieve')
        return render(request, 'login.html')

def logoutt(request):
    logout(request)
    return redirect('retrieve')

@login_required(login_url="login")
def search(request):
        query=request.GET.get('query')
        if query:
            results=TODO.objects.filter(Q(title__icontains=query) & Q(user=request.user))
        else:
             results=None
        if not results: 
            return render(request, 'no_results.html')
        else:
            return render(request, 'search.html', {'results': results})
        
       