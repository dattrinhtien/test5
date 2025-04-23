from flask import Flask, render_template, request, redirect
import json
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = load_data()
    selected_date = request.form.get('date') if request.method == 'POST' else request.args.get('date')
    if not selected_date:
        selected_date = datetime.now().strftime('%Y-%m-%d')

    if request.method == 'POST':
        form_data = request.form.to_dict(flat=True)
        form_data.pop('date', None)
        data[selected_date] = form_data
        save_data(data)
        return redirect("/")

    selected_data = data.get(selected_date, {})
    return render_template('index.html', date=selected_date, data=selected_data, all_data=data)

if __name__ == '__main__':
    import os
app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

