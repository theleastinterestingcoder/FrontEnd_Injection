# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Session(models.Model):
    name = models.CharField(max_length=200, unique=True)
    team = models.OneToOneField(User, unique=True, blank=True, null=True)

    @classmethod
    def create(cls, name, team=None):
        session = cls(name=name, team=team)
        return session

class LeaderBoard(models.Model):
    session = models.ForeignKey(Session)

    @classmethod
    def create(cls, session):
        leaderboard = cls(session = session)
        return leaderboard
    @property
    def sorted_flagclaim_set(self):
        return self.flagclaim_set.order_by('-last_modified')

class FlagClaim(models.Model):
    team_submit = models.ForeignKey(User, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    leaderboard = models.ForeignKey(LeaderBoard, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    current_team = models.CharField(max_length=255)
    previous_team = models.CharField(max_length=255)

    @classmethod
    def create(cls, leaderboard, comment, current_team, previous_team, team_submit = None):
        claim = cls(team_submit=team_submit, leaderboard=leaderboard, current_team=current_team, previous_team=previous_team, comment=comment)
        return claim


