from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from mc.models import Config,Decision
import datetime

# def hello(request):
#     now = datetime.datetime.now()
#     t = get_template('index.html')
#     html = t.render(Context({'current_date':now}))
#     return HttpResponse(html)
class FormatUser(object):
    """docstring for FormatUser"""
    def __init__(self, name,want,now):
        super(FormatUser, self).__init__()
        self.name = name
        self.want = int(want)
        self.max = int(int(want)*1.1)
        self.min = int(int(want)*0.9)
        self.now = now
        self.left = int(int(want)*0.9-now)
        self.left2 = int(int(want)-now)

@login_required(login_url='/login/')
def home(request):
    config = Config.objects.get()
    ps = User.objects.filter(first_name="1")
    decides1 = Decision.objects.filter(financing_name = config.name,financing_part = 1)
    decides2 = Decision.objects.filter(financing_name = config.name,financing_part = 2)
    formatps = []
    for p in ps:
        mydecides = Decision.objects.filter(financing_name = config.name,to_user=p.username,financing_part = 2,status=1)
        amount = 0
        for mydecide in mydecides:
            amount+=mydecide.amount
        formatps.append(FormatUser(p.username,p.last_name,amount))
    t = get_template('home.html')
    html = t.render(Context({'decides1':decides1,'decides2':decides2,'config':config,'user':request.user,'formatps':formatps}))
    return HttpResponse(html)

@login_required(login_url='/login/')
def decide(request):
    if request.user.first_name !='1' and request.user.first_name !='2':
        return  HttpResponseRedirect('/login/')
    config = Config.objects.get()
    p = User.objects.filter(first_name="1")
    if request.user.first_name=="2":
        decides = Decision.objects.filter(financing_name = config.name,financing_term = config.term,financing_part = 1,status=1)
        mydecides = Decision.objects.filter(financing_name = config.name,from_user=request.user.username,financing_part = 2,status=1)
        umydecides = Decision.objects.filter(financing_name = config.name,from_user=request.user.username,financing_part = 2,status=0)
        amount = 0
        for mydecide in mydecides:
            amount+=int(mydecide.amount)
        for mydecide in umydecides:
            amount+=int(mydecide.amount)
        left = int(config.limit) - amount
    else:
        decides = Decision.objects.filter(financing_name = config.name,financing_term = config.term,financing_part = 1,from_user = request.user.username,status=1)
        mydecides = Decision.objects.filter(financing_name = config.name,to_user=request.user.username,financing_part = 2,status=1)
        amount = 0
        for mydecide in mydecides:
            amount+=int(mydecide.amount)
        left = int(request.user.last_name) - amount
    t = get_template('decide.html')
    html = t.render(Context({'user':request.user,'config':config,'decides':decides,'amount':amount,'left':left}))
    return HttpResponse(html)

@csrf_exempt
@login_required(login_url='/login/')
def decide_form(request):
    if request.user.first_name !='1' and request.user.first_name !='2':
        return  HttpResponseRedirect('/login/')
    config = Config.objects.get()
    t = get_template('decide.html')
    if request.user.first_name=="1":
        if request.POST.get('interest','') is None or request.POST.get('financing_type','') is None:
            return  HttpResponseRedirect('/decide/')
        
        _interest = float(request.POST.get('interest',''))
        _financing_type = request.POST.get('financing_type','')
        if config.part !=1:
            return  HttpResponseRedirect('/decide/')
        mydecides = Decision.objects.filter(financing_name = config.name,to_user=request.user.username,financing_part = 2,status=1)
        _amount = int(request.user.last_name)
        hasRecieve = 0
        for mydecide in mydecides:
            hasRecieve+=int(mydecide.amount)
        if _amount-hasRecieve < 0:
            return  HttpResponseRedirect('/decide/')
        _amount = _amount - hasRecieve
        d = Decision.objects.filter(   financing_name = config.name,
                                    financing_term = config.term,
                                    financing_part = request.user.first_name,
                                    from_user = request.user.username,
                                    status = 1,
                                    )
        if len(d)>0:
            d[0].financing_type = _financing_type
            d[0].amount = _amount
            d[0].interest = _interest
            if 'to_user_name' in request.POST:
                d[0].to_user = User.objects.get(username=request.POST.get('to_user_name',''))
            d[0].save()
        else:
            d = Decision(   financing_name = config.name,
                            financing_term = config.term,
                            financing_part = request.user.first_name,
                            financing_type = _financing_type,
                            from_user = request.user.username,
                            amount = _amount,
                            interest = _interest,
                            status = 1,
                            )
            if 'to_user_name' in request.POST:
                d.to_user = request.POST.get('to_user_name','')
            d.save()
    else:
        if config.part !=2:
            return  HttpResponseRedirect('/decide/')
        mydecides = Decision.objects.filter(financing_name = config.name,from_user=request.user.username, financing_part = 2,status=1)
        amount = config.limit
        if amount<=0:
            return  HttpResponseRedirect('/decide/')
        for mydecide in mydecides:
            amount-=mydecide.amount
        Decision.objects.filter(   financing_name = config.name,
                                    financing_term = config.term,
                                    financing_part = config.part,
                                    from_user = request.user.username).delete()
        for value in request.POST:
            _d = request.POST.getlist(value,'')
            if _d[0]=='' or _d[1] == '' or _d[2]=='' or _d[3]=='':
                continue
            if int(_d[3])<0:
                _d[3] = 0
            amount-=int(_d[3])
            if amount<0:
                return  HttpResponseRedirect('/decide/')
            if _d[1]=='g':
                _d[2] = round(float(_d[3]) * float( _d[2]) /int(_d[4]),2)
            else:
                _d[2] = float(_d[2])
            print _d[2]
            d = Decision(   financing_name = config.name,
                financing_term = config.term,
                financing_part = config.part,
                financing_type = _d[1],
                from_user = request.user.username,
                to_user = _d[0],
                amount = int(_d[3]),
                interest = _d[2],
                status = 0
                )
            d.save()
    return  HttpResponseRedirect('/home/')
def login(request):
    t = get_template('login.html')
    now = datetime.datetime.now()
    html = t.render(Context({'current_date':now}))
    return HttpResponse(html)

@csrf_exempt 
def login_form(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username=username, password= password)
    if user is not None and user.is_active:
        auth.login(request,user)
        # print user.groups
        return HttpResponseRedirect('/home/')
    else:
        t = get_template('login.html')
        now = datetime.datetime.now()
        html = t.render(Context({'error':'error'}))
        return HttpResponse(html)
    
def logout(request):
    auth.logout(request)
    t = get_template('login.html')
    now = datetime.datetime.now()
    html = t.render(Context({'current_date':now}))
    return HttpResponse(html)
@login_required(login_url='/login/')
def count(request):
    config = Config.objects.get()
    if request.user.is_staff:
        if config.part == 2:
            cdecides = Decision.objects.filter(financing_name = config.name,financing_term=config.term,financing_part = 1)
            for cdecide in cdecides:
                todecides= Decision.objects.filter(financing_name = config.name,financing_term=config.term,financing_part = 2,to_user = cdecide.from_user,status=0)
                amount = cdecide.amount
                total = 0
                for todecide in todecides:
                    total+= todecide.amount
                if amount*1.1 -total<0:
                    todecides.update(status=2)
                else:
                    todecides.update(status=1)
            error = 0
            config.term = config.term + 1
            config.part = 1
            config.save()
        else:
            error = 2
            config.part = 2
            config.save()
    else:
        error = 1
    t = get_template('count.html')
    html = t.render(Context({'config':config,'error':error}))
    return HttpResponse(html)
