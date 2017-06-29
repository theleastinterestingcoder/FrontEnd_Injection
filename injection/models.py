# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Session(models.Model):
    team_name = models.CharField(max_length=200, unique=True)
    number_of_resets = models.IntegerField(default=0)
    number_of_submission_attempts = models.IntegerField(default=0)
    IsSolved = models.BooleanField(default=True)

    @classmethod
    def create(cls, team_name):
        session = cls(team_name=team_name)
        return session

class Seating(models.Model):
    member = models.CharField(max_length=200)
    guest = models.CharField(max_length=200)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    @classmethod
    def create(cls, session, member, guest):
        seating = cls(session=session, member=member, guest=guest)
        return seating

# class LeaderBoard(models.Model):
#     @classmethod
#     def create(cls):
#         leaderboard = cls()
#         return leaderboard

# class Session(models.Model):
#     