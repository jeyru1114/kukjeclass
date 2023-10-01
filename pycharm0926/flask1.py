import json

from flask import Flask, render_template, request, jsonify
app =Flask(__name__)

@app.route("/")
def hello():
    return render_template('sympy.html')

@app.route('/sympy', methods=['POST'])
def jquerytest():
    data = request.get_json()
    first = data['first']
    second = data['second']
    result_list = [first,second]
    print(result_list)
    love = data['love_be']['love']
    believe = data['love_be']['believe']
    print(love,believe)

    print(data)
    return jsonify({'strarus': 'ok', 'result':result_list,'list':[love,believe]}) #success callback 함수로 전달


if __name__== '__main__':
    app.run()
