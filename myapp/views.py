from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import Group, User
from django.http import JsonResponse, request
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import path
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from myapp.models import *


def psychologist_home(request):
    return render(request,'psychologist/index.html')

def logout(request):
    return redirect('/myapp/login_get/')

def home_get(request):
    return render(request, 'admin/index.html')
def login_get(request):
    return render(request,'login.html')

def LandingPage(request):
    return render(request,'landingpage.html')

@csrf_exempt
def login_post(request):
    username=request.POST['username']
    password = request.POST['password']
    s=authenticate(request,username=username,password=password)
    if s is not None:
        if s.is_superuser:
            login(request, s)
            return redirect('/myapp/home_get')
        if s.groups.filter(name='Admin').exists():
            login(request,s)
            return redirect('/myapp/home_get')
        elif s.groups.filter(name='psychologist').exists():
            login(request, s)
            return redirect('/myapp/psychologist_home/')
        else:
            return redirect('/myapp/login_get/')
    else:
        return redirect('/myapp/login_get/')

def verify_psychologist_get(request):
    var=Psychologist.objects.filter(status='Pending')
    return render(request, 'admin/verify_psychologist.html',{'data':var})

def view_complaint_get(request):
    var=Complaint.objects.all()
    return render(request,'admin/view_complaint.html',{'data':var})


def view_feedback_get(request):
    data=Feedback.objects.all()
    return render(request,'admin/view_feedback.html',{'data':data})

def accept_psychologist(request,id):
    a=Psychologist.objects.filter(id=id).update(status='Approved')
    return redirect('/myapp/verify_psychologist_get/')

def reject_psychologist(request,id):
    a=Psychologist.objects.filter(id=id).update(status='Rejected')
    return redirect('/myapp/verify_psychologist_get/')

def approved_psy(request):
    a=Psychologist.objects.filter(status='Approved')
    return render(request,'admin/approved_psy.html',{'data':a})

def view_review_get(request):
    data=Rating.objects.all()
    return render(request,'admin/view_review.html',{'data':data})

def view_users_get(request):
    data=User_table.objects.all()
    return render(request,'admin/view_users.html',{'data':data})


def chat_with_user_get(request):
    return render(request, 'psychologist/chat_with_user.html')

def manage_schedule_get(request):
    return render(request, 'psychologist/manage_schedule.html')

def view_booking_get(request):
    return render(request, 'psychologist/view_booking.html')

def view_payment_get(request):
    data=Payment.objects.all()
    return render(request,'psychologist/view_payment.html',{'data':data})


def register_get(request):
    return render(request, 'psychologist/register.html')

def change_password(request):
    return render(request,'admin/change_password.html')

def change_password_post(request):
    currentpassword = request.POST['old']
    newpassword = request.POST['new']
    confirmpassword = request.POST['confirm']
    user = request.user
    if not check_password(currentpassword, user.password):
        messages.error(request,'current password is not correct....!')
        return redirect('/myapp/change_password/')
    if newpassword == confirmpassword:
        user.set_password(newpassword)
        user.save()
        messages.error(request,'Password changed succesfully')
        return redirect('/myapp/login_get')
    else:
        messages.error(request, 'Password does not match....!')
        return redirect('/myapp/change_password/')

# def psychologist_home(request):
#     return render(request,'psychologist/index.html')

def register(request):
    return render(request,'psychologist/register.html')

def psychologist_post(request):
    username=request.POST['username']
    password=request.POST['password']
    name=request.POST['name']
    place=request.POST['place']
    phone=request.POST['phone']
    email=request.POST['email']
    qualification=request.POST['qualification']
    experience=request.POST['experience']
    user=User.objects.create(username=username,password=make_password(password))
    user.groups.add(Group.objects.get(name='psychologist'))
    user.save()

    a=Psychologist()
    a.username=username
    a.password=password
    a.name=name
    a.email=email
    a.place=place
    a.phone=phone
    a.qualification=qualification
    a.experience=experience

    a.LOGIN=user
    a.save()
    return redirect ('/myapp/login_get/')

def view_psychologist_get(request):
    return render(request, 'admin/view_psychologist.html')

def send_reply_get(request,id):
    a=Complaint.objects.get(id=id)
    return render(request, 'admin/send_reply.html',{'data':a})

def send_reply_post(request):
    reply = request.POST['reply']
    id=request.POST['id']
    a=Complaint.objects.filter(id=id).update(reply=reply)
    return redirect('/myapp/view_complaint_get/')

def add_schedule_get(request):
    return render(request, 'psychologist/add_schedule.html')

def add_schedule_post(request):
    from_time=request.POST['from_time']
    to_time=request.POST['to_time']
    date=request.POST['date']
    b=Psychologist.objects.get(LOGIN_id=request.user.id)

    a=schedule()
    a.from_time=from_time
    a.to_time=to_time
    a.date=date
    a.status='Pending'
    a.PSYCHOLOGIST=b
    a.save()
    return redirect('/myapp/view_schedule_get')

def view_schedule_get(request):
    a = schedule.objects.filter(PSYCHOLOGIST__LOGIN_id = request.user.id)
    return render(request, 'psychologist/view_schedule.html',{'data':a})

def view_schedule_post(request):
    return redirect('/myapp/view_schedule_get')


def view_appointment_get(request):
    a = Appointment.objects.filter(schedule__PSYCHOLOGIST__LOGIN_id = request.user.id,status='pending')
    return render(request, 'psychologist/view_appoinment.html',{'data':a})

def approve_appointment(request,id):
    a = Appointment.objects.filter(id=id).update(status='Approved')
    return redirect('/myapp/view_appointment_get/')

def reject_appointment(request,id):
    a = Appointment.objects.filter(id=id).update(status='Rejected')
    return redirect('/myapp/view_appointment_get/')

def view_approved_appointment(request):
    a = Appointment.objects.filter(schedule__PSYCHOLOGIST__LOGIN_id = request.user.id,status='Approved')
    return redirect(request,'admin/approved_appoinment.html',{'data':a})


def edit_schedule_get(request,id):
    e=schedule.objects.get(id=id)
    return render(request, 'psychologist/edit_schedule.html',{'data':e})

def edit_schedule_post(request):
    from_time = request.POST['from_time']
    to_time = request.POST['to_time']
    date = request.POST['date']
    # status = request.POST['status']
    id = request.POST['id']

    a = schedule.objects.get(id=id)

    a.from_time = from_time
    a.to_time = to_time
    a.date = date
    # a.status =  status
    a.save()
    return redirect('/myapp/view_schedule_get/')

def delete_schedule(request,id):
    schedule.objects.get(id=id).delete()
    return redirect('/myapp/view_schedule_get')

#
# def view_booking_get(request):
#     date = request.POST['date']
#     from_time = request.POST['from_time']
#     to_time = request.POST['to_time']
#     status = request.POST['status']
#     chat = request.POST['chat']
#     id = request.POST['id']
#
#     a = schedule.objects.get(id=id)
#
#     a.from_time = from_time
#     a.to_time = to_time
#     a.date = date
#     a.status ='pending'
#     a.save()
#     return redirect('/myapp/view_booking_get/')








