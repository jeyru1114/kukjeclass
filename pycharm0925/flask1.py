import json

from flask import Flask, render_template, request, jsonify
app =Flask(__name__)

@app.route("/")
def hello():
    h= '홍길동'
    return render_template('index.html', h=h)

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route('/signupUser', methods=['POST'])
def signupUser():
    data= request.get_json()
    print(data)
    user= data['user']
    password= data['pw']
    print(user, password)
    return jsonify({'strarus': 'ok', 'user': user, 'pass': password}) #success callback 함수로 전달

@app.route('/c')
def chajung():
    return render_template('chaejungho.html')

@app.route('/a', methods=['POST'])
def chajung11():
    mat= request.form['math']
    print(mat)
    return render_template('index.html')


if __name__== '__main__':
    app.run()
