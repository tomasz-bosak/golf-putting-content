from flask import Blueprint, render_template, request, flash,jsonify
from flask_login import login_required,  current_user
from .models import Game, User
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
        if request.method == 'POST':
            data = request.form
            print(data)

            host = request.form.get('host')
            guest = request.form.get('guest')
            host_score = request.form.get('host_score')
            guest_score = request.form.get('guest_score')

            guestId = User.query.filter_by(email=guest).first()

            if not guestId:
                flash('Guest user not known', category='error')
            elif host == guest:
                flash('Cannot play with yourself', category='error')
            elif float(host_score) + float(guest_score) != 9:
                flash('Game should consist of 9 holes (sum of points should be 9)', category='error')
            else:
                new_game = Game(host_id = current_user.id, guest_id = guestId.id, host_score = host_score, guest_score= guest_score, accepted=False)
                db.session.add(new_game)
                db.session.commit()
                flash('Note added', category='success')
        print(current_user.game_host)
        print(current_user.game_guest)
        print(len(current_user.game_host)+len(current_user.game_guest))
        all_players = sorted(User.query.all(), key= lambda d : d.first_name)
        return render_template("home.html", user=current_user, players=all_players)

@views.route('/ranking', methods=['GET', 'POST'])
def ranking():
        all_players = User.query.all()
        for player in all_players:
             if not player.index:
                  player.index = 800.0

        return render_template("rank.html", user=current_user, players=all_players)

@views.route('/delete-game', methods=['POST'])
def delete_game():
    gamed = json.loads(request.data)
    gameId = gamed['gameId']
    print (f"trying to delete game: {gameId}")
    game = Game.query.get(gameId)
    if game:
        if game.host_id == current_user.id or game.guest_id == current_user.id:
            db.session.delete(game)
            db.session.commit()
    return jsonify({})

@views.route('/accept-game', methods=['POST'])
def accept_game():
    gamed = json.loads(request.data)
    gameId = gamed['gameId']
    print (f"accepting game: {gameId}")
    game = Game.query.get(gameId)
    if game:
        if game.host_id == current_user.id or game.guest_id == current_user.id:
            game.accepted=True

            # recalculate scores
            p1 = User.query.get(game.host_id)
            p2 = User.query.get(game.guest_id)

            s1 = game.host_score
            s2 = game.guest_score

            sb1 = p1.index or 800
            sb2 = p2.index or 800
            if sb1 < 800:
                sb1 = 800
            if sb2 < 800:
                sb2 = 800

            K = 16 # 32/2
            D = 0.04  # K/4C = 32/4*200

            sa1  = sb1 + K* ( s1 - s2) - D*(sb1 - sb2)
            sa2  = sb2 + K* ( s2 - s1) - D*(sb2 - sb1)
            print(f"Recalculating score:\nGame: {s1}:{s2}\n{p1.email} {sb1} -> {sa1}\n{p2.email} {sb2} -> {sa2}")
            p1.index = sa1
            p2.index = sa2

            db.session.commit()
    return jsonify({})
