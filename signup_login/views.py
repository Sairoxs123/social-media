from django.shortcuts import render, redirect
from .forms import SignupForm
from core.models import Users

# Create your views here.

def signup(request):

    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        error = False
        name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get("password")
        photo = request.POST.get("photo")
        results = Users.objects.all()

        for i in results:
            if email == i.email:
                error = "email"
                break

            elif name == i.username:
                error = "username"
                break

            else:
                error = False

        if error == "email":
            return render(request, 'signup/index.html', {'message' : 'email-exists'})

        if error == "username":
            return render(request, 'signup/index.html', {'message' : 'username-exists'})

        if error == "toolong":
            return render(request, 'signup/index.html', {'message' : 'toolong'})

        try:
            form.save()
            request.session["email"] = email
            request.session["username"] = name
            request.session["logged-in"] = True
            return redirect("/account/login")

        except:
            Users(username=name, email=email, password=password).save()
            request.session["email"] = email
            request.session["username"] = name
            request.session["logged-in"] = True
            return redirect("/")

    return render(request, 'signup/index.html', {"form":SignupForm})

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        results = Users.objects.all().filter(username=username)

        if results:
            for i in results:
                if password == i.password:
                    request.session["logged-in"] = True
                    request.session["id"] = i.id
                    request.session["username"] = i.username
                    request.session["email"] = i.email
                    if not i.photo:
                        request.session["filename"] = "default"
                    else:
                        request.session["filename"] = i.photo.url
                    return redirect("/")

                else:
                    return render(request, "login/message.html", {"message": "wrongpassword"})

        else:
            return render(request, "login/message.html", {"message": "account-no-exist"})

    if request.session.get("logged-in"):
        return redirect("/")

    return render(request, "login/index.html")
