#
# ██████╗ ██╗  ██╗██████╗ ██╗    ██╗       ██████╗ ██████╗ ███╗   ██╗███╗   ██╗███████╗ ██████╗████████╗
# ██╔══██╗██║  ██║██╔══██╗██║    ██║      ██╔════╝██╔═══██╗████╗  ██║████╗  ██║██╔════╝██╔════╝╚══██╔══╝
# ██║  ██║███████║██████╔╝██║ █╗ ██║█████╗██║     ██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██║        ██║
# ██║  ██║██╔══██║██╔══██╗██║███╗██║╚════╝██║     ██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██║        ██║
# ██████╔╝██║  ██║██████╔╝╚███╔███╔╝      ╚██████╗╚██████╔╝██║ ╚████║██║ ╚████║███████╗╚██████╗   ██║
# ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚══╝╚══╝        ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝ ╚═════╝   ╚═╝
#
# Testaccount: E-Mail: test123@mail.de / PW: tester1
# _____________________________________________________________________________________________________________________

from flask import Flask, render_template, session, redirect, request
from werkzeug.security import generate_password_hash, check_password_hash
import speech_recognition as sr
import pyttsx3
import psycopg2
import pywhatkit

app = Flask(__name__)

app.secret_key = '#*ÜÖÄ---:,,."§!)?KLON;;;;...;234kayak8888walkGVSSBRAA--....yy.aö09348u)=!(§$"(/)????§($&'

con = psycopg2.connect(
    host='ec2-3-248-103-75.eu-west-1.compute.amazonaws.com',
    dbname='dccg1q7f25lefn',
    user='jsopdlybnrgqys',
    password='b0d7a5b2b9e080b3fa709b19596e51ed645857aba9c83f8ac1a459289f6ab9f3')


# Standardroutinen
# _____________________________________________________________________________________________________________________
@app.route('/')
def link_matching():
    if session.get('user'):
        try:
            return render_template('Matching.html')
        finally:
            return redirect('/show_profile')
    else:
        return render_template('Login.html')


@app.route('/Registrierung')
def link_registrieren():
    return render_template('Registrieren.html')


@app.route('/match_gruppe')
def match_gruppe():
    if session.get('user'):
        try:
            return render_template('Matching_Group.html')
        finally:
            return redirect('/show_group')
    else:
        return render_template('Login.html')


@app.route('/GruppeErstellen')
def link_gruppe():
    if session.get('user'):
        return render_template('Gruppe_erstellen.html')
    else:
        return render_template('Login.html')


@app.route('/TerminErstellen')
def termin_erstellen():
    if session.get('user'):
        return render_template('termin_erstellen.html')
    else:
        return render_template('Login.html')


@app.route('/Einstellungen')
def link_einstellungen():
    if session.get('user'):
        return render_template('Einstellungen.html')
    else:
        return render_template('Login.html')


@app.route('/meinProfil')
def link_profil():
    if session.get('user'):
        return redirect('/termin_match_ausgeben')
    else:
        return render_template('Login.html')


@app.route('/ProfilBearbeiten')
def link_profil_bearb():
    if session.get('user'):
        return render_template('Account_Bearbeiten.html')
    else:
        return render_template('Login.html')


