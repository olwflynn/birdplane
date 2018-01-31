from flask import Flask, render_template, request
from bird_plane import bird_plane_evaluate
import json, os
app = Flask(__name__)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def main():
    return render_template('signup.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
        # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate the received values
    if _name and _email and _password:
        return json.dumps(bird_plane_evaluate(_name))
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT,"templates/images/")
    print (target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print (file)
        filename = file.filename
        destination = "/".join([target,filename])
        print (destination)
        print (os.path.join(target,filename))
        file.save(destination)

        bird_or_plane = bird_plane_evaluate(destination)


    return render_template("complete.html", **locals())


if __name__ == "__main__":
    app.run()
