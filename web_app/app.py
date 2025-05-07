from flask import Flask, render_template, redirect, url_for, request, session
from rpg_battle_patata.game.language_manager import get_dict
import random, secrets
from game_manager import GameManager
game = GameManager()

app = Flask(__name__)
app.secret_key = secrets.token_hex()


image_table = {
    "Baker" : "static/img/baker.png",
    "NarcissicPerverse" : "static/img/narcissicperverse.png",
    "Gambler" : "static/img/gambler.png",
    "EnyOldMan" : "static/img/enyoldman.png",
    "EnyRageDog" : "static/img/enyragedog.png",
    "Eny" : "static/img/eny.png",
    "EnyElementaryBug" : "static/img/enyelementarybug.png",
    "MagicPlace" : "static/img/magicplace.png",
    "FireCamp" : "static/img/firecamp.png",
    "Chest" : "static/img/chest1.png"
}

def greetings() :
    storytelling = get_dict("storytelling")
    num = random.randint(0, len(storytelling['greetings'])-1)
    return storytelling['greetings'][num]


@app.route('/')
def home():
    if 'lang' not in session :
        session['dico'] = get_dict("webapp_dict")
    return render_template("index.html", request=request)

@app.route('/lang_selection/<lang>')
def lang_selection(lang) :
    session['lang'] = lang
    print(lang)
    session['dico'] = get_dict("webapp_dict")
    return redirect(request.args.get('next', '/'))

@app.route('/about')
def about():
    return render_template("about.html", request=request, dico = get_dict("about_dict"))

@app.route('/char_selection', methods = ["POST", "GET"])
def char_selection() :
    dico = get_dict("characters_dict")
    if request.method == "POST" :
        game.set_player(request.form.get('player'), request.form.get('name'))
        session['name'] = game.player.name
        return redirect(url_for('battle'))
    else :
        if 'name' not in session :
            texts = {"dico" : dico, "greetings" : greetings()}
            return render_template("char_selection.html", texts = texts, request=request)
        else :
            return redirect(url_for('battle'))


@app.route('/battle')
def battle() :
    img = [image_table[game.player.__class__.__name__], image_table[game.enemy.__class__.__name__]]
    return render_template('game.html', game=game, img = img, request=request, dico = get_dict('stats_dict'))

@app.route('/logout', methods=['POST', 'GET'])
def logout() :
    global game
    game = GameManager()
    if 'name' in session :
        session.pop('name')
    return redirect(url_for('home'))

@app.route('/restart', methods=['POST'])
def restart():
    game.restart_game()
    return redirect(url_for('event'))

@app.route('/event', methods=['POST', 'GET'])
def event():
    next_ev = game.event_generator()
    if next_ev == 'magicplace' :
        return redirect(url_for('magic_place'))
    elif next_ev == 'chest' :
        return redirect(url_for('chest'))
    elif next_ev == 'firecamp' :
        return redirect(url_for('fire_camp'))
    else :
        return redirect(url_for('battle'))

@app.route('/action', methods=['POST'])
def action():
    act = request.form.get('action')
    if act :
        game.next_turn_action(player_action=act)
    else:
        game.next_turn_action(player_action=None)
    return redirect(url_for('battle'))

@app.route('/chest', methods=['POST', 'GET'])
def chest():
    act = request.form.get('action')
    if act :
        game.resolve_chest_event(player_action=act)
    else :
        game.resolve_chest_event()
    return render_template('chest.html', game=game, request=request, img = image_table["Chest"])

@app.route('/use_item', methods=['POST'])
def use_item():
    id_item = int(request.form.get('use'))
    if id_item :
        game.player_use_item(id_item)
    return redirect(url_for('battle'))

@app.route("/manage_equipment", methods=['POST'])
def manage_equipment():
    id_item = int(request.form.get('equip')) if request.form.get('equip') else int(request.form.get('unequip'))
    act = 'equip' if request.form.get('equip') else 'unequip'
    game.player_wearable(act, id_item)
    return redirect(url_for('fire_camp'))

@app.route("/fire_camp", methods=['POST', 'GET'])
def fire_camp() :
    act = request.form.get('action')
    if act :
        game.resolve_firecamp_event(player_action=act)
    else :
        game.resolve_firecamp_event()
    return render_template('firecamp.html', game=game, dico = get_dict("events_dict"), request=request,img = image_table["FireCamp"] )

@app.route("/magic_place", methods=['POST', 'GET'])
def magic_place():
    act = request.form.get('action')
    if act :
        game.resolve_magicplace_event(player_action=act)
    else :
        game.resolve_magicplace_event()
    return render_template("magicplace.html", game=game, dico =get_dict("events_dict"), request=request, img = image_table["MagicPlace"])

if __name__ == "__main__":
    app.run(debug=True)