@app.route('/404')
def err_page():
    return render_template('404.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.clear()
    return redirect('/')


# Anmelden/Registrieren
# _____________________________________________________________________________________________________________________
@app.route('/Anmelden', methods=['POST'])
def anmelden():
    cur = con.cursor()

    try:
        email = request.form['inputEmail']
        passwort = request.form['inputPassword']

        cur = con.cursor()
        cur.execute("SELECT id ,passwort FROM nutzer WHERE Email = %(email)s;", {'email': email})

        ergebnis = cur.fetchone()

        if ergebnis is not None:
            ergebnis = list(ergebnis)

            if check_password_hash(str(ergebnis[1]), passwort):

                session['user'] = ergebnis[0]
                return redirect('/')

            else:
                return render_template('Login.html')

        else:
            return render_template('Login.html')

    finally:
        cur.close()


@app.route('/registrieren', methods=['POST', 'GET'])
def registrieren():
    cur = con.cursor()

    try:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['confirmPW']
        number = request.form['number']
        dhbw = request.form['dhbw']
        studiengang = request.form['studiengang']
        alter = request.form['age']
        interesse = request.form['interesse']

        if username and email and password and password_confirm and number and dhbw and studiengang and alter and interesse:

            cur.execute("SELECT count(*) FROM nutzer WHERE email = %(email)s", {'email': email})

            result = cur.fetchone()[0]

            if result < 1:
                if password != password_confirm:
                    return render_template('Registrieren.html')

                else:
                    hashed_password = generate_password_hash(password)

                    cur.execute("SELECT count(*) FROM dhbw where name = %(dhbwName)s", {'dhbwName': dhbw})
                    dhbw_count = cur.fetchone()[0]

                    if dhbw_count < 1:
                        cur.execute("INSERT INTO dhbw(name) VALUES(%(dhbwName)s)", {'dhbwName': dhbw})
                        con.commit()

                    cur.execute("SELECT id FROM dhbw where name = %(dhbwName)s", {'dhbwName': dhbw})
                    dhbw = cur.fetchone()[0]

                    cur.execute("SELECT count(*) FROM studiengang where name = %(sgang)s", {'sgang': studiengang})
                    studiengang_count = cur.fetchone()[0]

                    if studiengang_count < 1:
                        cur.execute("INSERT INTO studiengang(name) VALUES(%(sgang)s)", {'sgang': studiengang})
                        con.commit()

                    cur.execute("SELECT id FROM studiengang where name = %(sgang)s", {'sgang': studiengang})
                    studiengang = cur.fetchone()[0]

                    cur.execute(
                        "INSERT INTO nutzer (email, passwort, username, telefonnummer, alter, dhbw_id, sgang_id, interesse) "
                        "VALUES (%(email)s, %(pass)s, %(nickname)s, %(number)s, %(age)s, %(dhbw)s, %(sgang)s, %(interesse)s)",
                        {'email': email, 'pass': hashed_password, 'nickname': username, 'number': number, 'age': alter,
                         'dhbw': dhbw, 'sgang': studiengang, 'interesse': interesse})

                    con.commit()
                    return render_template('Login.html')
            else:
                return render_template('Registrieren.html')
    finally:
        cur.close()


# Match User/Gruppe
# _____________________________________________________________________________________________________________________
"""@app.route('/like')
def like():
    cur = con.cursor()
    try:
        aktiv = session['user']
        cur.execute("SELECT n.id, n.username, n.alter, i.name, d.name, s.name from nutzer n, interesse i,dhbw d, studiengang s WHERE n.interesse = i.id AND n.dhbw_id = d.id AND n.sgang_id = s.id "
                    "AND n.id <> %(id)s ORDER BY RANDOM()", {"id": aktiv})
        ergebnis = cur.fetchone()
        id_like, nutzer, alter, interesse, dhbw, studiengang = ergebnis[0], ergebnis[1], ergebnis[2], ergebnis[3], ergebnis[4], ergebnis[5]
        
        cur.execute("SELECT u2_id from liked WHERE u1_id = %(u_partner)s", {'u_partner': id_like})
        u2 = cur.fetchall()
        for (x) in u2:
            if x != aktiv:
                print("Match")
                cur.execute("INSERT INTO matched (u1_id, u2_id) VALUES (%(u_aktiv)s, %(u_partner)s)", {'u_aktiv': aktiv, 'u_partner': id_like})
                con.commit()
                return render_template('Matching.html', nutzer=nutzer, alter=alter, interesse=interesse, dhbw=dhbw, studiengang=studiengang)
            break
        else:
            print("Like")
            cur.execute("INSERT INTO liked (u1_id, u2_id) VALUES (%(u_aktiv)s, %(u_partner)s)", {'u_aktiv': aktiv, 'u_partner': id_like})
            con.commit()
            return render_template('Matching.html', nutzer=nutzer, alter=alter, interesse=interesse, dhbw=dhbw, studiengang=studiengang)
    finally:
        cur.close()"""


@app.route('/show_profile', methods=['GET'])
def show_profile():
    cur = con.cursor()
    try:
        aktiv = session['user']
        cur.execute(
            "SELECT username, alter, i.name, d.name, s.name from nutzer n, interesse i, dhbw d, studiengang s where n.interesse = i.id AND n.dhbw_id = d.id "
            "AND n.sgang_id = s.id AND n.id <> %(id)s ORDER BY RANDOM()", {"id": aktiv})
        ergebnis = cur.fetchone()
        nutzer, alter, interesse, dhbw, studiengang = ergebnis[0], ergebnis[1], ergebnis[2], ergebnis[3], ergebnis[4]
        nutzer_like = ergebnis[0]
        cur.execute("INSERT INTO zwischenspeicher (nutzer_like) VALUES(%(nutzer)s)", {'nutzer': nutzer_like})
        cur.execute("SELECT count(*) FROM liked where u1_id = %(aktiv)s AND u2_id = (SELECT id FROM nutzer WHERE username = %(nutzer)s)", {'aktiv': aktiv, 'nutzer': nutzer})
        ergebnis = cur.fetchone()[0]
        if ergebnis == 0:
            return render_template('Matching.html', nutzer=nutzer, alter=alter, interesse=interesse, dhbw=dhbw, studiengang=studiengang)
        else:
            cur.execute(
                "SELECT COUNT(*) from nutzer n, interesse i, dhbw d, studiengang s where n.interesse = i.id AND n.dhbw_id = d.id AND n.sgang_id = s.id AND n.id <> %(id)s AND n.id <> (SELECT id FROM "
                "nutzer WHERE username = %(nutzer2)s) ORDER BY RANDOM()",
                {"id": aktiv, 'nutzer2': nutzer})
            return render_template('Matching.html', nutzer='Kein neuer Nutzer', alter='', interesse='', dhbw='', studiengang='')
    finally:
        cur.close()


@app.route('/like')
def like():
    cur = con.cursor()
    try:
        cur.execute("SELECT nutzer_like FROM zwischenspeicher ")
        nutzer_like = cur.fetchall()[-1]
        cur.execute("SELECT id FROM nutzer WHERE username = %(nutzer_like)s", {'nutzer_like': nutzer_like})
        partner = cur.fetchone()[0]
        aktiv = session['user']
        cur.execute("SELECT u2_id from liked WHERE u1_id = %(u_partner)s", {'u_partner': partner})
        u2 = cur.fetchall()
        for (x) in u2:
            if x != aktiv:
                print("Match")
                cur.execute("INSERT INTO matched (u1_id, u2_id) VALUES (%(u_aktiv)s, %(u_partner)s)", {'u_aktiv': aktiv, 'u_partner': partner})
                cur.execute("INSERT INTO liked (u1_id, u2_id) VALUES (%(u_aktiv)s, %(u_partner)s)", {'u_aktiv': aktiv, 'u_partner': partner})
                con.commit()
                return redirect('/delete_zwischenspeicher')
            break
        else:
            print("Like")
            cur.execute("INSERT INTO liked (u1_id, u2_id) VALUES (%(u_aktiv)s, %(u_partner)s)", {'u_aktiv': aktiv, 'u_partner': partner})
            con.commit()
            return redirect('/delete_zwischenspeicher')
        return redirect('/delete_zwischenspeicher')
    finally:
        cur.close()


@app.route('/delete_zwischenspeicher')
def delete():
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM zwischenspeicher")
        return redirect('/show_profile')
    finally:
        cur.close()


@app.route('/dislike')
def dislike():
    cur = con.cursor()
    try:
        return redirect('/show_profile')
    finally:
        cur.close()


@app.route('/like_group')
def like_group():
    cur = con.cursor()
    try:
        cur.execute("SELECT id, name, interesse from gruppe ORDER BY RANDOM()")
        ergebnis = cur.fetchone()
        id_group, name, interesse = ergebnis[0], ergebnis[1], ergebnis[2]
        cur.execute("SELECT i.name FROM interesse i, gruppe g WHERE i.id = g.interesse")
        interesse = cur.fetchone()[0]
        cur.execute("SELECT link FROM gruppe WHERE id = %(akt_gruppe)s", {'akt_gruppe': id_group})
        link = cur.fetchone()[0]
        return render_template('Matching_Group.html', gruppe=name, interesse=interesse, link=link)
    finally:
        cur.close()


@app.route('/dislike_group', methods=['GET'])
def dislike_group():
    cur = con.cursor()
    try:
        cur.execute("SELECT id, name, interesse from gruppe ORDER BY RANDOM()")
        ergebnis = cur.fetchone()
        id_dislike_group, name, interesse = ergebnis[0], ergebnis[1], ergebnis[2]
        cur.execute("SELECT i.name FROM interesse i, gruppe g WHERE i.id = g.interesse")
        interesse = cur.fetchone()[0]
        return render_template('Matching_Group.html', gruppe=name, interesse=interesse)
    finally:
        cur.close()


@app.route('/match_group')
def match_group():
    cur = con.cursor()
    try:
        aktiv = session['user']
        cur.execute("SELECT n.username FROM nutzer n, matched m where u1_id = %(u_aktiv)s and m.u2_id = n.id", {'u_aktiv': aktiv})
        ergebnis = cur.fetchall()
        return render_template('Profil.html', ergebnis=ergebnis)
    finally:
        cur.close()


@app.route('/show_group')
def show_group():
    cur = con.cursor()
    try:
        cur.execute("SELECT id, name, interesse from gruppe ORDER BY RANDOM()")
        ergebnis = cur.fetchone()
        id_show_group, name, interesse = ergebnis[0], ergebnis[1], ergebnis[2]
        cur.execute("SELECT i.name FROM interesse i, gruppe g WHERE i.id = g.interesse")
        interesse = cur.fetchone()[0]
        return render_template('Matching_Group.html', gruppe=name, interesse=interesse)
    finally:
        cur.close()


# Profil Bearbeiten
# _____________________________________________________________________________________________________________________
@app.route('/usernameAendern', methods=['POST'])
def profil_aendern():
    cur = con.cursor()
    try:
        username = request.form['new_username']
        if session.get('user'):
            aktiv = session['user']
            cur.execute("UPDATE nutzer SET username = %(u_name)s WHERE id= %(aktiv)s", {'u_name': username, 'aktiv': aktiv})
            con.commit()
            return redirect('/ProfilBearbeiten')
        else:
            return redirect('/')
    finally:
        cur.close()


@app.route('/EmailAendern')
def email_aendern():
    cur = con.cursor()
    try:
        email = request.form['new_email']
        if session.get('user'):
            if len(email) > 0:
                cur.execute("SELECT count(*) FROM nutzer WHERE email = %(mail)s;", {'mail': email})
                result = cur.fetchone()[0]
                if result < 1:
                    aktiv = session['user']
                    cur.execute("UPDATE nutzer SET email = %(email)s WHERE id = %(aktiv)s;", {'email': email, 'aktiv': aktiv})
                    con.commit()
                    return render_template('Account_Bearbeiten.html')
                else:
                    return render_template('Account_Bearbeiten.html')
            else:
                return render_template('Account_Bearbeiten.html')
        else:
            return redirect('Login.html')
    finally:
        cur.close()


@app.route('/passwortAendern', methods=['POST'])
def passwort_aendern():
    cur = con.cursor()

    try:
        password = request.form['new_password']
        passwordconfirm = request.form['confirm_new_password']

        if session.get('user'):
            if len(password) and len(passwordconfirm) > 0:
                if password == passwordconfirm:
                    aktiv = (session['user'])
                    hashed_password = generate_password_hash(password)

                    cur.execute("UPDATE nutzer SET passwort = %(pass)s WHERE id = %(aktiv)s;", {'pass': hashed_password, 'aktiv': aktiv})
                    con.commit()
                    return render_template('Account_Bearbeiten.html')

        else:
            return render_template('Login.html')
    finally:
        cur.close()


@app.route('/AccountLoeschen', methods=['POST'])
def AccountLoeschen():
    cur = con.cursor()
    try:
        aktiv = session['user']
        cur.execute("DELETE FROM nutzer WHERE id = %(aktiv)s", {'aktiv': aktiv})
        con.commit()
        return render_template('Login.html')

    finally:
        cur.close()


# Weitere Funktionen
# _____________________________________________________________________________________________________________________
@app.route('/gruppenerstellung', methods=['POST', 'GET'])
def gruppenerstellung():
    cur = con.cursor()

    try:
        name = request.form['groupname']
        link = request.form['whatsappLink']
        interesse = request.form['interesse']

        if name and link and interesse:

            cur.execute("SELECT count(*) FROM gruppe WHERE name = %(name)s", {'name': name})
            result = cur.fetchone()[0]

            if result > 0:
                return render_template('Registrieren.html')
            else:
                cur.execute("INSERT INTO gruppe(name, link, interesse) VALUES(%(name)s,%(link)s,%(interesse)s)",
                            {'name': name, 'link': link, 'interesse': interesse})
                con.commit()

                return render_template('Gruppe_erstellen.html')
        else:
            return render_template('Gruppe_erstellen.html')
    finally:
        cur.close()


@app.route('/termin_eintragen', methods=['POST'])
def termin_eintragen():
    cur = con.cursor()
    try:
        partner = request.form['partnername']
        datum = request.form['datumTermin']
        uhrzeit = request.form['uhrzeitTermin']
        aktiv = session['user']

        cur.execute("insert into termine(nutzer_id, partner, datum, uhrzeit) values(%(u_aktiv)s, %(u_partner)s, %(datum)s, %(uhrzeit)s);",
                    {'u_aktiv': aktiv, 'u_partner': partner, 'datum': datum, 'uhrzeit': uhrzeit})
        con.commit()
        return render_template('termin_erstellen.html')
    finally:
        cur.close()


@app.route('/termin_match_ausgeben', methods=['GET'])
def termin_ausgeben():
    cur = con.cursor()
    try:
        aktiv = session['user']
        cur.execute("SELECT n.username, n.email FROM nutzer n, matched m where u1_id = %(u_aktiv)s and m.u2_id = n.id", {'u_aktiv': aktiv})
        ergebnis = cur.fetchall()
        cur.execute("SELECT partner, datum, uhrzeit FROM termine where nutzer_id = %(u_aktiv)s", {'u_aktiv': aktiv})
        termine = cur.fetchall()
        return render_template('Profil.html', termine=termine, ergebnis=ergebnis)
    finally:
        cur.close()


@app.route('/speech')
def speech():
    cur = con.cursor()
    listener = sr.Recognizer()
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    de_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_DE-DE_HEDDA_11.0"
    engine.setProperty('voice', de_voice_id)

    aktiv = session['user']
    cur.execute("select username from nutzer where id = %s", (aktiv,))
    aktiv = cur.fetchone()[0]
    engine.say('Hallo ' + aktiv)
    engine.runAndWait()

    with sr.Microphone() as source:
        voice = listener.listen(source)
        command = listener.recognize_google(voice, language="de-DE")
        command = command.lower()

        if 'connect' in command:
            if 'zeige' in command:
                cur.execute("select * from termine where datum = CAST(CURRENT_TIMESTAMP AS VARCHAR)")
                engine.say(cur.fetchall())
                engine.runAndWait()
                return redirect('/meinProfil')
            if 'wer bin ich' in command:
                aktiv = session['user']
                cur.execute("select username from nutzer where id = %s", (aktiv,))
                engine.say('Du bist ' + cur.fetchone()[0])
                engine.runAndWait()
                return redirect('/Home')
            if 'lösche' in command:
                aktiv = session['user']
                cur.execute("DELETE FROM nutzer WHERE id = %(aktiv)s", {'aktiv': aktiv})
                con.commit()
                engine.say('Der Account wurde gelöscht.')
                engine.runAndWait()
                pywhatkit.playonyt('Cro Bye Bye')
                return redirect('Login.html')
            if 'löschen' in command:
                aktiv = session['user']
                cur.execute("DELETE FROM nutzer WHERE id = %(aktiv)s", {'aktiv': aktiv})
                con.commit()
                engine.say('Der Account wurde gelöscht.')
                engine.runAndWait()
                pywhatkit.playonyt('Cro Bye Bye')
                return redirect('Login.html')
            if 'mein profil' in command:
                return redirect('/meinProfil')
            if 'profil bearbeiten' in command:
                return redirect('/ProfilBearbeiten')
            if 'gruppe erstellen' in command:
                return redirect('/GruppeErstellen')
            if 'benutzer matchen' in command:
                return redirect('/')
            if 'gruppe matchen' in command:
                return redirect('/gruppe_matchen')
            if 'ausloggen' in command:
                return redirect('/logout')
        else:
            engine.say('Ich habe dich leider nicht verstanden. Viel Spaß noch beim Matchen.')
            engine.runAndWait()
            return redirect('/Home')

        engine.say('Ich habe dich leider nicht verstanden. Viel Spaß noch beim Matchen.')
        engine.runAndWait()
        return redirect('/Home')


# App
# _____________________________________________________________________________________________________________________
if __name__ == "__main__":
    app.run(debug=True)
