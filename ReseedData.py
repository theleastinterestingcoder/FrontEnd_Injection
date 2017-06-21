# usage: python manage.py shell < ReseedData.py 
from injection.models import Session
from injection.models import Seating

print 'Deleting existing sessions...'
Session.objects.all().delete()

print 'Recreating test sessions...'
s = Session.create('TestTeam1')
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