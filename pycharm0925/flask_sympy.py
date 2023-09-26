# app.py

from flask import Flask, render_template, request, jsonify
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
from sympy import  *
import  numpy as np
import base64
import  itertools


app = Flask(__name__)

def remove_zero_values(lst):
    non_zero_results=[]
    # Filter out dictionaries with non-zero results
    for dict1 in lst:
        non_zero_results.append([{key:value} for key, value in dict1.items() if value != 0])
    return non_zero_results

def derivative_partial(f, variables):
    list_partial = []
    print('deri:', f, 'v', variables, 'ff:', variables.split(" "))
    variables_list = variables.split(" ")


    # Generate all possible combinations
    for i in range(1, len(variables_list) + 1):
        combinations = itertools.combinations(variables_list, i)
        for combo in combinations:
            # Calculate the partial derivative for the current combination
            partial_derivative = f
            for var in combo:
                partial_derivative = diff(partial_derivative, var)
            list_partial.append({','.join(combo):partial_derivative})
    # Remove entries with zero values
    filtered_list = remove_zero_values(list_partial)
    merged_dict = {}

    try:
        # Merge dictionaries into one
        for item in filtered_list:
            for sub_item in item:
                #print(sub_item)
                merged_dict.update(sub_item)
    except ValueError:
        print('ValueError 발생: 오류')

    return merged_dict

def save_equation_plot(equation_expr,variable):
    filtered_dict= derivative_partial(equation_expr, variable)
    x = sp.symbols('x')
    for k, v in filtered_dict.items():

        x_values = np.linspace(-10, 10, 4)  # x값 범위 설정
        y_values = v*x_values
        print(y_values)
    # # 변수 및 수식을 정의합니다.
    # x = sp.symbols('x')
    # x_values = np.linspace(-10, 10, 400)  # x값 범위 설정
    # y_values = [equation_expr.evalf(subs={x: x_val}) for x_val in x_values]
    # derivative_values = [diff(equation_expr, x).evalf(subs={x: x_val}) for x_val in x_values]
    #
    # plt.plot(x_values, y_values, label='Equation')  # label을 설정하여 레이블을 지정
    # plt.plot(x_values, derivative_values, label='Derivative')  # 미분 그래프 추가
    #
    # img_path = 'static/latex_derivative_plot.png'  # 이미지 파일 경로 (static 폴더에 저장)
    # plt.savefig(img_path, format='png')
    # plt.close()  # 그래프 창 닫기
    #
    # return img_path  # 이미지 파일 경로 반환

@app.route('/')
def index():
    return render_template('index6.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data['expression']
    variable = data['variable']
    print(variable, expression)
    # Convert the expression and variable to SymPy symbols
    x = sp.Symbol(variable)
    f = sp.sympify(expression)
    #
    # # Calculate the partial derivative
    df_dx = diff(f, x)

    save_equation_plot(expression,variable)

    return jsonify({'result_dir': df_dx, 'result_org': expression})
@app.route('/plot', methods=['POST'])
def plot_equation():

    img_tag = 'static/latex_derivative_plot.png'  # 이미지 파일 경로 (static 폴더에 저장)
    # 이미지를 Base64로 인코딩
    with open(img_tag, 'rb') as img_file:
        img_data = base64.b64encode(img_file.read()).decode('utf-8')
    return jsonify({'image': img_data})
if __name__ == '__main__':
    app.run(debug=True)