# def chat1(request):
#     request.session["userid"] = '1'
#     cid = str(request.session["userid"])
#     request.session["new"] = cid
#     return render(request, "experts/chat.html",{'toid': cid})
#
# #----------admin--------------
# def chat2(request,id):
#     request.session["userid"] = id
#     cid = str(request.session["userid"])
#     request.session["new"] = cid
#     return render(request, "admin/chat.html",{'toid': cid})
#
#
#
# def chat_view(request):
#     fromid = request.user.id
#     toid = request.session["userid"]
#     from django.db.models import Q
#
#     res = Chatss.objects.filter(Q(FROM=fromid, To=toid) | Q(FROM=toid, To=fromid))
#     l = []
#
#     for i in res:
#         l.append({"id": i.id, "message": i.Chat, "to_id": i.TO, "date": i.Date, "from_id": i.FROM})
#
#     return JsonResponse({ "data": l, 'toid': request.session["userid"]})
#
# def chat_send(request, msg):
#     lid = request.user.id
#     from_id = request.session["User"]
#     to_id = request.session["User"]
#     message = msg
#     print(message,'gfdtd=======ghftgf======hgff======ghfdgfc')
#     import datetime
#     d = datetime.datetime.now().date()
#     chatobt = Chatss()
#     chatobt.message = message
#     chatobt.TO= to_id
#     chatobt.FROM = lid
#     chatobt.date = d
#     chatobt.save()
#
#     return JsonResponse({"status": "ok"})

def psychologist_view_user(request):
    user=User_table.objects.all()
    return render(request,'psychologist/view user.html',{'data':user})

def psychologist_chat_to_user(request, id):
    request.session["userid"] = id
    # cid = str(request.session["userid"])
    cid = str(request.session["userid"])

    print(cid,'cid==========')
    print( request.session["userid"],' request.session["userid"]==========')

    request.session["new"] = cid
    qry = User_table.objects.get(LOGIN_id=cid)
    print(qry.LOGIN.id,'login----------')

    return render(request, "psychologist/user Chat.html", { 'name': qry.name, 'toid': cid})


def psy_chat_view_user(request):
    # fromid = request.session["lid"]
    fromid = request.user.id
    toid = request.session["userid"]
    qry = User_table.objects.get(LOGIN_id=request.session["userid"])
    from django.db.models import Q

    res = Chatss.objects.filter(Q(FROM=fromid, TO=toid) | Q(FROM=toid, TO=fromid)).order_by('id')
    l = []
    print(qry.name,'userssssssssss')

    for i in res:
        l.append({"id": i.id, "message": i.message, "to": i.TOID_id, "date": i.date, "from": i.FROMID_id})

    # return JsonResponse({'photo': qry.image, "data": l, 'name': qry.name, 'toid': request.session["userid"]})
    return JsonResponse({ "data": l, 'name': qry.name, 'toid': request.session["userid"]})


def psy_chat_send_user(request, msg):
    lid = request.user.id
    toid = request.session["userid"]
    message = msg

    import datetime
    d = datetime.datetime.now().date()
    chatobt = Chatss()
    chatobt.message = message
    chatobt.TO = toid
    chatobt.FROM = lid
    chatobt.date = d
    chatobt.save()

    return JsonResponse({"status": "ok"})
#
#
#
#
# def user_viewchat(request):
#     fromid = request.POST["from_id"]
#     toid = request.POST["to_id"]
#     # lmid = request.POST["lastmsgid"]    from django.db.models import Q
#
#     res = Chat.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid)).order_by("id")
#     l = []
#
#     for i in res:
#         l.append({"id": i.id, "msg": i.message, "from": i.FROMID_id, "date": i.date, "to": i.TOID_id})
#
#     return JsonResponse({"status":"ok",'data':l})
#
#
# def user_sendchat(request):
#     FROM=request.POST['from_id']
#     TO=request.POST['to_id']
#     date=request.POST['date']
#     print(FROM)
#     print(TO)
#     msg=request.POST['message']
#
#     from  datetime import datetime
#     c=Chatss()
#     c.FROM=FROM
#     c.TOID_id=TO
#     c.message=msg
#     c.date=datetime.now()
#     c.save()
#     return JsonResponse({'status':"ok"})
#


# def view_booking_get(request):
def psy_bookings_get(request,id):
    a = Appointment.objects.filter(schedule_id = id)
    return render(request, 'psychologist/view_booking.html',{'data':a})

def approve_request(request,id):
    Appointment.objects.filter(id=id).update(status="approved")
    return redirect('/myapp/view_schedule_get/')


def reject_request(request,id):
    Appointment.objects.filter(id=id).update(status="Rejected")
    return redirect('/myapp/view_schedule_get/')

# def view_payment_post(request):


def user_login_post(request):
    username=request.POST['username']
    password = request.POST['password']
    s=authenticate(request,username=username,password=password)
    if s is not None:
        if s.groups.filter(name='Users').exists():
            return JsonResponse({'status':'ok','lid':str(s.id),'type':'Users'})

        else:
            return JsonResponse({'status':'Not ok',})
    else:
        return JsonResponse({'status': 'Not ok', })


def user_register_post(request):
    name=request.POST['name']
    place=request.POST['place']
    phone=request.POST['phone']
    email=request.POST['email']
    username=request.POST['username']
    password=request.POST['password']
    user = User.objects.create(username=username, password=make_password(password))
    user.groups.add(Group.objects.get(name='Users'))
    user.save()

    a = User_table()
    a.name = name

    a.email = email
    a.place = place
    a.phone = phone

    a.LOGIN = user
    a.save()



    return JsonResponse({'status':'ok'})

def register_post(request):
    return JsonResponse({'status': 'ok', })

def send_feedback_post(request):
    return JsonResponse({'status': 'ok', })

def send_complaints_and_view_reply_post(request):
    return JsonResponse({'status': 'ok', })

def manage_dairy_post(request):
    return JsonResponse({'status': 'ok', })


def predict_emotion_using_nlp_post(request):
    return JsonResponse({'status': 'ok', })


def recommend_psychologist_while_high_post(request):
    return JsonResponse({'status': 'ok', })


def suggest_the_remedy_while_emotion_low_post(request):
    return JsonResponse({'status': 'ok', })


def view_psychologist_post(request):
    # lid = request.POST['lid']
    # print(lid,'============lid============')
    # print(lid,'============lid============')
    # print(lid,'============lid============')
    # print(lid,'============lid============')
    # print(lid,'============lid============')
    # print(lid,'============lid============')
    var=Psychologist.objects.all()
    data=[]
    for i in var:
        data.append({
            'id':i.id,
            'LOGIN':str(i.LOGIN.id),
            'name':i.name,
            'qualification':i.qualification,
            'phone':i.phone,
            'email':i.email,
            'experience':i.experience
        })

    print(data,'=============')
    return JsonResponse({'status': 'ok','data':data })


def book_appointment_post(request):
    return JsonResponse({'status': 'ok', })


def chat_psychologist_post(request):
    return JsonResponse({'status': 'ok', })


def send_review_rating_post(request):
    return JsonResponse({'status': 'ok', })



