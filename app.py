from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/sign_up')
def index():
    image_url = 'C:\\Users\\Hadeel\\Downloads\\voteChain.jpg'
    return render_template('sign_up.html',image_url=image_url)

@app.route('/homepage',methods=['POST','GET'])
def homepage():
    image_url = 'C:\\Users\\Hadeel\\Downloads\\voteChain.jpg'
    image_url1 = 'https://e3.365dm.com/24/08/1600x900/skynews-2024-us-election-teaser_6671376.png?20240830164706'
    return render_template("homepage.html",image_url=image_url,image_url1=image_url1)

@app.route('/login')
def loginn():
    return render_template("login.html")

@app.route('/forgetPassword')
def forgetPassword():
    return render_template("forgetPassword.html")

@app.route('/reset_password')
def resetPassword():
    return render_template("reset_password.html",image_url="./voteChain.jpg")


@app.route("/voteChain.jpg")
def image():
    return render_template("voteChain.jpg")

if __name__ == '__main__':
    app.run(debug=True)
