from flask import Flask, request, render_template
from scraper import fetch_case_details
from models import log_query
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    # Static list of case types for dropdown
    case_types = [
        "CR", "FIR", "Civil", "Criminal", "Family",
        "Consumer", "Motor Accident", "Rent", "Labor","	SC - SESSIONS CASES"
    ]
    return render_template('index.html', case_types=case_types)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/court-rules')
def court_rules():
    return render_template("court_rules.html")


@app.route('/result', methods=['POST'])
def result():
    selected_type = request.form['case_type'].strip()
    case_number = request.form['case_number'].strip()
    filing_year = request.form['year'].strip()

    case_info, orders = fetch_case_details(selected_type, case_number, filing_year)

    result_text = case_info.get("Case Title", "No matching case found") if "Error" not in case_info else case_info["Error"]
    log_query(selected_type, case_number, filing_year, result_text)

    return render_template("result.html", case=case_info, orders=orders)
@app.route('/logs')
def view_logs():
    logs = []
    try:
        with sqlite3.connect('db.sqlite3', timeout=10) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM logs ORDER BY id ASC")
            logs = c.fetchall()
    except sqlite3.OperationalError as e:
        print(f"[ERROR] Failed to fetch logs: {e}")
    return render_template('logs.html', logs=logs)


if __name__ == '__main__':
    app.run(debug=True)
