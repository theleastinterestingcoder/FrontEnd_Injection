# usage: python manage.py shell < ReseedData.py 
from injection.models import Session, LeaderBoard, FlagClaim
from injection.models import Seating

print 'Deleting existing sessions...'
Session.objects.all().delete()

print 'Recreating test sessions...'
s = Session.create('Open Session')
s.save()
Seating.create(s, 'Linan Qiu', 'Jenny Liu').save()
Seating.create(s, 'Steve Swanson', 'Becky').save()
Seating.create(s, 'Travis Vanderstud', 'TBD').save()

s = Session.create('TestTeam2')
s.save()
Seating.create(s, 'Linan Qiu', 'Jenny Liu').save()
Seating.create(s, 'Steve Swanson', 'Becky').save()
Seating.create(s, 'Travis Vanderstud', 'TBD').save()

s = Session.create('TestTeam3')
s.save()
Seating.create(s, 'Linan Qiu', 'Jenny Liu').save()
Seating.create(s, 'Steve Swanson', 'Becky').save()
Seating.create(s, 'Travis Vanderstud', 'TBD').save()

# Session.objects.all()

manage.py sqlclear
python manage.py migrate injection zero
python manage.py flush
python manage.py migrate --fake injection zero

python manage.py makemigrations
python manage.py makemigrations injection


!python manage.py flush
from django.contrib.auth.models import User
from injection.models import Session, LeaderBoard, FlagClaim

testuser = User.objects.create_user('chris.fawcett', '', 'testing')

s = Session.create('Open Session')
s.save()
l = LeaderBoard.create(s)
l.save()
c = FlagClaim.create(l, "Seeding Flag", "Quan", "[Nobody]", testuser)
c.save()
c = FlagClaim.create(l, "First blood", "Steve", "Quan", testuser)
c.save()
c = FlagClaim.create(l, "Taking Flag back",  "Quan",  "Steve",testuser)
c.save()
c = FlagClaim.create(l, "All you guys suck", "Linan", "Quan",  testuser)
c.save()