from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import *
from .forms import *
from django.template.defaulttags import register
from django.db.models import Q
from datetime import datetime

# Create your views here.

@register.filter

def get_range(value):
    return range(value)

def index(request):

    if not request.session.get("logged-in"):
        return redirect("/account/login")

    useremail = request.session.get("email")
    username = request.session.get("username")
    user = Users.objects.get(email=useremail)

    latest = Messages.objects.all().filter(Q(incoming=user) | Q(outgoing=user)).order_by("-id")

    latestGroups = GroupMessage.objects.all().filter(outgoing=user)

    latestMessages = []

    if len(latest) == 0:
        latestMessages.append("You have no recent messages.")

    else:
        others = []

        for i in latest:
            if i.incoming == user:
                if i.outgoing not in others:
                    others.append(i.outgoing)
                    latestMessages.append(i)

            else:
                if i.incoming not in others:
                    others.append(i.incoming)
                    latestMessages.append(i)

        for i in latestGroups:
            if i.incoming not in others:
                others.append(i.incoming)
                latestMessages.append(i)



    for i in range(len(latestMessages)):
        for j in range(len(latestMessages) - 1):
            date = str(latestMessages[j].message.date).split("-")
            time = str(latestMessages[j].message.time).split(":")
            current_date_time = datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))

            date = str(latestMessages[j+1].message.date).split("-")
            time = str(latestMessages[j+1].message.time).split(":")
            next_date_time = datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))


            if current_date_time < next_date_time:
                latestMessages[j], latestMessages[j+1] = latestMessages[j+1], latestMessages[j]


    if len(latestMessages) > 3:
        latestMessages = latestMessages[:3]

    latestMessagesHTML = []

    for i in latestMessages:
        if i.incoming == user:
            sender = i.outgoing.username
            name = i.outgoing.username
            if i.outgoing.photo:
                pfp = i.outgoing.photo.url

            else:
                pfp = '<img src="https://t4.ftcdn.net/jpg/05/89/93/27/360_F_589932782_vQAEAZhHnq1QCGu5ikwrYaQD0Mmurm0N.jpg" width="80" height="80">'

            url = f"/chat/direct/{i.outgoing.id}"

        else:
            sender = "You"
            try:
                name = i.incoming.username
                url = f"/chat/direct/{i.incoming.id}"
                if i.incoming.photo:
                    pfp = i.incoming.photo.url

                else:
                    pfp = '<img src="https://t4.ftcdn.net/jpg/05/89/93/27/360_F_589932782_vQAEAZhHnq1QCGu5ikwrYaQD0Mmurm0N.jpg" width="80" height="80">'

            except:
                name = i.incoming.name
                url = f"/chat/group/{i.incoming.id}"
                if i.incoming.photo:
                    pfp = i.incoming.photo.url

                else:
                    pfp = '''
                    <svg viewBox="0 0 212 212" height="80" width="80" preserveAspectRatio="xMidYMid meet"
                        class="ln8gz9je ppled2lx">
                        <title>default-group</title>
                        <path class="background"
                            d="M105.946 0.25C164.318 0.25 211.64 47.596 211.64 106C211.64 164.404 164.318 211.75 105.945 211.75C47.571 211.75 0.25 164.404 0.25 106C0.25 47.596 47.571 0.25 105.946 0.25Z"
                            fill="#DFE5E7"></path>
                        <path class="background"
                            d="M105.946 0.25C164.318 0.25 211.64 47.596 211.64 106C211.64 164.404 164.318 211.75 105.945 211.75C47.571 211.75 0.25 164.404 0.25 106C0.25 47.596 47.571 0.25 105.946 0.25Z"
                            fill="#DFE5E7"></path>
                        <path class="primary" fill-rule="evenodd" clip-rule="evenodd"
                            d="M102.282 77.2856C102.282 87.957 93.8569 96.5713 83.3419 96.5713C72.827 96.5713 64.339 87.957 64.339 77.2856C64.339 66.6143 72.827 58 83.3419 58C93.8569 58 102.282 66.6143 102.282 77.2856ZM150.35 80.1427C150.35 89.9446 142.612 97.857 132.954 97.857C123.296 97.857 115.5 89.9446 115.5 80.1427C115.5 70.3409 123.296 62.4285 132.954 62.4285C142.612 62.4285 150.35 70.3409 150.35 80.1427ZM83.3402 109.428C68.5812 109.428 39 116.95 39 131.928V143.714C39 147.25 41.8504 148 45.3343 148H121.346C124.83 148 127.68 147.25 127.68 143.714V131.928C127.68 116.95 98.0991 109.428 83.3402 109.428ZM126.804 110.853C127.707 110.871 128.485 110.886 129 110.886C143.759 110.886 174 116.95 174 131.929V141.571C174 145.107 171.15 148 167.666 148H134.854C135.551 146.007 135.995 143.821 135.995 141.571L135.75 131.071C135.75 121.51 130.136 117.858 124.162 113.971C122.772 113.067 121.363 112.15 120 111.143C119.981 111.123 119.962 111.098 119.941 111.07C119.893 111.007 119.835 110.931 119.747 110.886C121.343 110.747 124.485 110.808 126.804 110.853Z">
                        </path>
                    </svg>
                    '''


        if i.message.type == "image":
            x = f"{sender}: Photo"

        else:
            x = f"{sender}: {i.message.message}"

        if len(x) > 3:
            x = x[:3]

        latestMessagesHTML.append(f"""
            <a href={url}>
                <div class="chat">
                    <div>
                        {pfp}
                    </div>
                    <div style="display: flexbox;margin-left: 5%;">
                        <div class="username">
                            <h1>{name}</h1>
                        </div>
                        <div class="message">
                            <p>{x}</p>
                        </div>
                    </div>
                </div>
            </a>
        """)


    res = FollowSystem.objects.all().filter(follower=user)

    posts = []

    if len(res) > 0:
        following = True

        for i in res:
            try:
                post = Posts.objects.all().filter(posted_by=Users.objects.get(username=i.following.username)).order_by("-id")
                for i in post:
                    if user not in i.likes.all():
                        posts.append(i)

            except:
                pass

    else:
        following = False

    requests = Requests.objects.all().filter(requested_to=user)

    return render(request, "main/index.html", {"user":user, "following":following, "requests":requests, "posts":posts, "latest":latestMessagesHTML})

