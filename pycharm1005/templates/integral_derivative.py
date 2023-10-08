from flask import Flask,render_template,request,jsonify
import sympy as sp
import numpy as np

app =Flask(__name__)

@app.route('/calc')
def v():
    return render_template('1.html')

# def derivative(f,x,h=0.0001):
#     return (f(x+h)-f(x))/h

# def diff(v, *r):
#     arr=[]
#     for i in range(len(r)):
#         arr.append(sp.diff(v,r[i]))
#         print(r[i])
#     return arr

@app.route('/calc',methods=['POST'])
def calc_post():
    data=request.get_json()
    print(data)
    diff_variable = ['x_value','y_value','z_value']
    diff_x_y_z = ['x','y','z']
    exp=data['f']
    x,y,z = sp.symbols(' '.join(diff_x_y_z))
    for k, v in data.items():
        if k in diff_variable: #정수로 변환
            data[k] = int(v)
    print(data)

    #변수와 미분 횟수를 리스트로 묶어 관리
    variable_diff_counts = [(x, data['x_value']), (y, data['y_value']), (z, data['z_value'])]
    print(variable_diff_counts)
    result_derivative=[]
    #각 변수에 대해 주어진 횟수만큼 미분
    for variable, count in variable_diff_counts:
        internal_der=[]
        for _ in range(count):
            exp = sp.diff(exp, variable)
            internal_der.append(str(exp)) #여기 str로 감싸지 않으면 터짐(sympy 형태의 데이터)
        result_derivative.append(internal_der)
        print(result_derivative)
        return jsonify({'result':result_derivative})

@app.route("/integral",methods=['POST'])
def calc_intergral():
    data = request.get_json()
    print(data)
    x, y, z =sp.symbols('x y z')
    lower = int(data['lower'])
    upper = int(data['upper'])
    expression = sp.simplify(data['f'])
    y_ = int(data['y_'])
    z_ = int(data['z_'])
    f_sub= expression.subs({y:y_,z:z_}) #여기 y,z 값도 사용자에게 받을수 있도록 수정하세요
    result = sp.integrate(f_sub,(x, lower, upper)) # f(x,y,z)를 x로 적분하고 적분 구간은 사용자가 입력한 (lower, upper)이고
    # y값은 2이고 z이ㅡ 값은 3에서의 면적을 구함, 3중 적분
    print(result)
    return jsonify({'result':str(result)})


if __name__=='__main__':
    app.run(debug=True)