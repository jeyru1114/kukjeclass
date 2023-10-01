import json
from  sympy import *
from flask import Flask, render_template, request, jsonify
app =Flask(__name__)
from sympy.printing.pretty.pretty import pretty
import numpy as np
import matplotlib.pyplot as plt
import base64

def save_equation_plot(equation_expr):
    print('save: ' ,equation_expr)
    # 변수 및 수식을 정의합니다.
    x = symbols('x')
    x_values = np.linspace(-10, 10, 400)  # x값 범위 설정
    y_values = [equation_expr.evalf(subs={x: x_val}) for x_val in x_values]
    derivative_values = [diff(equation_expr, x).evalf(subs={x: x_val}) for x_val in x_values]

    plt.plot(x_values, y_values, label='Equation')  # label을 설정하여 레이블을 지정
    plt.plot(x_values, derivative_values, label='Derivative')  # 미분 그래프 추가

    img_path = 'static/latex_derivative_plot.png'  # 이미지 파일 경로 (static 폴더에 저장)
    plt.savefig(img_path, format='png')
    plt.close()  # 그래프 창 닫기

    return img_path  # 이미지 파일 경로 반환

@app.route("/")
def hello():
    return render_template('sympy2.html')

@app.route('/sympy2', methods=['POST'])
def jquerytest():
    data = request.get_json()
    print('data:',data)
    f = data['data']
    derived_fn = diff(f)
    save_equation_plot(derived_fn)
    derived_fn = f"\\({latex(derived_fn)}\\)"
    # pretty1 = pretty(derived_fn)
    print(derived_fn)

    return jsonify({'strarus': 'ok', 'result':derived_fn}) #success callback 함수로 전달

@app.route('/plot', methods=['POST'])
def plot_equation():

    img_tag = 'static/latex_derivative_plot.png'  # 이미지 파일 경로 (static 폴더에 저장)
    # 이미지를 Base64로 인코딩
    with open(img_tag, 'rb') as img_file:
        img_data = base64.b64encode(img_file.read()).decode('utf-8')
    return jsonify({'image': img_data})

if __name__== '__main__':
    app.run()