# def user_view_schedule_post(request):
#     data = []
#     for i in schedule.objects.all():
#         data.append({
#             'id': i.id,
#             'psy_name': i.PSYCHOLOGIST.name,
#             'from_time': i.from_time,
#             'to_time': i.to_time,
#             'date': i.date,
#             'status': i.status,
#         })
#     return JsonResponse({'status': 'ok', 'data': data})

#
# def user_view_schedule_post(request):
#     lid = request.POST.get('lid')
#     user = User_table.objects.get(LOGIN_id=lid)
#
#     data = []
#
#     for i in schedule.objects.all():
#         appt = Appointment.objects.filter(
#             schedule=i,
#             USER=user
#         ).first()
#
#         data.append({
#             'id': i.id,
#             'psy_name': i.PSYCHOLOGIST.name,
#             'from_time': str(i.from_time),
#             'to_time': str(i.to_time),
#             'date': str(i.date),
#
#             # appointment info
#             'appointment_status': appt.status.lower() if appt else 'not_booked',
#             'appointment_id': appt.id if appt else 0,
#             'amount': appt.amount if appt else '500',
#         })
#
#     return JsonResponse({'status': 'ok', 'data': data})
#
#
#
# def user_book_appointment_post(request):
#     schedule_id = request.POST.get('schedule_id')
#     lid = request.POST.get('lid')
#
#     sch = schedule.objects.get(id=schedule_id)
#     user = User_table.objects.get(LOGIN_id=lid)
#
#     # prevent duplicate request by same user
#     if Appointment.objects.filter(schedule=sch, USER=user).exists():
#         return JsonResponse({
#             'status': 'failed',
#             'message': 'You already requested this appointment'
#         })
#
#     Appointment.objects.create(
#         USER=user,
#         name=sch.PSYCHOLOGIST.name,
#         schedule=sch,
#         date=sch.date,
#         status="pending",
#         amount="500"
#     )
#
#     return JsonResponse({'status': 'ok'})
#
#
#
# def payment_success(request):
#     appt_id = request.POST.get('appointment_id')
#     payment_id = request.POST.get('payment_id')
#
#     appt = Appointment.objects.get(id=appt_id)
#     appt.status = "paid"
#     appt.payment_id = payment_id
#     appt.save()
#
#     return JsonResponse({'status': 'ok'})


# views.py

def user_view_schedule_post(request):
    lid = request.POST.get('lid')
    user = User_table.objects.get(LOGIN_id=lid)

    data = []

    for i in schedule.objects.all():
        appt = Appointment.objects.filter(schedule=i, USER=user).first()

        amt = appt.amount if appt and appt.status.lower() == 'approved' else '0'

        data.append({
            'id': i.id,
            'psy_id': str(i.PSYCHOLOGIST.id),
            'psy_name': i.PSYCHOLOGIST.name,
            'from_time': str(i.from_time),
            'to_time': str(i.to_time),
            'date': str(i.date),
            'appointment_status': appt.status.lower() if appt else 'not_booked',
            'appointment_id': appt.id if appt else 0,
            'amount': amt,
        })

    return JsonResponse({'status': 'ok', 'data': data})


def user_view_psychologyst_googlemeet_link(request):
    psy_id=request.POST['psy_id']
    l=[]
    var=Google_meet_link.objects.filter(PSYCHOLOGIST_id=psy_id)
    for i in var:
        l.append({
            'id':i.id,
            'link':str(i.link),
            'date':str(i.date),
        })
    return JsonResponse({'status': 'ok', 'data': l})




# def user_book_appointment_post(request):
#     schedule_id = request.POST.get('schedule_id')
#     lid = request.POST.get('lid')
#
#     sch = schedule.objects.get(id=schedule_id)
#     user = User_table.objects.get(LOGIN_id=lid)
#
#     if Appointment.objects.filter(schedule=sch, USER=user).exists():
#         return JsonResponse({
#             'status': 'failed',
#             'message': 'You already requested this appointment'
#         })
#
#     Appointment.objects.create(
#         USER=user,
#         name=sch.PSYCHOLOGIST.name,
#         schedule=sch,
#         date=sch.date,
#         status="pending",
#         amount="500"
#     )
#
#     return JsonResponse({'status': 'ok'})









from datetime import datetime, timedelta
from django.http import JsonResponse

def user_book_appointment_post(request):
    schedule_id = request.POST.get('schedule_id')
    lid = request.POST.get('lid')

    sch = schedule.objects.get(id=schedule_id)
    user = User_table.objects.get(LOGIN_id=lid)

    # Prevent duplicate booking by same user
    if Appointment.objects.filter(schedule=sch, USER=user).exists():
        return JsonResponse({
            'status': 'failed',
            'message': 'You already requested this appointment'
        })

    # ✅ FIXED TIME FORMAT (24-hour)
    start_time = datetime.strptime(sch.from_time, "%H:%M")
    end_time = datetime.strptime(sch.to_time, "%H:%M")

    # Calculate total slots
    total_minutes = int((end_time - start_time).total_seconds() / 60)
    total_slots = total_minutes // 15

    # Count booked slots
    booked_slots = Appointment.objects.filter(schedule=sch).count()

    if booked_slots >= total_slots:
        sch.status = "Full"
        sch.save()
        return JsonResponse({
            'status': 'failed',
            'message': 'Slot full'
        })

    # Create appointment
    Appointment.objects.create(
        USER=user,
        name=sch.PSYCHOLOGIST.name,
        schedule=sch,
        date=sch.date,
        status="pending",
        amount="500"
    )

    # If last slot booked
    if booked_slots + 1 == total_slots:
        sch.status = "Full"
        sch.save()

    return JsonResponse({
        'status': 'ok',
        'message': 'Appointment booked'
    })




# def approve_appointment(request, appointment_id):
#     appt = Appointment.objects.get(id=appointment_id)
#     appt.status = "approved"   # important: lowercase
#     appt.amount = "500"        # ensure numeric
#     appt.save()
#     return JsonResponse({'status': 'ok'})


def payment_success(request):
    appt_id = request.POST.get('appointment_id')
    payment_id = request.POST.get('payment_id')

    appt = Appointment.objects.get(id=appt_id)
    appt.status = "paid"
    appt.payment_id = payment_id
    appt.save()

    # Add entry to Payment table
    Payment.objects.create(
        APPOINTMENT=appt,
        name=appt.name,
        date=appt.date,
        status="paid",
        amount=appt.amount
    )

    return JsonResponse({'status': 'ok'})




def user_send_feedback_post(request):
    lid = request.POST['lid']
    feedback=request.POST['feedback']
    user = User_table.objects.get(LOGIN=lid)
    a=Feedback()
    a.date=timezone.now().date()
    a.feedback=feedback
    a.USER=user
    a.save()
    return JsonResponse({'status': 'ok'})

def user_send_review_rating_post(request):
    lid = request.POST['lid']
    rating=request.POST['rating']
    review=request.POST['review']
    user = User_table.objects.get(LOGIN=lid)
    a=Rating()
    a.date=timezone.now().date()
    a.review=review
    a.rating=rating
    a.USER=user
    a.save()
    return JsonResponse({'status': 'ok'})

