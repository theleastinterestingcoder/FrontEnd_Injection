from django.contrib.auth.models import User
from dateutil import tz
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from injection.models import Session, LeaderBoard, FlagClaim
from django.shortcuts import redirect

def login_request(request, context = {}):
    if not request.user.is_authenticated() and ('username' not in request.POST.keys() or 'password' not in request.POST.keys()):
        template = loader.get_template('login_request.html')
        return HttpResponse(template.render({}, request))

    if (not request.user.is_authenticated()):
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username).first()

        if (user is None):
            return create_user(request)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('login failed! Password is incorrect')
    else:
        user = request.user

    context['team_name'] =  user.username
    template = loader.get_template('login_request.html')
    return HttpResponse(template.render(context, request))

def logout_request(request):
    logout(request)
    return login_request(request)

def create_user(request, context = {}, force_recreate = False):
    template = loader.get_template('create_user.html')
    if (request.user.is_authenticated()):
        context = {'success_message' : '%s has been created. Go forth and vandalize some pages.' % request.user.username}
        return HttpResponse(template.render(context, request))

    if (force_recreate or 'username' not in request.POST.keys() or 'password' not in request.POST.keys()):
        return HttpResponse(template.render(context, request))

    username = request.POST['username']
    password = request.POST['password']

    m = User.objects.filter(username=username).first()

    if (m is None):
        user = User.objects.create_user(username, '', password)
        login(request, user)

        return create_user(request)
    else:
        context['error_message'] = 'Username is taken'
        return create_user(request, context, True)


def index(request):
    template = loader.get_template('index.html')
    open_session = Session.objects.filter(name='Open Session').first()
    recent_leaderboard = open_session.leaderboard_set.order_by('-id').first()

    template = loader.get_template('index.html')
    winning_claim = recent_leaderboard.flagclaim_set.order_by('-last_modified').first()
    
    winning_team = '[Nobody]' if winning_claim is None else winning_claim.current_team
    current_user_is_winning = request.user is not None and request.user.username.lower().strip() == winning_team.lower().strip()
    context = {
        'session': open_session,
        'leaderboard' : recent_leaderboard,
        'winning_claim' : winning_claim,
        'winning_team' : winning_team,
        'current_user_is_winning' : current_user_is_winning
    }

    return HttpResponse(template.render(context, request))

@login_required(login_url='/injection/login')
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

@login_required(login_url='/injection/login')
def view_session(request, session_id, leaderboard_id):
    session = get_object_or_404(Session, pk=session_id)
    leaderboard = get_object_or_404(LeaderBoard, pk=leaderboard_id)

    if (session.team is not None and session.team != request.user):
        template = loader.get_template('session_denied.html')
        context = {'private_session_owner' : session.team.username}
        return HttpResponse(template.render(context, request))
    
    template = loader.get_template('index.html')

    winning_claim = LeaderBoard.objects.filter(id=leaderboard_id).first().flagclaim_set.order_by('-last_modified').first()
    winning_team = '[Nobody]' if winning_claim is None else winning_claim.current_team
    current_user_is_winning = request.user is not None and request.user.username.lower().strip() == winning_team.lower().strip()

    if ('team_name' not in request.POST.keys() or 'comment' not in request.POST.keys()):

        context = {
            'session': session,
            'leaderboard' : leaderboard,
            'winning_claim' : winning_claim,
            'winning_team' : winning_team,
            'current_user_is_winning' : current_user_is_winning

        }
        return HttpResponse(template.render(context, request))

    team_name = request.POST['team_name']
    comment = request.POST['comment']
    team_submit = request.user
    previous_team = winning_claim.current_team

    c = FlagClaim.create(leaderboard, comment, team_name, previous_team, team_submit)
    c.save()

    winning_claim = c
    winning_team = c.current_team
    current_user_is_winning = request.user is not None and request.user.username.lower().strip() == winning_team.lower().strip()

    context = {
        'session': session,
        'leaderboard' : leaderboard,
        'winning_claim' : winning_claim,
        'success_message' : 'Successfully claimed the flag at %s. (For now)'  % (c.last_modified.astimezone(tz.gettz('America/New_York')).strftime("%H:%M %p")),
        'winning_team' : c.current_team,
        'current_user_is_winning' : current_user_is_winning
    }

    print 'current team: %s, request.user.username %s' % (c.current_team, request.user.username)
    print 'current winning team %s' % (current_user_is_winning)

    return HttpResponse(template.render(context, request))

@login_required(login_url='/injection/login')
def my_session(request):
    # look for session
    session = Session.objects.filter(team=request.user).first()

    # if it does not exist, then create
    if (session is None):
        session = Session.create("Private session: %s's" % request.user.username, team=request.user)
        session.save()

    leaderboard = LeaderBoard.objects.filter(session = session).first()
    if (leaderboard is None):
        leaderboard = LeaderBoard.create(session)
        leaderboard.save()

    claim = FlagClaim.objects.filter(leaderboard = leaderboard).first()
    if (claim is None):
        claim = FlagClaim.create(leaderboard, 'Seeding flag', 'Quan', '', request.user)
        claim.save()

    return redirect('/injection/submit/%s/%s' % (session.id, leaderboard.id))



    # then direct into view session


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