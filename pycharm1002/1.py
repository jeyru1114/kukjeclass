from flask import Flask,render_template,request,jsonify
import mysql.connector
import numpy as np

cnt = 0
app =Flask(__name__)

def derivative(f,x,h=0.0001):
    return (f(x+h)-f(x))/h

@app.route('/a',methods=['GET','POST'])
def v():
    if request.method == 'GET' : #get 방식으로 4.html 열기
        return render_template('4.html',v ='홍길동')
        #홍길동 출력하려면 html파일에서 {{}}를 이용하여 출력
    else: #post 방식(button 누르면 ajax 호출되어)으로 전송시 처리함
        data = request.get_json()
        dict1 = {}
        key =""
        value =""
        for i,j in data.items():
            key+= i
            value+= j
        dict1[key]=value
        return jsonify(dict1)

@app.route('/q', methods=['POST'])
def q():
    data = request.get_json()
    print(data)
    # 객체로 전달되므로 data["fn"]을 하면 배열이고 배열이므로 하나씩 꺼내어 lambda 문자열 추가
    lambda_merge = map(lambda i: 'lambda x:' + i, data['fn'])
    sum_=0
    sum_d=0
    for i in lambda_merge:
        sum_+=eval(i)(data['arg']) #arg: 17, 전달된 data['arg'] 하면 17을 얻을수 있고 함수에 전달함
        sum_d += sum(derivative(eval(i),np.arange(-10,10,0.01)))
    return jsonify({'total':sum_ , 'derivative':sum_d})
        

@app.route('/create', methods=['POST'])
def r():
    pass

@app.route('/k')
def r1():
    return render_template('kwon.html')

@app.route('/p')
def pp():
    return render_template('pixabay.html')

if __name__ == '__main__':
    app.run(debug=True)