def send_complaint_viewreply_post(request):
    lid = request.POST['lid']
    complaint=request.POST['complaint']
    user = User_table.objects.get(LOGIN=lid)
    a=Complaint()
    a.date=timezone.now().date()
    a.complaint=complaint
    a.reply='pending'
    a.USER=user
    a.save()
    return JsonResponse({'status': 'ok'})

from django.db.models import Q

def user_chat(request):
    lid = request.POST['lid']
    pid = request.POST['pid']
    messages = Chatss.objects.filter(
        Q(FROM_id=lid, TO_id=pid) | Q(FROM_id=pid, TO_id=lid)
    ).order_by('id').values('message', 'FROM_id')

    formatted = [
        {'mess': m['message'], 'fro_id': m['FROM_id']}
        for m in messages
    ]

    return JsonResponse({'key': formatted})

def send_byst(request):
    lid = request.POST['lid']
    pid = request.POST['pid']
    message = request.POST['message']

    cc = Chatss()
    cc.message = message
    cc.date = datetime.now()
    cc.FROM_id = lid
    cc.TO_id = pid
    cc.save()

    return JsonResponse({'key': 'Success'})

# def diary_post(request):
#     lid = request.POST['lid']
#     dairys = request.POST['complaint']
#     user = User_table.objects.get(LOGIN=lid)
#
#     a = Complaint()
#     a.date = str(timezone.now().date()),
#     a.diary = diarys
#     a.reply = 'pending'
#     a.USER = user
#     a.save()
#     return JsonResponse({'status': 'ok'})

from django.db.models import Q

def view_reply(request):
    lid = request.POST['lid']
    complaint = request.POST['complaint']
    reply = request.POST['reply']
    user = User_table.objects.get(LOGIN=lid)

    a = reply()
    a.complaint = complaint
    a.reply = 'pending'
    a.USER = user
    a.save()
    return JsonResponse({'status': 'ok'})

def user_view_reply(request):
    lid = request.POST['lid']
    f = Complaint.objects.filter(USER__LOGIN_id = lid)
    l =[]
    for i in f:
        l.append({
            'id':i.id,
            'complaint':i.complaint,
            'reply':i.reply,
            'date':i.date,

                  })
    return JsonResponse({'status':'ok', 'data':l})

# def user_chat(request):
#     lid = request.POST['lid']
#     pid = request.POST['pid']
#     print(pid,'=========')
#     # ab = Psychologist.objects.get(id=pid)
#     ab = pid
#     print(lid,'yyygy')
#     messaage = Chatss.objects.filter(FROM_id=lid, TO_id=ab).order_by('id').values('message','FROM_id','TO_id')| Chatss.objects.filter(FROM_id=ab, TO_id=lid).order_by('id').values('message','FROM_id','TO_id')
#     print (messaage,'===============messages')
#     return JsonResponse({'key':list(messaage)})
#
# def send_byst(request):
#     lid=request.POST['lid']
#     pid = request.POST['pid']
#     # ab = Psychologist.objects.get(id = pid)
#     ab=pid
#     message = request.POST['message']
#     print(message,'=-========')
#
#     cc=Chatss()
#     cc.message=message
#
#     cc.date=datetime.now()
#     cc.FROM_id = lid
#     cc.TO_id = ab
#     cc.save()
#     return JsonResponse({'key':'Success'})







#
# def byst_chat(request):
#     lid = request.POST['lid']
#     book_id = request.POST['book_id']
#     ab = Appointment.objects.get(id=book_id)
#     sch = ab.SCHEDULE
#     dia_id = sch.DIALYSIS.LOGIN_id
#     print(dia_id,'jyyj')
#     print(lid,'yyygy')
#     messaage = chat.objects.filter(fro_id=lid, to_id=dia_id).order_by('id').values('mess','fro_id','to_id')|chat.objects.filter(fro_id=dia_id, to_id=lid).order_by('id').values('mess','fro_id','to_id')
#     print (messaage)
#     return JsonResponse({'key':list(messaage)})

# def send_byst(request):
#     lid=request.POST['lid']
#     book_id = request.POST['book_id']
#     ab = booking.objects.get(id = book_id)
#     sch = ab.SCHEDULE
#     dia_id = sch.DIALYSIS.LOGIN_id
#     mess = request.POST['mess']
#     print(mess)
#
#     cc=chat()
#     cc.mess=mess
#
#     cc.date=datetime.now()
#     cc.fro_id = lid
#     cc.to_id = dia_id
#     cc.save()
#     return JsonResponse({'key':'Seccess'})


# from django.http import JsonResponse
# from datetime import datetime
# from transformers import pipeline
# from .models import Diary_or_journal, User_table
#
# # Load emotion classifier ONCE
# emotion_classifier = pipeline(
#     "text-classification",
#     model="j-hartmann/emotion-english-distilroberta-base",
#     return_all_scores=True
# )
#
# def user_add_diary(request):
#     lid = request.POST['lid']
#     details = request.POST['details']
#
#     predictions = emotion_classifier(details)[0]
#     print(predictions,'predictionssssd')
#
#     detected_emotion = max(predictions, key=lambda x: x['score'])['label']
#
#     print(detected_emotion,'============detected_emotion')
#     print(detected_emotion,'============detected_emotion')
#     print(detected_emotion,'============detected_emotion')
#     print(detected_emotion,'============detected_emotion')
#
#
#     diary = Diary_or_journal()
#     diary.USER = User_table.objects.get(LOGIN_id=lid)
#     diary.date = datetime.now().date()
#     diary.details = details
#     diary.emotion = detected_emotion
#     diary.save()
#
#     return JsonResponse({
#         'status': 'ok',
#         'emotion': detected_emotion
#     })
#
#
#
# def user_view_diary(request):
#     lid = request.POST['lid']
#     f = Diary_or_journal.objects.filter(USER__LOGIN_id = lid)
#     l =[]
#     for i in f:
#         l.append({
#             'id':i.id,
#             'details':i.details,
#             'emotion':i.emotion,
#             'date':str(i.date),
#
#                   })
#     return JsonResponse({'status':'ok', 'data':l})
#
#
#
# from django.http import JsonResponse
# from datetime import date, timedelta
# from .models import Diary_or_journal, Psychologist
#
# def recommend_psychologist(request):
#     lid = request.POST['lid']
#
#     TARGET_EMOTIONS = ['sadness', 'depression', 'stress', 'fear', 'lonely']
#
#     today = date.today()
#
#     # Get last 3 diary entries ordered by date (latest first)
#     diaries = Diary_or_journal.objects.filter(
#         USER__LOGIN_id=lid
#     ).order_by('-date')[:3]
#
#     # Must have exactly 3 days data
#     if diaries.count() < 3:
#         return JsonResponse({
#             'status': 'ok',
#             'recommend': False,
#             'message': 'Not enough diary entries'
#         })
#
#     # Get emotions
#     emotions = [d.emotion.lower() for d in diaries]
#
#     # Check SAME emotion for 3 days
#     if emotions[0] == emotions[1] == emotions[2] and emotions[0] in TARGET_EMOTIONS:
#
#         psychologists = Psychologist.objects.all()
#         data = []
#
#         for i in psychologists:
#             data.append({
#                 'id': i.id,
#                 'name': i.name,
#                 'qualification': i.qualification,
#                 'phone': i.phone,
#                 'email': i.email,
#                 'experience': i.experience
#             })
#
#         return JsonResponse({
#             'status': 'ok',
#             'recommend': True,
#             'emotion': emotions[0],
#             'reason': 'Same negative emotion continued for 3 days',
#             'data': data
#         })
#
#     # ❌ Condition not satisfied
#     return JsonResponse({
#         'status': 'ok',
#         'recommend': False,
#         'message': 'No continuous negative emotion'
#     })




