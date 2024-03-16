from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from core.models import *
from core.forms import *
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

# Create your views here.

def index(request):

    useremail = request.session.get("email")
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
            current_date_time = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))

            date = str(latestMessages[j+1].message.date).split("-")
            time = str(latestMessages[j+1].message.time).split(":")
            next_date_time = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))


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

    return render(request, "chat/index.html", {"latest" : latestMessagesHTML})

def chat(request, userid):
    if not request.session.get("logged-in") or not request.session.get("id"):
        return redirect("/login")

    currentid = request.session.get("id")

    if userid == currentid:
        return render(request, "chat/message.html", {"message": "same"})

    users = Users.objects.all()
    results = Users.objects.all().filter(id=userid)

    user = None

    for j in results:
        user = j.id

    return render(
        request,
        "chat/direct/chat.html",
        {
            "info": results,
            "id": request.session.get("id"),
            "username": request.session.get("username"),
            "email": request.session.get("email"),
            "url": request.session.get("filename"),
            "users": users,
            "senderid": user,
        },
    )

@csrf_exempt
def sendImage(request):
    image = request.FILES.get("image")
    incoming = request.POST.get("incoming")
    outgoing = request.POST.get("outgoing")
    Type = request.POST.get("type")
    message = request.POST.get("message")
    date = request.POST.get("date")
    time = request.POST.get("time")

    if Messages.objects.all():
        pid = MessageInstances.objects.last().id + 1
    else:
        pid = 1

    MessageInstances(id=pid, type=Type, message=message, date=date, time=time).save()

    p = MessageInstances.objects.get(id=pid)

    if image:
        p.image = image

    p.save()

    Messages(incoming=Users.objects.get(username=incoming), outgoing=Users.objects.get(username=outgoing), message=p).save()

    return JsonResponse({"success":True})


def sendmessage(request):
    incoming = request.GET.get("incoming")
    outgoing = request.GET.get("outgoing")
    messageinput = request.GET.get("message")
    users = Users.objects.get(username=incoming)
    user = Users.objects.get(username=outgoing)
    date = request.GET.get("date")
    time = request.GET.get("time")

    try:
        lid = MessageInstances.objects.last().id + 1

    except:
        lid = 1

    MessageInstances.objects.create(id=lid, type="text", message=messageinput, date=date, time=time)

    messageinst = MessageInstances.objects.get(id=lid)


    Messages.objects.create(
        incoming=users, outgoing=user, message=messageinst
    )

    data = {"success"}

    return HttpResponse(data)


def search(request):
    query = request.GET.get("q")
    users = Users.objects.filter(username__contains=query)
    username = request.session.get("username")
    main = []

    for i in users:
        if i.username == username:
            continue
        else:
            main.append(
                f"""
                    <a href="/main/chat/{i.id}">
                        <div class="options">
                            <div class="option">
                                <div class="img">
                                    <img src="{ i.photo.url }" height="56" width="56" id="pfp">
                                </div>
                                <div class="user">
                                    <h3>{ i.username }</h3>
                                </div>
                            </div>
                        </div>
                    </a>
                        """
            )

    return HttpResponse(main)


def date_time(date, time):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    date = date.split("-")
    date = datetime.date(int(date[0]), int(date[1]), int(date[2]))

    month = months[date.month - 1]

    day = days[date.weekday()]

    today = datetime.date.today()

    time = time.split(":")

    time.pop()

    if int(time[0]) > 12:
        time[0] = str(int(time[0]) - 12)
        time = ":".join(time)
        time += " p.m"

    else:
        time = ":".join(time)
        time += " a.m"

    if (today - date).days > 4:
        full_date = f"{month} {date.day}, {time}"

    elif today == date:
        full_date = f"Today, {time}"

    else:
        full_date = f"{day}, {time}"

    return full_date



