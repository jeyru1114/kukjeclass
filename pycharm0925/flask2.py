import json

from flask import Flask, render_template, request, jsonify
app =Flask(__name__)
from sympy import *

@app.route("/")
def hello():
    h= '홍길동'
    return render_template('sympy.html', h=h) # sympy.html

@app.route("/signup")
def signup():
    return render_template('signup.html')

def plus(first,second):
    return first + second

def minus(first,second):
    return first - second

def mul(first,second):
    return first * second

def div(first,second):
    return first / second

@app.route('/sympy', methods=['POST'])
def signupUser():
    # data= request.get_json()
    # print(data)
    # user= data['user'] # name = user 입력하는것은 이차방정식의 수식
    # result = solve(user) # sympy로 해를 푼다
    # solution = [pretty(sol) for sol in result]

    data2 = request.get_json()
    print(data2)
    first= int(data2['first'])
    second= int(data2['second'])
    op = data2['operator']
    print('op',op)
    list1 = op.split(" ")
    print(list1)
    result = 0
    operator_list=['+',"-",'*','/']
    function_list =[plus,minus,mul,div]
    zip_list = list(zip(operator_list,function_list))
    
    list_result=[]
    for i in list1:
        for o,f in zip_list:
            if i == o:
                list_result.append(f(first,second))
    print('ff',list_result)

    return jsonify({'strarus': 'ok', 'result': list_result}) #success callback 함수로 전달

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
