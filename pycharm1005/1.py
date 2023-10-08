from flask import Flask,render_template,request,jsonify
import sympy as sp
import mysql.connector

app =Flask(__name__)

mysql_config={
    'user':'root',
    'password':'1234',
    'host':'localhost',
    'database':'flaskdb'
}
conn= mysql.connector.connect(**mysql_config)
cursor= conn.cursor()
@app.route('/a' ,methods=['GET','POST'])
def v():
    if request.method=='GET': #get 방식(url) 으로 4.html 열기
        return render_template('4.html')
    else:#post 방식(button  누루면  ajax 호출되어 ) 으로 전송시 처리함
        data = request.get_json()
        print(data)
        f_raw= data['f']
        x = sp.symbols('x')
        f = sp.lambdify(x,f_raw) # lambdaify는 람다식으로 변경해주는것
        f_der = sp.diff(sp.simplify(f_raw)) # sympy형태로 변경하는것
        print(f_der)
        lower = int(data['lower'])
        f_der_evaluate = sp.lambdify(x,f_der)(lower) 
        upper = int(data['upper'])
        f_integrate = sp.integrate(f_raw,x)
        f_integrate_eval = sp.integrate(f(x), (x, lower, upper))  # f(x)를 x 로 적분하고 적분 구간은 2,5까지 면적을 구함 ㄴㄴ
        print(f_integrate_eval)
        cursor.execute('insert into der_tbl (e, d,i,d_value,i_value) ' +
                       ' values(%s,%s,%s,%s, %s)' ,(  f_raw  ,   str(f_der)  ,str(f_integrate) , f_der_evaluate,  str(int(f_integrate_eval)) ))
        conn.commit()
        return jsonify({'result': str(f_integrate_eval)})

if __name__  =='__main__':
    app.run(debug=True)