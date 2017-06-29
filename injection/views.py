from django.http import HttpResponse
from django.template import loader
from injection.models import Session
from injection.models import Seating
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_request(request):
    if not request.user.is_authenticated() and ('username' not in request.POST.keys() or 'password' not in request.POST.keys()):
        template = loader.get_template('login_request.html')
        return HttpResponse(template.render({}, request))

    if (not request.user.is_authenticated()):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('login failed!')
    else:
        user = request.user

    context = {'team_name': user.username}
    template = loader.get_template('login_request.html')
    return HttpResponse(template.render(context, request))

def logout_request(request):
    logout(request)
    return login_request(request)

# @login_required
def index(request):
    template = loader.get_template('index.html')
    first_session = Session.objects.first()

    context = {
        'session': first_session,
    }

    return HttpResponse(template.render(context, request))

def reset_session(request, session_id):
    template = loader.get_template('index.html')
    session = get_object_or_404(Session, pk=session_id)

    result = session.seating_set.all().delete()
    Seating.create(session, 'Linan Qiu', 'Jenny Liu').save()
    Seating.create(session, 'Steve Swanson', 'Becky').save()
    Seating.create(session, 'Travis Vanderstud', 'TBD').save()
    session.number_of_resets += 1
    session.save()

    reseed_count = len(session.seating_set.all())

    context = {
            'session': session,
            'reset_message' : "Successfully reset session. Deleted %s seatings. Reseeded %s seatings." % (result[1]['injection.Seating'], reseed_count),
    }

    return HttpResponse(template.render(context, request))

def submit(request, session_id):
    template = loader.get_template('index.html')
    session = get_object_or_404(Session, pk=session_id)

    if ('member_name' not in request.POST.keys() or 'guest_name' not in request.POST.keys()):
        return index(request)

    member_name = request.POST['member_name']
    guest_name = request.POST['guest_name']
    seating = Seating.create(session,member_name, guest_name)
    seating.save()
    session.save()
    context = {
        'session': session,
        'success_message' : 'Entry saved successfully',
    }
    return HttpResponse(template.render(context, request))

    # try:
    #     member_name = request.POST['member_name']
    #     guest_name = request.POST['guest_name']
    #     seating = Seating.create(session,member_name, guest_name)
    #     seating.save()
    #     session.save()
    # except Exception as e:
    #     context = {
    #         'session': session,
    #         'exception_type' : e.__class__.__name__,
    #         'exception' : e,
    #     }
    #     return HttpResponse(template.render(context, request))
    # else:   
    #     context = {
    #         'session': session,
    #         'success_message' : 'Entry saved successfully',
    #     }
    #     return HttpResponse(template.render(context, request))

    # try:
    #     selected_choice = question.choice_set.get(pk=request.POST['choice'])
    # except (KeyError, Choice.DoesNotExist):
    #     # Redisplay the question voting form.
    #     return render(request, 'polls/detail.html', {
    #         'question': question,
    #         'error_message': "You didn't select a choice.",
    #     })
    # else:
    #     selected_choice.votes += 1
    #     selected_choice.save()
    #     # Always return an HttpResponseRedirect after successfully dealing
    #     # with POST data. This prevents data from being posted twice if a
    #     # user hits the Back button.
    #     return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))