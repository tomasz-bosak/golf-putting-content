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

            if guestId == "" :
                flash('Guest not known', category='error')
            elif host == guest:
                flash('Cannot play with yourself', category='error')
            else:
                new_game = Game(host_id = current_user.id, guest_id = guestId.id, host_score = host_score, guest_score= guest_score, accepted=False)
                db.session.add(new_game)
                db.session.commit()
                flash('Note added', category='success')
        print(current_user.game_host)
        all_players = User.query.all()
        return render_template("home.html", user=current_user, players=all_players)


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