def details(request, username):
    followinst = Users.objects.get(username=username)

    posts = Posts.objects.all().filter(posted_by=followinst)

    following = False

    userinst = Users.objects.get(email=request.session.get("email"))

    try:
        res = Requests.objects.get(requested_by=userinst, requested_to=followinst, type="follow")
        requested = True

    except:
        requested = False

        try:
            res = FollowSystem.objects.get(follower=userinst, following=followinst)
            followers = FollowSystem.objects.all().filter(following=followinst)
            following = True

        except:
            followers = 0
            following = False

    return render(request, "main/details.html", {"user":followinst, "posts":posts, "following":following, "requested":requested, "followers":followers})

def follow(request):
    followid = int(request.GET.get("followid"))

    userinst = Users.objects.get(email=request.session.get("email"))

    followinst = Users.objects.get(id=followid)

    if followinst.public == False:
        Requests.objects.create(requested_by=userinst, requested_to=followinst, type="follow")
        return HttpResponse("Requested")

    else:
        FollowSystem.objects.create(follower=userinst, following=followinst)

    return HttpResponse("Following")

def unfollow(request):
    followid = int(request.GET.get("followid"))

    userinst = Users.objects.get(email=request.session.get("email"))

    followinst = Users.objects.get(id=followid)

    FollowSystem.objects.get(follower=userinst, following=followinst).delete()

    return HttpResponse("done")

def derequest(request):
    followid = int(request.GET.get("followid"))

    userinst = Users.objects.get(email=request.session.get("email"))

    followinst = Users.objects.get(id=followid)

    Requests.objects.get(requested_by=userinst, requested_to=followinst, type="follow").delete()

    return HttpResponse("done")


def requestAction(request):
    action = request.GET.get("action")
    requestid = request.GET.get("id")

    if action == "accept":
        res = Requests.objects.get(id=requestid)

        FollowSystem.objects.create(follower=res.requested_by, following=res.requested_to)

        Requests.objects.get(id=requestid).delete()

    else:
        Requests.objects.get(id=requestid).delete()

    return HttpResponse("success")

def createsuccess(request):
    return render(request, "main/created.html")

def createPost(request):

    if request.method == "POST":
        username = request.session.get("username")
        files = request.FILES.getlist("files")
        caption = request.POST.get("caption")

        try:
            pid = Posts.objects.last().id + 1

        except:
            pid = 1

        post = Posts.objects.create(id=pid, posted_by=Users.objects.get(username=username), caption=caption)

        for i in files:
            try:
                fid = Files.objects.last().id + 1

            except:
                fid = 1

            f = Files.objects.create(id=fid)
            f.file = i
            f.save()

            post.files.add(f)

            post.save()

        return redirect("/post/create/success/")

    return render(request, "main/create.html", {"form":CreatePostForm})

def likePost(request):
    postid = request.GET.get("postid")

    userinst = Users.objects.get(email=request.session.get("email"))

    postinst = Posts.objects.get(id=postid)

    postinst.likes.add(userinst)

    postinst.save()

    return HttpResponse("yes")

def dislikePost(request):
    postid = request.GET.get("postid")

    userinst = Users.objects.get(email=request.session.get("email"))

    postinst = Posts.objects.get(id=postid)

    postinst.likes.remove(userinst)

    postinst.save()

    return HttpResponse("yes")


def displayPost(request, postid):
    try:
        post = Posts.objects.get(id=postid)
        comments = Comments.objects.all().filter(post=post)

    except:
        return HttpResponse("Post with this ID doesn't exist")

    return render(request, "main/display-post.html", {"post":post, "comments":comments})


def commentPost(request):
    postid = request.GET.get("postid")
    postinst = Posts.objects.get(id=postid)
    userinst = Users.objects.get(email=request.session.get("email"))
    comment = request.GET.get("comment")

    Comments.objects.create(post=postinst, commented_by=userinst, comment=comment)

    comments = Comments.objects.all().filter(post=postinst)

    pfps = []

    for i in comments:
        pfp = Users.objects.get(username=i.commented_by.username)

        if pfp.photo:
            pfps.append(pfp.photo.url)

        else:
            pfps.append(
                "https://t4.ftcdn.net/jpg/05/89/93/27/360_F_589932782_vQAEAZhHnq1QCGu5ikwrYaQD0Mmurm0N.jpg"
            )

    allcomment = []

    for i in range(len(comments)):
        allcomment.append(
            f"""

<span class="comment">
    <div class="img">
        <img src="{ pfps[i] }" alt="" width="56" height="56">
    </div>
    <div class="content" style="margin-left: 2%;">
        <div class="username" style="display: flex;">
            <h3>{ comments[i].commented_by.username }</h3>
        </div>
        <div class="message">
            { comments[i].comment }
        </div>
    </div>
</span>

"""
        )

    return HttpResponse(allcomment)


def logout(request):
    del request.session

    return redirect("/")