# new 1-1-26


# views.py
#
# from django.http import JsonResponse
# from datetime import datetime
# from .models import Diary_or_journal, User_table, Psychologist
# from transformers import pipeline
# import torch  # Optional, but ensures GPU if available
#
# # ==============================
# # CONFIG
# # ==============================
# NEGATIVE_EMOTIONS = ["sadness", "anger", "fear", "disgust"]  # Common negative from the model
# MIN_NEGATIVE_CONFIDENCE = 60  # Percentage threshold to suggest doctor
#
# # ==============================
# # LOAD EMOTION CLASSIFIER ONCE (at server start)
# # ==============================
# # Using a reliable multi-emotion model: "bhadresh-savani/distilbert-base-uncased-emotion"
# # Labels: sadness, joy, love, anger, fear, surprise
# print("Loading emotion classification model...")
# emotion_classifier = pipeline(
#     "text-classification",
#     model="bhadresh-savani/distilbert-base-uncased-emotion",
#     return_all_scores=True,  # Get all emotion probabilities
#     device=0 if torch.cuda.is_available() else -1  # Use GPU if available
# )
# print("Model loaded successfully!")
#
# # Map model labels to user-friendly names (optional)
# EMOTION_LABEL_MAP = {
#     "sadness": "sad",
#     "joy": "happy",
#     "love": "loved",
#     "anger": "angry",
#     "fear": "anxiety",
#     "surprise": "surprised"
# }
#
# # ==============================
# # MAIN VIEW
# # ==============================
# def user_add_diary(request):
#     if request.method != "POST":
#         return JsonResponse({"status": "error", "message": "POST required"})
#
#     try:
#         lid = request.POST["lid"]
#         details = request.POST.get("details", "").strip()
#
#         if not details:
#             return JsonResponse({"status": "error", "message": "Details are required"})
#
#         # ==========================
#         # EMOTION DETECTION
#         # ==========================
#         results = emotion_classifier(details)[0]  # List of dicts: [{'label': 'joy', 'score': 0.99}, ...]
#
#         # Convert to percentage and map labels
#         emotion_scores = {}
#         for item in results:
#             label = item['label']
#             score = item['score'] * 100  # Convert to percentage
#             friendly_label = EMOTION_LABEL_MAP.get(label, label)
#             emotion_scores[friendly_label] = round(score, 2)
#
#         # Determine dominant emotion
#         detected_emotion = max(emotion_scores, key=emotion_scores.get)
#         detected_percentage = emotion_scores[detected_emotion]
#
#         # ==========================
#         # DOCTOR SUGGESTION LOGIC
#         # ==========================
#         suggest_doctor = False
#         psychologist = None
#
#         # Check if dominant emotion is strongly negative
#         if (detected_emotion in NEGATIVE_EMOTIONS) and (detected_percentage >= MIN_NEGATIVE_CONFIDENCE):
#             suggest_doctor = True
#             psychologist = Psychologist.objects.first()  # Or use better logic to select
#
#         # ==========================
#         # SAVE DIARY ENTRY
#         # ==========================
#         diary = Diary_or_journal()
#         diary.USER = User_table.objects.get(LOGIN_id=lid)
#         diary.date = datetime.now().date()
#         diary.details = details
#         diary.emotion = detected_emotion
#         diary.emotion_percentage = detected_percentage
#         diary.save()
#
#         # ==========================
#         # RESPONSE
#         # ==========================
#         return JsonResponse({
#             "status": "ok",
#             "detected_emotion": detected_emotion,
#             "percentage": detected_percentage,
#             "emotion_breakdown": emotion_scores,
#             "suggest_doctor": suggest_doctor,
#             "psychologist": psychologist.name if psychologist else None,
#             "diary_id": diary.id
#         })
#
#     except User_table.DoesNotExist:
#         return JsonResponse({"status": "error", "message": "Invalid user"})
#     except Exception as e:
#         return JsonResponse({"status": "error", "message": str(e)})