def fetch(request, userid):
    results = Users.objects.all().filter(id=userid)
    username = request.session.get("username")
    userinst = Users.objects.get(username=username)
    messages = Messages.objects.all().filter(Q(incoming=userinst, outgoing=results[0]))
    main = []

    stored_date = None

    for i in messages:
        if stored_date != date_time(str(i.message.date), str(i.message.time)):
            main.append(f'''
                <main class="center">
                    <span>{date_time(str(i.message.date), str(i.message.time))}</span>
                </main>
                        ''')

            for j in results:
                if (
                    str(i.incoming).strip() == str(username).strip()
                    and str(i.outgoing).strip() == str(j.username).strip()
                    ):
                    if str(i.message.type) == "image":
                        main.append(
                            f"""<main class="left" id="{i.message.id}">
                                    <a href="/media/{str(i.message.image)}" target="_blank">
                                        <img src=/media/{str(i.message.image)} id="text-img" style="width: 200px; height: 150px; border-radius: 22px;">
                                    </a>
                                </main>"""
                        )

                        continue

                    else:
                        main.append(
                            f"""<main class="left" id="{i.id}">
                                <span id="message-{i.message.id}">{ i.message.message }</span>
                            </main>"""
                        )

                    continue

                elif (
                    str(i.incoming).strip() == str(j.username).strip()
                    and str(i.outgoing).strip() == str(username).strip()
                    ):
                    if str(i.message.type) == "image":
                        main.append(
                            f"""<main class="right" id="{i.message.id}">
                                <div class="menu-content">
                                    <button type="button" class="delete-btn" onclick="deleteMessage({i.message.id})">Delete</button>
                                </div>
                                <div class="menu">
                                    <button type="button" class="menu-btn" onclick="openMenu()">...</button>
                                </div>
                                <a href="/media/{str(i.message.image)}" target="_blank">
                                    <img src=/media/{str(i.message.image)} id="text-img" style="width: 200px; height: 150px; border-radius: 22px;">
                                </a>
                            </main>"""
                        )

                        continue

                    else:
                        main.append(
                            f"""<main class="right" id="{i.message.id}">
                                <div class="menu-content">
                                    <button type="button" class="delete-btn" onclick="deleteMessage({i.message.id})">Delete</button>
                                </div>
                                <div class="menu">
                                    <button type="button" class="menu-btn" onclick="openMenu()">...</button>
                                </div>
                                <span id="message-{i.message.id}">{ i.message.message }</span>
                            </main>"""
                        )

                    continue


        else:
            for j in results:
                if (
                    str(i.incoming).strip() == str(username).strip()
                    and str(i.outgoing).strip() == str(j.username).strip()
                    ):
                    if str(i.message.type) == "image":
                        main.append(
                            f"""<main class="left" id="{i.message.id}">
                                    <a href="/media/{str(i.message.image)}" target="_blank">
                                        <img src=/media/{str(i.message.image)} id="text-img" style="width: 200px; height: 150px; border-radius: 22px;">
                                    </a>
                                </main>"""
                        )

                        continue

                    else:
                        main.append(
                            f"""<main class="left" id="{i.id}">
                                <span id="message-{i.message.id}">{ i.message.message }</span>
                            </main>"""
                        )

                    continue

                elif (
                    str(i.incoming).strip() == str(j.username).strip()
                    and str(i.outgoing).strip() == str(username).strip()
                    ):
                    if str(i.message.type) == "image":
                        main.append(
                            f"""<main class="right" id="{i.message.id}">
                                <div class="menu-content">
                                    <button type="button" class="delete-btn" onclick="deleteMessage({i.message.id})">Delete</button>
                                </div>
                                <div class="menu">
                                    <button type="button" class="menu-btn" onclick="openMenu()">...</button>
                                </div>
                                <a href="/media/{str(i.message.image)}" target="_blank">
                                    <img src=/media/{str(i.message.image)} id="text-img" style="width: 200px; height: 150px; border-radius: 22px;">
                                </a>
                            </main>"""
                        )

                        continue

                    else:
                        main.append(
                            f"""<main class="right" id="{i.message.id}">
                                <div class="menu-content">
                                    <button type="button" class="delete-btn" onclick="deleteMessage({i.message.id})">Delete</button>
                                </div>
                                <div class="menu">
                                    <button type="button" class="menu-btn" onclick="openMenu()">...</button>
                                </div>
                                <span id="message-{i.message.id}">{ i.message.message }</span>
                            </main>"""
                        )

                    continue

    return HttpResponse(main)


def deleteMessage(request):
    mid = request.GET.get("id")
    MessageInstances.objects.get(id=mid).delete()

    return HttpResponse("done")


def createGroup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        selected = request.POST.get("users")
        selected = selected.split(",")

        try:
            last = Groups.objects.last().id + 1

        except:
            last = 1

        group = Groups(id=last, name=name)

        group.save()

        for i in selected:
            inst = Users.objects.get(username=i)
            group.members.add(inst)
            group.save()

        admininst = Users.objects.get(username=selected[0])
        group.admin.add(admininst)
        group.save()

        return redirect(f"/chat/group/{last}")

    users = Users.objects.all()
    username = request.session.get("username")
    return render(
        request, "chat/group/create-group.html", {"users": users, "username": username}
    )


def groupChat(request, groupid):
    if not request.session.get("logged-in") or not request.session.get("id"):
        return redirect("/login")

    users = Users.objects.all()
    results = Users.objects.all()

    try:
        group = Groups.objects.get(id=groupid)

    except:
        return HttpResponse("<center><h1>Group does not exist</h1></center>")

    return render(
        request,
        "chat/group/chat.html",
        {
            "info": results,
            "id": request.session.get("id"),
            "username": request.session.get("username"),
            "email": request.session.get("email"),
            "url": request.session.get("filename"),
            "users": users,
            "groupid": groupid,
            "group":group
        },
    )


