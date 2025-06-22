from flask import Flask, render_template, request
import pandas as pd
import os
from scheduler import schedule_day_offs
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    assignments = None
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith(('.csv', '.xlsx')):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Read file
            if filename.endswith('.csv'):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)

            assignments = schedule_day_offs(df)
            os.remove(filepath)

    return render_template('index.html', assignments=assignments)

if __name__ == '__main__':
    app.run(debug=True)