# views.py
#
# from django.http import JsonResponse
# from datetime import datetime
# from .models import Diary_or_journal, User_table, Psychologist
# from transformers import pipeline
# import torch
#
# # ==============================
# # CONFIG
# # ==============================
# NEGATIVE_EMOTIONS = ["sad", "anxiety", "angry", "lonely"]  # Your desired negative emotions
# STRONG_THRESHOLD = 80      # Suggest doctor if current emotion ≥80%
# PERSISTENCE_THRESHOLD = 60 # Count as "negative day" if ≥60%
# RECENT_ENTRIES_TO_CHECK = 5
# MIN_NEGATIVE_DAYS_FOR_SUGGESTION = 3  # If 3+ out of last 5 are negative → suggest
#
# # ==============================
# # LOAD EMOTION MODEL ONCE
# # ==============================
# print("Loading emotion classification model...")
# emotion_classifier = pipeline(
#     "text-classification",
#     model="bhadresh-savani/distilbert-base-uncased-emotion",
#     return_all_scores=True,
#     device=0 if torch.cuda.is_available() else -1
# )
# print("Model loaded!")
#
# # Map model labels → your preferred emotion names
# EMOTION_LABEL_MAP = {
#     "sadness": "sad",
#     "joy": "happy",
#     "love": "loved",
#     "anger": "angry",
#     "fear": "anxiety",
#     "surprise": "surprised"
# }
#
# # ==============================
# # MAIN VIEW
# # ==============================
# def user_add_diary(request):
#     if request.method != "POST":
#         return JsonResponse({"status": "error", "message": "POST required"})
#
#     try:
#         lid = request.POST["lid"]
#         details = request.POST.get("details", "").strip()
#         if not details:
#             return JsonResponse({"status": "error", "message": "Diary details required"})
#
#         user = User_table.objects.get(LOGIN_id=lid)
#
#         # ==========================
#         # EMOTION DETECTION
#         # ==========================
#         results = emotion_classifier(details)[0]
#         emotion_scores = {}
#         for item in results:
#             model_label = item['label']
#             score_pct = round(item['score'] * 100, 2)
#             friendly_label = EMOTION_LABEL_MAP.get(model_label, model_label)
#             emotion_scores[friendly_label] = score_pct
#
#         detected_emotion = max(emotion_scores, key=emotion_scores.get)
#         detected_percentage = emotion_scores[detected_emotion]
#
#         # ==========================
#         # SAVE CURRENT DIARY ENTRY
#         # ==========================
#         diary = Diary_or_journal()
#         diary.USER = user
#         diary.date = datetime.now().date()
#         diary.details = details
#         diary.emotion = detected_emotion
#         diary.emotion_percentage = detected_percentage
#         diary.save()
#
#         # ==========================
#         # CHECK FOR PERSISTENT NEGATIVE EMOTIONS
#         # ==========================
#         recent_diaries = Diary_or_journal.objects.filter(
#             USER=user
#         ).order_by('-date')[:RECENT_ENTRIES_TO_CHECK]
#
#         negative_count = 0
#         for entry in recent_diaries:
#             if (entry.emotion in NEGATIVE_EMOTIONS) and (entry.emotion_percentage >= PERSISTENCE_THRESHOLD):
#                 negative_count += 1
#
#         persistent_negative = negative_count >= MIN_NEGATIVE_DAYS_FOR_SUGGESTION
#
#         # ==========================
#         # CURRENT STRONG NEGATIVE?
#         # ==========================
#         current_strong_negative = (
#             detected_emotion in NEGATIVE_EMOTIONS and
#             detected_percentage >= STRONG_THRESHOLD
#         )
#
#         # ==========================
#         # FINAL DOCTOR SUGGESTION LOGIC
#         # ==========================
#         suggest_doctor = current_strong_negative or persistent_negative
#         psychologist = Psychologist.objects.first() if suggest_doctor else None
#
#         # Optional: Add reason for suggestion (for debugging or frontend display)
#         suggestion_reason = []
#         if current_strong_negative:
#             suggestion_reason.append(f"Current emotion '{detected_emotion}' is {detected_percentage}%")
#         if persistent_negative:
#             suggestion_reason.append(f"{negative_count}/{RECENT_ENTRIES_TO_CHECK} recent entries show strong negative emotions")
#
#         # ==========================
#         # RESPONSE
#         # ==========================
#         return JsonResponse({
#             "status": "ok",
#             "detected_emotion": detected_emotion,
#             "percentage": detected_percentage,
#             "emotion_breakdown": emotion_scores,
#             "suggest_doctor": suggest_doctor,
#             "psychologist": psychologist.name if psychologist else None,
#             "suggestion_reason": " | ".join(suggestion_reason) if suggestion_reason else None,
#             "recent_negative_count": negative_count,
#             "diary_id": diary.id
#         })
#
#     except User_table.DoesNotExist:
#         return JsonResponse({"status": "error", "message": "Invalid user"})
#     except Exception as e:
#         return JsonResponse({"status": "error", "message": str(e)})













from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import Diary_or_journal, User_table, Psychologist
from google import genai
import json, re

# ================= CONFIG =================
NEGATIVE_EMOTIONS = ["sad", "anxiety", "angry", "lonely"]
STRONG_THRESHOLD = 80
PERSISTENCE_THRESHOLD = 60
RECENT_ENTRIES_TO_CHECK = 5
MIN_NEGATIVE_DAYS_FOR_SUGGESTION = 3

# ================= GEMINI CLIENT =================
client = genai.Client(api_key="AIzaSyDgSe5mfzzeqjAV6xv3OVXITljszXBy6jI")

