from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('FIXER_API_KEY')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            from_currency = request.form['from_currency'].upper()

            url = f"http://data.fixer.io/api/latest?access_key={API_KEY}&symbols={from_currency},INR"
            response = requests.get(url)
            data = response.json()

            if data.get('success'):
                rates = data['rates']
                eur_to_from = rates.get(from_currency)
                eur_to_inr = rates.get('INR')

                if eur_to_from is None or eur_to_inr is None:
                    result = "Invalid currency code."
                else:
                    # Convert from 'from_currency' to INR using EUR as base
                    converted_amount = (amount / eur_to_from) * eur_to_inr
                    result = f"{amount} {from_currency} = {round(converted_amount, 2)} INR"
            else:
                result = "Error fetching exchange rate. Check your API key."
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
