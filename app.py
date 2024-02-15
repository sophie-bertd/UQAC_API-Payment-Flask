from flask import Flask, render_template, request
import sqlite3 as sql


#conn = sql.connect('repTel.db')
#cur = conn.cursor()
#cur.execute("create table contact (id_contact int, name text, last_name text, address text, primary key(id_contact))")
#cur.execute("create table repertory (id_repertory int, id_contact int, phone int, primary key(id_repertory))")
#conn.commit()
#cur.close()
#conn.close()

#conn = sql.connect ("repTel.db")
#cur = conn.cursor()
#datas = [
    #(1, 1, "02 38 56 54 37"),
    #(2, 2, "06 71 03 37 72"),
    #(3, 3, "06 08 07 22 04"),
    #(4, 3, "06 62 10 88 85"),
    #(5, 4, "02 47 28 49 94"),]
#cur.executemany ("insert into repertory (id_repertory, id_contact, phone) values (?, ?, ?)", datas)
#conn.commit()
#cur.close()
#conn.close()

#conn = sql.connect ("repTel.db")
#cur = conn.cursor()
#datas = [
    #(1, "Sophie", "Bertrand", "63 Rue Basse d'Ingré"),
    #(2, "Patricia", "Bertrand", "63 Rue Basse d'Ingré"),
    #(3, "Jean-Luc", "Bertrand", "63 Rue Basse d'Ingré"),
    #(4, "Thérèse", "Bourdeau", "10 Allée de la Sagerie"),]
#cur.executemany ("insert into contact (id_contact, name, last_name, address) values (?, ?, ?, ?)", datas)
#conn.commit()
#cur.close()
#conn.close()


app = Flask(__name__, template_folder ="templates")


@app.route('/')
def webpage():
    return render_template("webpage.html")

@app.route('/my_infos/')
def my_infos():
    return render_template('my_infos.html')

@app.route('/contacts/')
def view():
   con = sql.connect("repTel.db")
   con.row_factory = sql.Row

   cur = con.cursor()
   cur.execute("select distinct * from contact inner join repertory on repertory.id_contact=contact.id_contact order by id_contact asc")

   rows = cur.fetchall()
   return render_template("contacts.html", rows = rows)

@app.route('/addrec', methods = ['post', 'get'])
def addrec():
   msg = "msg"
   try:
      id_contact = request.form['id']
      name = request.form['name']
      last_name = request.form['last_name']
      address = request.form['address']
      phone = request.form['phone']

      with sql.connect("repTel.db") as con:
         cur = con.cursor()
         cur.execute("insert into contact (id, name,last_name,address) values (?,?,?)", [(id_contact, name, last_name, address)])
         cur.execute("insert into repertory (phone) values (?)", [(phone)])
         con.commit()
         msg = "Added contact with sucess"

   except:
      con.rollback()
      msg = "An unexpected error occured"

   finally:
      return render_template("result.html", msg = msg)

@app.route("/delrec", methods = ["post"])
def delrec():
   id = request.form["id"]
   with sql.connect("repTel.db") as con:
      try:
         cur = con.cursor()
         cur.execute("delete from repertory where id_contact = ?",id)
         cur.execute("delete from contact where id_contact = ?",id)
         msg = "Contact successfully deleted"

      except:
         msg = "An unexpected error occured"

      finally:
         return render_template("result.html", msg = msg)


if __name__ == '__main__':
   app.run(debug = True, port = 50000)