# ================= MAIN VIEW =================
@csrf_exempt
def user_add_diary(request):

    lid = request.POST["lid"]
    details = request.POST.get("details", "").strip()
    if not details:
        return JsonResponse({"status": "error", "message": "Diary details required"})

    user = User_table.objects.get(LOGIN_id=lid)

    # ===== MULTI-LINE EMOTION DETECTION (GEMINI) =====
    prompt = f"""
Analyze the following diary (may contain multiple lines).

Diary:
{details}

Identify emotions ONLY from:
happy, loved, surprised, sad, anxiety, angry, lonely

Return ONLY valid JSON:
{{
  "emotions": [
    {{"emotion": "sad", "score": 0.75}},
    {{"emotion": "anxiety", "score": 0.60}}
  ]
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",

        contents=prompt
    )

    try:
        json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
        parsed = json.loads(json_match.group())
        emotion_results = parsed.get("emotions", [])
    except Exception:
        emotion_results = [{"emotion": "neutral", "score": 1.0}]

    emotion_scores = {}
    for item in emotion_results:
        emotion = item["emotion"].lower()
        score = round(item["score"] * 100, 2)
        emotion_scores[emotion] = max(emotion_scores.get(emotion, 0), score)

    detected_emotion = max(emotion_scores, key=emotion_scores.get)
    detected_percentage = emotion_scores[detected_emotion]

    # ===== SAVE DIARY =====
    diary = Diary_or_journal.objects.create(
        USER=user,
        date=datetime.now().date(),
        details=details,
        emotion=detected_emotion,
        emotion_percentage=detected_percentage
    )

    # ===== PERSISTENT NEGATIVE CHECK =====
    recent = Diary_or_journal.objects.filter(USER=user).order_by('-date')[:RECENT_ENTRIES_TO_CHECK]
    negative_count = sum(
        1 for d in recent
        if d.emotion in NEGATIVE_EMOTIONS and d.emotion_percentage >= PERSISTENCE_THRESHOLD
    )

    current_strong_negative = (
        detected_emotion in NEGATIVE_EMOTIONS and
        detected_percentage >= STRONG_THRESHOLD
    )

    persistent_negative = negative_count >= MIN_NEGATIVE_DAYS_FOR_SUGGESTION
    suggest_doctor = current_strong_negative or persistent_negative
    psychologist = Psychologist.objects.first() if suggest_doctor else None

    return JsonResponse({
        "status": "ok",
        "detected_emotion": detected_emotion,
        "percentage": detected_percentage,
        "emotion_breakdown": emotion_scores,
        "suggest_doctor": suggest_doctor,
        "psychologist": psychologist.name if psychologist else None,
        "recent_negative_count": negative_count,
        "diary_id": diary.id
    })










# ==============================
# VIEW DIARY
# ==============================
def user_view_diary(request):
    lid = request.POST['lid']
    diaries = Diary_or_journal.objects.filter(
        USER__LOGIN_id=lid
    ).order_by('-date')

    data = []
    for i in diaries:
        data.append({
            'id': i.id,
            'details': i.details,
            'emotion': i.emotion,
            'date': str(i.date),
        })

    return JsonResponse({'status': 'ok', 'data': data})



# def recommend_psychologist(request):
#     lid = request.POST['lid']
#
#     NEGATIVE_EMOTIONS = [
#         'sad', 'sadness', 'depression',
#         'lonely', 'stress', 'fear', 'anxiety'
#     ]
#
#     diaries = Diary_or_journal.objects.filter(
#         USER__LOGIN_id=lid
#     ).order_by('-date')[:3]
#
#     if diaries.count() < 3:
#         return JsonResponse({'status':'ok','recommend':False})
#
#     emotions = [d.emotion.lower() for d in diaries]
#
#     # Check all 3 are negative emotions
#     if any(e not in NEGATIVE_EMOTIONS for e in emotions):
#         return JsonResponse({'status':'ok','recommend':False})
#
#     # ✅ Fetch psychologists
#     psychologists = Psychologist.objects.all()
#     data = []
#     for p in psychologists:
#         data.append({
#             'id': p.id,
#             'name': p.name,
#             'qualification': p.qualification,
#             'phone': p.phone,
#             'email': p.email,
#             'experience': p.experience
#         })
#
#     return JsonResponse({
#         'status':'ok',
#         'recommend': True,
#         'emotions': emotions,
#         'psychologists': data
#     })





# def recommend_psychologist(request):
#     lid = request.POST['lid']
#
#     NEGATIVE_EMOTIONS = ['sad', 'sadness', 'depression', 'lonely', 'stress', 'fear', 'anxiety']
#
#     diaries = Diary_or_journal.objects.filter(USER__LOGIN_id=lid).order_by('-date')[:3]
#
#     if diaries.count() < 3:
#         return JsonResponse({'status':'ok', 'recommend': False})
#
#     emotions = [d.emotion.lower() for d in diaries]
#
#     if any(e not in NEGATIVE_EMOTIONS for e in emotions):
#         return JsonResponse({'status':'ok', 'recommend': False})
#
#
#     emotion_to_qualification = {
#         'depression': ['M.Phil Psychology', 'Clinical Psychology'],
#         'stress': ['M.Phil Psychology', 'Clinical Psychology'],
#         'lonely': ['Counseling Psychology', 'M.A Psychology'],
#         'fear': ['Clinical Psychology', 'M.Phil Psychology'],
#         'sad': ['M.Phil Psychology', 'Clinical Psychology'],
#     }
#
#     latest_emotion = emotions[0]
#     required_qualifications = emotion_to_qualification.get(latest_emotion, [])
#
#     # 🔹 Filter psychologists by qualification
#     psychologists = Psychologist.objects.filter(qualification__in=required_qualifications)
#
#     # 🔹 Sort by experience (descending)
#     def experience_to_int(exp):
#         try:
#             return int(exp)
#         except:
#             return 0
#
#     psychologists = sorted(psychologists, key=lambda x: experience_to_int(x.experience), reverse=True)
#
#     # Prepare response
#     data = []
#     for p in psychologists:
#         data.append({
#             'id': p.id,
#             'name': p.name,
#             'qualification': p.qualification,
#             'phone': p.phone,
#             'email': p.email,
#             'experience': p.experience
#         })
#
#     return JsonResponse({
#         'status':'ok',
#         'recommend': True,
#         'emotions': emotions,
#         'psychologists': data
#     })


# def recommend_psychologist(request):
#     lid = request.POST['lid']
#
#     NEGATIVE_EMOTIONS = ['sad', 'sadness', 'depression', 'lonely', 'stress', 'fear', 'anxiety']
#
#     # Get last 3 diary entries
#     diaries = Diary_or_journal.objects.filter(USER__LOGIN_id=lid).order_by('-date')[:3]
#
#     if diaries.count() < 3:
#         return JsonResponse({'status':'ok', 'recommend': False})
#
#     emotions = [d.emotion.lower() for d in diaries]
#
#     if any(e not in NEGATIVE_EMOTIONS for e in emotions):
#         return JsonResponse({'status':'ok', 'recommend': False})
#
#     latest_emotion = emotions[0]
#
#     # Qualification mapping
#     emotion_to_qualification = {
#         'depression': ['M.Phil Psychology', 'Clinical Psychology'],
#         'stress': ['M.Phil Psychology', 'Clinical Psychology'],
#         'lonely': ['Counseling Psychology', 'M.A Psychology'],
#         'fear': ['Clinical Psychology', 'M.Phil Psychology'],
#         'sad': ['M.Phil Psychology', 'Clinical Psychology'],
#         'anxiety': ['Clinical Psychology', 'M.Phil Psychology'],
#     }
#
#     required_qualifications = emotion_to_qualification.get(latest_emotion, [])
#
#     # Filter psychologists
#     psychologists = Psychologist.objects.filter(qualification__in=required_qualifications)
#
#     # Sort by experience descending
#     def experience_to_int(exp):
#         try:
#             return int(exp)
#         except:
#             return 0
#
#     psychologists = sorted(psychologists, key=lambda x: experience_to_int(x.experience), reverse=True)
#
#     # Prepare psychologist data
#     psych_data = []
#     for p in psychologists:
#         psych_data.append({
#             'id': p.id,
#             'name': p.name,
#             'qualification': p.qualification,
#             'phone': p.phone,
#             'email': p.email,
#             'experience': p.experience
#         })
#
#     # 🔹 Add remedies / suggestions mapping
#     emotion_to_remedy = {
#         'depression': "Try light exercise, meditation, talk therapy, maintain a healthy routine.",
#         'stress': "Practice deep breathing, take short breaks, organize tasks, mindfulness meditation.",
#         'lonely': "Connect with friends/family, join a hobby group, try journaling, social activities.",
#         'fear': "Face small steps gradually, practice relaxation techniques, discuss fears with a therapist.",
#         'sad': "Spend time on hobbies, talk to loved ones, maintain a positive routine, gentle exercise.",
#         'anxiety': "Practice breathing exercises, reduce caffeine, maintain sleep hygiene, cognitive behavioral techniques."
#     }
#
#     remedy = emotion_to_remedy.get(latest_emotion, "Maintain healthy lifestyle and consider talking to a counselor.")
#
#     return JsonResponse({
#         'status':'ok',
#         'recommend': True,
#         'emotions': emotions,
#         'psychologists': psych_data,
#         'remedy': remedy,
#         'latest_emotion': latest_emotion
#     })






from django.http import JsonResponse
from .models import Diary_or_journal, Psychologist

def recommend_psychologist(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required'})

    try:
        lid = request.POST.get('lid')
        if not lid:
            return JsonResponse({'status': 'error', 'message': 'lid required'})

        # Define negative emotions (normalized)
        NEGATIVE_EMOTIONS = {
            'sad', 'sadness', 'depression', 'lonely', 'loneliness',
            'stress', 'stressed', 'fear', 'anxiety', 'angry', 'anger'
        }

        # Get last 3 diary entries
        diaries = Diary_or_journal.objects.filter(
            USER__LOGIN_id=lid
        ).order_by('-date')[:3]

        if diaries.count() < 3:
            return JsonResponse({
                'status': 'ok',
                'recommend': False,
                'message': 'Not enough diary entries (need 3 recent ones)'
            })

        # Extract and normalize emotions
        emotions = [d.emotion.strip().lower() for d in diaries]
        latest_emotion = emotions[0]  # Most recent

        # Check if ALL 3 are negative
        if not all(emo in NEGATIVE_EMOTIONS for emo in emotions):
            return JsonResponse({
                'status': 'ok',
                'recommend': False,
                'message': 'Recent emotions are not consistently negative'
            })

        # Mapping: primary emotion → recommended specialist areas
        emotion_specialty_map = {
            'depression': ['Clinical Psychology', 'M.Phil Psychology', 'Psychiatry'],
            'sad': ['Clinical Psychology', 'M.Phil Psychology', 'Counseling Psychology'],
            'sadness': ['Clinical Psychology', 'M.Phil Psychology', 'Counseling Psychology'],
            'anxiety': ['Clinical Psychology', 'M.Phil Psychology', 'CBT Specialist'],
            'stress': ['Clinical Psychology', 'Counseling Psychology', 'Stress Management'],
            'lonely': ['Counseling Psychology', 'M.A Psychology', 'Social Psychology'],
            'loneliness': ['Counseling Psychology', 'M.A Psychology'],
            'fear': ['Clinical Psychology', 'M.Phil Psychology', 'Exposure Therapy'],
            'anger': ['Clinical Psychology', 'Anger Management', 'Counseling Psychology'],
            'angry': ['Clinical Psychology', 'Anger Management', 'Counseling Psychology'],
        }

        required_specialties = emotion_specialty_map.get(latest_emotion, ['Clinical Psychology', 'M.Phil Psychology'])

        # Filter psychologists whose qualification contains any required specialty
        psychologists = Psychologist.objects.all()
        matched_psychologists = []

        for psych in psychologists:
            psych_qual = psych.qualification or ""
            if any(specialty.lower() in psych_qual.lower() for specialty in required_specialties):
                try:
                    exp_years = int(psych.experience or 0)
                except (ValueError, TypeError):
                    exp_years = 0
                matched_psychologists.append((exp_years, psych))

        # Sort by experience descending
        matched_psychologists.sort(key=lambda x: x[0], reverse=True)

        # Extract sorted psychologist objects
        sorted_psychologists = [psych for exp, psych in matched_psychologists]

        # Prepare response data
        psych_data = []
        for p in sorted_psychologists[:5]:  # Top 5 most experienced
            psych_data.append({
                'id': p.id,
                'name': p.name,
                'qualification': p.qualification,
                'phone': p.phone or "Not available",
                'email': p.email or "Not available",
                'experience': p.experience or "N/A"
            })

        # Self-help remedies based on emotion
        remedies = {
            'depression': "• Practice daily sunlight exposure\n• Try gentle exercise (walking)\n• Maintain sleep schedule\n• Consider journaling positive moments",
            'sad': "• Connect with a trusted friend\n• Engage in a favorite hobby\n• Listen to uplifting music\n• Practice gratitude journaling",
            'sadness': "• Connect with a trusted friend\n• Engage in a favorite hobby\n• Listen to uplifting music\n• Practice gratitude journaling",
            'anxiety': "• Try 4-7-8 breathing (inhale 4s, hold 7s, exhale 8s)\n• Limit caffeine\n• Practice grounding techniques\n• Avoid overthinking spirals",
            'stress': "• Take short breaks every hour\n• Practice progressive muscle relaxation\n• Prioritize tasks\n• Say 'no' when needed",
            'lonely': "• Reach out to one person today\n• Join an online/offline community\n• Volunteer or help someone\n• Try group activities",
            'loneliness': "• Reach out to one person today\n• Join an online/offline community\n• Volunteer or help someone\n• Try group activities",
            'fear': "• Break fears into small steps\n• Use relaxation techniques\n• Challenge negative thoughts\n• Seek gradual exposure",
            'anger': "• Pause and count to 10\n• Use deep breathing\n• Express feelings calmly\n• Physical activity helps release tension",
        }

        remedy = remedies.get(latest_emotion, "Focus on self-care: healthy sleep, nutrition, movement, and social connection.")

        return JsonResponse({
            'status': 'ok',
            'recommend': True,
            'latest_emotion': latest_emotion.capitalize(),
            'recent_emotions': [e.capitalize() for e in emotions],
            'psychologists': psych_data,
            'remedy': remedy,
            'message': f"Based on recent feelings of {latest_emotion}, professional support is recommended."
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })



def psy_chat_to_user(request, id):
    request.session["userid"] = id
    # cid = str(request.session["userid"])
    cid = str(request.session["userid"])

    print(cid,'cid==========')
    print( request.session["userid"],' request.session["userid"]==========')

    request.session["new"] = cid
    qry = User_table.objects.get(LOGIN_id=cid)
    print(qry.LOGIN.id,'login----------')

    return render(request, "psychologist/Chat.html", { 'name': qry.name, 'toid': cid})


def chat_view(request):
    # fromid = request.session["lid"]
    fromid = request.user.id
    toid = request.session["userid"]
    qry = User_table.objects.get(LOGIN_id=request.session["userid"])
    from django.db.models import Q

    res = Chatss.objects.filter(Q(FROM_id=fromid, TO_id=toid) | Q(FROM_id=toid, TO_id=fromid)).order_by('id')
    l = []
    print(qry.name,'userssssssssss')

    for i in res:
        l.append({"id": i.id, "message": i.message, "to": i.TO_id, "date": i.date, "from": i.FROM_id})

    # return JsonResponse({'photo': qry.image, "data": l, 'name': qry.name, 'toid': request.session["userid"]})
    return JsonResponse({ "data": l, 'name': qry.name, 'toid': request.session["userid"]})


def psy_chat_send_user_new(request, msg):
    lid = request.user.id
    toid = request.session["userid"]
    message = msg

    import datetime
    d = datetime.datetime.now().date()
    chatobt = Chatss()
    chatobt.message = message
    chatobt.TO_id = toid
    chatobt.FROM_id = lid
    chatobt.date = d
    chatobt.save()

    return JsonResponse({"status": "ok"})









def user_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    # lmid = request.POST["lastmsgid"]    from django.db.models import Q

    res = Chatss.objects.filter(Q(FROM_id=fromid, TO_id=toid) | Q(FROM_id=toid, TO_id=fromid)).order_by("id")
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.message, "from": i.FROM_id, "date": i.date, "to": i.TO_id})

    return JsonResponse({"status":"ok",'data':l})


def user_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    print(FROM_id)
    print(TOID_id)
    msg=request.POST['message']

    from  datetime import datetime
    c=Chatss()
    c.FROM_id=FROM_id
    c.TO_id=TOID_id
    c.message=msg
    c.date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})



def psy_add_google_meet_link(request):
    if request.method == 'POST':
        link = request.POST['link']

        var = Google_meet_link()
        var.date = datetime.now().today().date()
        var.link = link
        var.PSYCHOLOGIST = Psychologist.objects.get(LOGIN_id=request.user.id)
        var.save()
        return redirect('/myapp/psy_add_google_meet_link/')
    return render(request,'psychologist/Add_googlemeetlink.html')


def psy_view_link(request):

    var=Google_meet_link.objects.filter(PSYCHOLOGIST__LOGIN_id=request.user.id)
    return render(request,'psychologist/view_googlemeetlink.html',{'data':var})


def psy_delete_link(request,id):
    var=Google_meet_link.objects.get(id=id)
    var.delete()
    return redirect('/myapp/psy_view_link/')



def user_send_schedule_rating(request):
    sid=request.POST['psy_id']
    lid=request.POST['lid']
    rating=request.POST['rating']
    review=request.POST['review']
    user = User_table.objects.get(LOGIN=lid)
    a=Expert_Rating()
    a.date=timezone.now().date()
    a.review=review
    a.rating=rating
    a.EXPERT=Psychologist.objects.get(id=sid)
    a.USER=user
    a.save()
    return JsonResponse({'status': 'ok'})




