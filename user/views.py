from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer
from .forms import RegistrationForm

# Create your views here.
class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

#frontend requirement
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user_data=form.save(commit=False)
            user_data.set_password(form.cleaned_data['password'])
            user_data.save()   

        messages.success(request,'account created successfully')
        return redirect('login')
    else:
        form = RegistrationForm()   
    return render(request,'register.html',{'form':form})

def login_view(request):
    if request.method == 'POST':

        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request,user)
            messages.success(request,'Login successful')
            return redirect('blog_list')
        else:
            messages.error(request,'Invalid credentials')
            return redirect('login')
        
    return render(request,'login.html')        

def logout_view(request):
    logout(request)
    messages.success(request,'Logged out successfully')
    return redirect('login')
