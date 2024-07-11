from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from modules.issuer import IssuerModule
from modules.buyer import BuyerModule

app = Flask(__name__)

# Load the input data
df = pd.read_excel('Input.xlsx')

issuer_module = IssuerModule(df)
buyer_module = BuyerModule(df)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/issuer', methods=['GET', 'POST'])
def issuer_stats():
    if request.method == 'POST':
        issuer_name = request.form['issuer_name']
        top_n = int(request.form['top_n'])
        issuer_stats = issuer_module.get_issuer_stats(issuer_name, top_n)
        return render_template('issuer_stats.html', issuer_stats=issuer_stats, issuer_name=issuer_name)
    return render_template('issuer_stats.html')

@app.route('/buyer', methods=['GET', 'POST'])
def buyer_stats():
    if request.method == 'POST':
        buyer_name = request.form['buyer_name']
        buyer_stats = buyer_module.get_buyer_stats(buyer_name)
        return render_template('buyer_stats.html', buyer_stats=buyer_stats, buyer_name=buyer_name)
    return render_template('buyer_stats.html')

@app.route('/get_buyer_stats/<buyer_name>')
def get_buyer_stats(buyer_name):
    # Get buyer statistics using the BuyerModule
    buyer_stats = buyer_module.get_buyer_stats(buyer_name)
    return render_template('get_buyer_stats.html', buyer_name=buyer_name, buyer_stats=buyer_stats)


if __name__ == '__main__':
    app.run(debug=True)
