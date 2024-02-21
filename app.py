from flask import Flask, render_template ,request,redirect,url_for
import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    con = sql.connect('gestion_des_taches.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('SELECT * FROM projects')
    projects = cur.fetchall()
    
    return render_template('index.html',projects = projects)

@app.route('/Add_Project', methods=['POST','GET'])
def Add_Project():
    if request.method == 'POST':
        name = request.form['name']
        con = sql.connect('gestion_des_taches.db')
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('INSERT INTO projects (PNAME) values (?)',(name,))
        con.commit()
        return redirect(url_for('index'))
    return render_template('Add_project.html')
          
@app.route('/Delete_Project/<int:id>' , methods=['POST','GET'])
def Delete_Project(id):
        con = sql.connect('gestion_des_taches.db')
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('DELETE FROM projects WHERE PID= ?',(id,))
        con.commit()
        return redirect(url_for('index'))
    
    
################ TASKS ############################
@app.route('/tache/<int:pid>', methods=['GET','POST'])
def tache(pid):
    con = sql.connect('gestion_des_taches.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('SELECT * FROM tasks WHERE PID=?', (pid,))
    tasks = cur.fetchall()
    return render_template('tache.html', tasks=tasks ,pid = pid)




@app.route('/AddTask/<int:pid>', methods=['GET','POST'])
def AddTask(pid):
    if request.method == 'POST':
        tname = request.form['tname']
        desc = request.form['desc']
        pid = request.form['pid']
        # pid = request.args.get('pid')
        con = sql.connect('gestion_des_taches.db')
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('INSERT INTO tasks (TNAME, DESC, PID) VALUES (?, ?, ?)', (tname, desc, pid))
        con.commit()
        con.close()
        
    con = sql.connect('gestion_des_taches.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('SELECT * FROM tasks  WHERE PID =?',(pid,))
    tasks = cur.fetchall()
    return redirect(url_for('tache',tasks = tasks ,pid=pid))
    
@app.route('/DeleteTask/<int:pid>/<int:tid>')
def DeleteTask(pid, tid):
    con = sql.connect('gestion_des_taches.db')
    con.row_factory = sql.Row 
    cur = con.cursor()
    cur.execute('DELETE FROM  tasks WHERE PID=? AND TID=?',(pid,tid,))   
    con.commit()
    con.close()
    return redirect(url_for('tache' , pid = pid))    
    
@app.route('/EditTask/<int:pid>/<int:tid>' , methods=['GET','POST'])
def EditTask(pid,tid):
    if request.method == 'POST':
        newname = request.form['newname']
        newdesc = request.form['newdesc']
        con = sql.connect('gestion_des_taches.db')
        con.row_factory = sql.Row 
        cur = con.cursor()
        cur.execute('UPDATE tasks SET TNAME=? ,DESC=? WHERE PID=? AND TID=?',(newname,newdesc,pid,tid,))
        con.commit()
        return redirect(url_for('tache' ,pid  = pid))
    con = sql.connect('gestion_des_taches.db')
    con.row_factory = sql.Row 
    cur = con.cursor()
    cur.execute('SELECT * FROM tasks WHERE PID=? AND TID=?',(pid,tid,))
    task  = cur.fetchone()
    return render_template('Edit_task.html', task = task , pid = pid)

# @app.route('/EditTask/<int:id>', methods=['POST', 'GET'])
# def EditTask(id):
#     if request.method == 'POST':
#         newname = request.form['newname']
#         newdesc = request.form['newdesc']
#         con = sql.connect('gestion_des_taches.db')
#         con.row_factory = sql.Row
#         cur = con.cursor()
#         cur.execute('UPDATE tasks SET TNAME=?,DESC=? WHERE TID=?', (newname, newdesc, id,))
#         con.commit()
#         return redirect(url_for('tache'))
    
#     con = sql.connect('gestion_des_taches.db')
#     con.row_factory = sql.Row
#     cur = con.cursor()
#     cur.execute('SELECT * FROM tasks WHERE TID=?', (id,))
#     task = cur.fetchone()
#     con.commit()
    
#     return render_template('Edit_Task.html', row=task)

               
if __name__ == '__main__':
    app.run(debug=True)