def fetchGroup(request, groupid):
    group = Groups.objects.get(id=groupid)
    username = request.session.get("username")
    userinst = Users.objects.get(username=username)
    if userinst not in group.members.all():
        return HttpResponse("You are not added to this group.")
    messages = GroupMessage.objects.all().filter(incoming=group)
    main = []

    stored_date = None

    for i in messages:
        if stored_date != date_time(str(i.message.date), str(i.message.time)):
            main.append(f'''
                <main class="center">
                    <span>{date_time(str(i.message.date), str(i.message.time))}</span>
                </main>
                ''')
        if i.incoming == group:
            if str(i.outgoing) == username:
                if str(i.message.type) == "image":
                    main.append(
                        f"""<main class="right" id="{i.message.id}">
                            <div class="menu-content">
                                <button type="button" class="delete-btn" onclick="deleteMessage({i.message.id})">Delete</button>
                            </div>
                            <div class="menu">
                                <button type="button" class="menu-btn" onclick="openMenu()">...</button>
                            </div>
                            <a href="/media/{str(i.message.image)}" target="_blank">
                                <img src=/media/{str(i.message.image)} id="text-img" style="width: 200px; height: 150px; border-radius: 22px;">
                            </a>
                        </main>"""
                    )

                else:
                    main.append(
                        f"""<main class="right" id="{i.message.id}">
                                    <div class="menu-content">
                                        <button type="button" class="delete-btn" onclick="deleteMessage({i.message.id})">Delete</button>
                                    </div>
                                    <div class="menu">
                                        <button type="button" class="menu-btn" onclick="openMenu()">...</button>
                                    </div>
                                    <span id="message-{i.message.id}">{ i.message.message }</span>
                                </main>"""
                    )

            else:
                if str(i.message.type) == "image":
                    main.append(
                        f"""<main class="left" id="{i.id}">
                                <div class="image">
                                    <div class="name">
                                            {i.outgoing.username}
                                        </div>
                                    </div>
                                <div class="main">
                                    <img src="{i.outgoing.photo.url if i.outgoing.photo else "https://t4.ftcdn.net/jpg/05/89/93/27/360_F_589932782_vQAEAZhHnq1QCGu5ikwrYaQD0Mmurm0N.jpg"}" width="45" height="45" style="border-radius: 50%; margin-right: 0.5%;">
                                    <a href="/media/{str(i.message.image)}" target="_blank">
                                        <img src=/media/{str(i.message.image)} id="text-img" style="width: 200px; height: 150px; border-radius: 22px;">
                                    </a>
                                </div>
                            </main>"""
                    )

                else:
                    main.append(
                        f"""<main class="left" id="{i.id}">
                                <div class="image">
                                    <div class="name">
                                            {i.outgoing.username}
                                        </div>
                                    </div>
                                <div class="main">
                                    <img src="{i.outgoing.photo.url if i.outgoing.photo else "https://t4.ftcdn.net/jpg/05/89/93/27/360_F_589932782_vQAEAZhHnq1QCGu5ikwrYaQD0Mmurm0N.jpg"}" width="45" height="45" style="border-radius: 50%;">
                                    <span>{i.message.message}</span>
                                </div>
                            </main>"""
                    )

    return HttpResponse(main)

def groupSendmessage(request):
    incoming = request.GET.get("incoming")
    outgoing = request.GET.get("outgoing")
    messageinput = request.GET.get("message")

    group = Groups.objects.get(name=incoming)
    user = Users.objects.get(username=outgoing)
    date = request.GET.get("date")
    time = request.GET.get("time")

    try:
        lid = MessageInstances.objects.last().id + 1

    except:
        lid = 1

    MessageInstances.objects.create(id=lid, type="text", message=messageinput, date=date, time=time)

    messageinst = MessageInstances.objects.get(id=lid)

    GroupMessage.objects.create(
        incoming = group, outgoing = user, message = messageinst
    )

    return JsonResponse({"success":True})

def groupSendImage(request):
    image = request.FILES.get("image")
    incoming = request.POST.get("incoming")
    outgoing = request.POST.get("outgoing")
    message = request.POST.get("message")
    date = request.POST.get("date")
    time = request.POST.get("time")
    Type = "image"

    group = Groups.objects.get(name=incoming)
    user = Users.objects.get(username=outgoing)

    try:
        pid = MessageInstances.objects.last().id + 1

    except:
        pid = 1

    print(pid)

    MessageInstances(id=pid, type=Type, message=message, date=date, time=time).save()

    p = MessageInstances.objects.get(id=pid)

    if image:
        p.image = image

    p.save()

    GroupMessage(incoming=group, outgoing=user, message=p).save()

    return HttpResponse("success")

def deleteMessage(request):
    mid = request.GET.get("id")
    MessageInstances.objects.get(id=mid).delete()

    return HttpResponse("done")

