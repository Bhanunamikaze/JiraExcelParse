from flask import Flask, render_template, request
import requests
import openpyxl
from bs4 import BeautifulSoup


app = Flask(__name__)

JIRA_URL = 'https://your-jira-instance.atlassian.net'
JIRA_USERNAME = 'your-jira-username'
JIRA_PASSWORD = 'your-jira-password'
EXCEL_FILE = 'file.xlsx'

@app.route('/')
def index():
    data = read_excel_file()
    return render_template('index.html', options=data)

@app.route('/create-ticket', methods=['POST'])
def create_ticket():
    title = request.form['title']
    description = request.form['description']

    table = request.form['table']
     #   if is_table(description):
      #   description = convert_text_to_table(description)
    label = request.form['label']
    remediation = request.form['remediation']
    reference = request.form['reference']

    issue_data = {
        'fields': {
            'project': {
                'key': 'YOUR_PROJECT_KEY'
            },
            'summary': title,
            'description': description,
            'labels': [label],
            'issuetype': {
                'name': 'Task'
            },
            'customfield_10000': remediation,
            'customfield_10001': reference,
        }
    }
    print(f"Description: {description}")
    print(f"table: {table}")

    response = requests.post(
        f'{JIRA_URL}/rest/api/3/issue',
        json=issue_data,
        auth=(JIRA_USERNAME, JIRA_PASSWORD)
    )

    if response.status_code == 201:
        return 'Ticket created successfully!'
    else:
        return 'An error occurred while creating the ticket.'

def is_table(content):
    soup = BeautifulSoup(content, 'html.parser')
    return soup.find('table') is not None

def convert_text_to_table(text):
    rows = text.split('\n')
    table_html = "<table>"
    for row in rows:
        table_html += "<tr>"
        columns = row.split('\t')
        for column in columns:
            table_html += f"<td>{column}</td>"
        table_html += "</tr>"
    table_html += "</table>"
    return table_html

def read_excel_file():
    workbook = openpyxl.load_workbook(EXCEL_FILE)
    sheet = workbook.active
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        data.append({
            'title': row[0],
            'description': row[1],
            'remediation': row[2],
            'reference': row[3]
        })
    return data

if __name__ == '__main__':
    app.run()
