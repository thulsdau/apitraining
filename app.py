#!/usr/bin/env python

from bottle import get, post, run, debug, static_file, template, request, redirect, response, default_app
import sqlite3
import random
import re

cookie_secret = ''.join([random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(0,32)])

@get('/')
def get_home():
    c_training = request.get_cookie("training", secret=cookie_secret)
    c_username = request.get_cookie("username", secret=cookie_secret)
    if not c_training or not c_username:
        return redirect('/login')
    if c_training == 'admin':
        return redirect('/training')
    else:
        return redirect('/training/%s' % c_training)

@get('/login')
def get_login():
    return template('login',login='')

@post('/login')
def post_login():
    training = request.forms.get('training')
    password = request.forms.get('password')
    username = request.forms.get('username')
    conn = sqlite3.connect('apitraining.db')
    c = conn.cursor()
    c.execute("SELECT rowid FROM trainings WHERE name = ? and password = ?;", (training,password))
    result = c.fetchone()
    c.close()
    if result != None:
        response.set_cookie("training", training, secret=cookie_secret)
        response.set_cookie("username", username, secret=cookie_secret)
        if training == 'admin':
            redirect("/training")
        else:
            redirect("/training/%s" % training)
    else:
        return template('login',login='failure')

@get('/logout')
def get_logout():
    response.set_cookie("training", "", secret='invalid', expires=0)
    response.set_cookie("username", "", secret='invalid', expires=0)
    return template('login',login='loggedout')

@get('/training')
def get_training_overview():
    c_training = request.get_cookie("training", secret=cookie_secret)
    username   = request.get_cookie("username", secret=cookie_secret)
    if c_training != 'admin':
        return redirect('/training/%s' % c_training)
    conn = sqlite3.connect('apitraining.db')
    c = conn.cursor()
    c.execute("SELECT name, description FROM trainings WHERE name != 'admin';")
    result = c.fetchall()
    c.close()
    return template('training_overview',trainings=result)

@get('/training/<training>')
def get_training(training):
    c_training = request.get_cookie("training", secret=cookie_secret)
    username   = request.get_cookie("username", secret=cookie_secret)
    if training != c_training and c_training != 'admin':
        return template('login',login='failure')
    conn = sqlite3.connect('apitraining.db')
    c = conn.cursor()
    c.execute("SELECT rowid, name FROM exercises WHERE training = ? ORDER BY name;",(training,))
    exercises = c.fetchall()
    if c_training == 'admin':
        c.execute("SELECT e.rowid, e.name, s.username, s.solution, s.submit_timestamp, s.correct FROM exercises as e, submitted_solutions as s WHERE e.rowid=s.exercise_id and e.training = ? ORDER BY s.username, e.name, s.correct DESC;",(training,))
    else:
        c.execute("SELECT e.rowid, e.name, s.username, s.solution, s.submit_timestamp, s.correct FROM exercises as e, submitted_solutions as s WHERE e.rowid=s.exercise_id and e.training = ? and s.username = ? ORDER BY e.name, s.correct DESC;",(training,username))
    solutions = c.fetchall()
    c.close()
    users = []
    user_solutions = {}
    for solution in solutions:
        if not solution[2] in user_solutions:
            user_solutions[solution[2]] = {}
            users.append(solution[2])
        if not solution[0] in user_solutions[solution[2]]:
            user_solutions[solution[2]][solution[0]] = []
        user_solutions[solution[2]][solution[0]].append([solution[5],solution[3],solution[4]])
    return template('training',training=training,username=username,exercises=exercises,users=users,user_solutions=user_solutions)

@get('/solutions/training/<training>/username/<username>')
def get_solutions_for_username(training,username):
    c_training = request.get_cookie("training", secret=cookie_secret)
    c_username   = request.get_cookie("username", secret=cookie_secret)
    if c_training not in (training, 'admin'):
        return redirect('/login')
    if c_training != 'admin' and c_username != username:
        return redirect('/login')
    conn = sqlite3.connect('apitraining.db')
    c = conn.cursor()
    c.execute("SELECT e.rowid, e.name, s.username, s.solution, s.submit_timestamp, s.correct FROM exercises as e, submitted_solutions as s WHERE e.rowid=s.exercise_id and e.training = ? and s.username = ? ORDER BY e.name, s.submit_timestamp;",(training,username))
    solutions = c.fetchall()
    return template('solutions',solutions = solutions, training = training)

@post('/submit')
def submit():
    submission = request.json
    if not submission:
        return {'result':'ERROR','reason': 'Expect input as json. Maybe "Content-type" not set to "application/json"?'}
    #get all parameters and return with error if one is missing
    try:
        training = submission['training']
        password = submission['password']
        username = submission['username']
        exercise = submission['exercise']
        solution = submission['solution']
    except KeyError as e:
        return {'result':'ERROR','reason':'Mandatory parameter %s missing.' % str(e)}
    #check username
    if username == 'None' or username == 'CCO ID':
        return {'result':'ERROR','reason':'Please provide your own name/CCO ID as username.'}
    #connect to database
    conn = sqlite3.connect('apitraining.db')
    c = conn.cursor()
    #check if training and password are valid
    c.execute("SELECT rowid FROM trainings WHERE name = ? and password = ?;", (training,password))
    result = c.fetchone()
    if result == None:
        c.close();
        return {'result':'ERROR','reason':'Training unknown or password not valid.'}
    #get exercise from db, return error if exercise doesn't exist
    c.execute("SELECT rowid, name, solution_type, solution FROM exercises WHERE training = ? and name = ?;",(training,exercise))
    result = c.fetchone()
    if result == None:
        c.close();
        return {'result':'ERROR','reason':'Exercise "%s" unknown.' % exercise}
    exercise_id = result[0]
    solution_type = result[2]
    correct_solution = result[3]
    #check if solution is correct
    correct = False
    if solution_type == 'string':
        if str(solution) == correct_solution:
            correct = True
    elif solution_type == 'regexp':
        if re.match(correct_solution,str(solution)):
            correct = True
    #ergebnis in DB speichern
    c.execute("INSERT INTO submitted_solutions (exercise_id, username, correct, solution) VALUES (?,?,?,?);",(exercise_id, username, correct, str(solution)))
    conn.commit();
    c.close();
    if correct:
        result = 'SUCCESS'
        reason = 'Provided solution is correct.'
    else:
        result = 'FAILURE'
        reason = 'Provided solution is incorrect.'
    return {'result': result, 'reason': reason}

if __name__ == '__main__':    
    debug(True)
    #static cookie secret for developing, so one don't has to relogin everytime
    cookie_secret = 'dbe404a72766da075ffa3bf798615c0b'
    
    #only serve static files while developing
    @get('/static/<filename:path>')
    def send_static(filename):
        return static_file(filename, root='static')
    
    run(host='localhost', port=8080, reloader=True, )
else:
    application = default_app()