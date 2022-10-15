from flask import Flask,render_template,request,redirect

app=Flask(__name__)

@app.route('/login')
def login():
    return  render_template('home.html')

@app.route('/signup')
def home():
    return render_template('signup.html')

@app.route('/submission')
def submission():
    return render_template('submission.html')

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)