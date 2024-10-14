from _datetime import datetime

from Extensions import DATABASE as db

# Association table for many-to-many relationship between Roster and Player
roster_player = db.Table('roster_player',
    db.Column('roster_id', db.Integer, db.ForeignKey('roster.id')),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'))
)

# User model with optional fields
class User(db.Model):
    id = db.Column(db.String, primary_key=True)  # Unique token
    picture = db.Column(db.String, nullable=True)
    family_name = db.Column(db.String, nullable=False)
    given_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    preferred_firstname = db.Column(db.String, nullable=True)
    preferred_lastname = db.Column(db.String, nullable=True)
    preferred_email = db.Column(db.String, nullable=True)
    school_year = db.Column(db.String, nullable=True)

    # Relationship to Coach (if the user is a coach)
    coach = db.relationship('Coach', back_populates='user', uselist=False)

    def to_dict(self):
        return {
            'id': self.id,
            'picture': self.picture,
            'family_name': self.family_name,
            'given_name': self.given_name,
            'email': self.email,
            'preferred_firstname': self.preferred_firstname,
            'preferred_lastname': self.preferred_lastname,
            'preferred_email': self.preferred_email,
            'school_year': self.school_year
        }

# Coach model linking User to Team
class Coach(db.Model):
    user_id = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', back_populates='coach')
    team = db.relationship('Team', back_populates='coach', uselist=False)

# Team model linking to Coach and Rosters
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    coach_id = db.Column(db.String, db.ForeignKey('coach.user_id'))
    coach = db.relationship('Coach', back_populates='team')
    rosters = db.relationship('Roster', back_populates='team')

# Player model
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    # Additional fields can be added as needed

    # Many-to-many relationship with Roster
    rosters = db.relationship('Roster', secondary=roster_player, back_populates='players')

# Match model linking two teams and optional scores
class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    team1_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team2_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team1_goals = db.Column(db.Integer, nullable=True)
    team2_goals = db.Column(db.Integer, nullable=True)
    winner_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)

    team1 = db.relationship('Team', foreign_keys=[team1_id], backref='matches_as_team1')
    team2 = db.relationship('Team', foreign_keys=[team2_id], backref='matches_as_team2')
    winner_team = db.relationship('Team', foreign_keys=[winner_team_id], backref='wins')

    rosters = db.relationship('Roster', back_populates='match')

# Roster model linking Team, Match, and Players
class Roster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'))

    team = db.relationship('Team', back_populates='rosters')
    match = db.relationship('Match', back_populates='rosters')
    players = db.relationship('Player', secondary=roster_player, back_populates='rosters')
