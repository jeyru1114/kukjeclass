from flask import Flask, render_template, request, jsonify
import mysql.connector

app= Flask(__name__)

mysql_config={
    'user': 'root',
    'password':'1234',
    'host':'localhost',
    'database':'flaskdb'
}
conn= mysql.connector.connect(**mysql_config)
cursor= conn.cursor()
def get_grade(avg):
    if avg>=90:
        return '수'
    elif avg>=80:
        return '우'
    elif avg >= 70:
        return '미'
    elif avg >= 60:
        return '양'
    else: return '가'
@app.route("/")
def index():
    print("여기")
    cursor.execute("select * from flask_tbl")
    data= cursor.fetchall()
    print(data)
    list_of_dict = []
    for i in data:
        obj = {}
        fno, m, e, k, t, a, g = i
        obj['fno'] = fno
        obj['math'] = m
        obj['eng'] = e
        obj['korea'] = k
        obj['total'] = t
        obj['avg'] = a
        obj['grade'] = g
        list_of_dict.append(obj)
    print('result:', list_of_dict)
    return render_template('index.html', data= list_of_dict)

@app.route('/create' ,methods=['POST'])
def index_create():
    data= request.get_json()
    print(data)
    math= int(data['math'])
    eng= int(data['eng'])
    korea= int(data['korea'])
    total= math+ eng+ korea
    avg= total/3.0
    grade= get_grade(avg)
    print(math, eng, korea, total, avg, grade)
    data= (math, eng, korea, total, avg, grade)
    cursor.execute('insert into flask_tbl ( math, eng, korea, total, avg, grade) values(%s, %s, %s, %s, %s, %s)', (data))
    conn.commit()
    cursor.execute("select * from flask_tbl")
    result_db = cursor.fetchall()
    print(result_db)
    list_of_dict = []
    for i in result_db:
        obj = {}
        fno ,m ,e ,k, t, a, g = i
        obj['fno'] = fno
        obj['math'] = m
        obj['eng'] = e
        obj['korea'] = k
        obj['total'] = t
        obj['avg'] = a
        obj['grade'] = g
        list_of_dict.append(obj)
    print('result:',list_of_dict)
    return jsonify({'result':list_of_dict}),200

if __name__=='__main__':
    app.run(debug=True)