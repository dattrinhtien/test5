from flask import Flask, render_template, request, redirect
import json
from datetime import datetime
import os

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

    user = request.form.get('user') or request.args.get('user', '').strip().lower()
    selected_date = request.form.get('date') if request.method == 'POST' else request.args.get('date')

    if not selected_date:
        selected_date = datetime.now().strftime('%Y-%m-%d')

    if request.method == 'POST' and user:
        form_data = request.form.to_dict(flat=True)
        form_data.pop('date', None)
        form_data.pop('user', None)

        if user not in data:
            data[user] = {}

        data[user][selected_date] = form_data
        save_data(data)
        return redirect(f"/?user={user}&date={selected_date}")

    selected_data = data.get(user, {}).get(selected_date, {}) if user else {}
    user_data = data.get(user, {}) if user else {}

    return render_template(
        'index.html',
        user=user,
        date=selected_date,
        data=selected_data,
        all_data=user_data
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
