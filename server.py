from flask import Flask, render_template, request, redirect
from user import User
app = Flask(__name__)

@app.route("/")
def index():
    users = User.get_all()
    print(users)
    return render_template("index.html", all_users = users)

@app.route('/add_user', methods=["POST"])
def add_user():
    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"]
    }
    user_id = User.save(data)
    return redirect(f'/show_user/{user_id}')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/update/<int:id>')
def edit(id):
    data = {"id":id}
    return render_template("update.html",user=User.get_one(data))

@app.route('/show_user/<int:id>')
def show_user(id):
    data = {"id":id}
    return render_template("show_user.html",user=User.get_one(data))

@app.route('/update', methods=['POST'])
def update():
    updated_user = request.form["id"]
    User.update(request.form)
    return redirect(f'/show_user/{updated_user}')

@app.route('/remove/<int:id>')
def remove(id):
    data ={'id':id}
    User.remove(data)
    return redirect('/') 

if __name__ == "__main__":
    app.run(debug=True)