from flask import Flask, render_template, request

app = Flask('Nebula - Dashboard', template_folder='templates')


@app.route('/')
@app.route('/home')
def home():
    return render_template('/home.html')

@app.route('/submit', methods=['POST'])
def submit():
    return request.remote_addr

app.run()