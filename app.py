# app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import csv
from io import StringIO, BytesIO
import os

app = Flask(__name__)

# PostgreSQLデータベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# データベースモデル
class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reader_id = db.Column(db.String(100))
    department = db.Column(db.String(100))
    department_other = db.Column(db.String(100))
    doctor_year = db.Column(db.String(100))
    facility_year = db.Column(db.String(100))
    images_num = db.Column(db.String(100))
    position = db.Column(db.String(100))
    skill_1 = db.Column(db.String(100))
    skill_2 = db.Column(db.String(100))
    question_1 = db.Column(db.String(100))
    question_2 = db.Column(db.String(100))
    question_3 = db.Column(db.String(100))
    question_4 = db.Column(db.String(100))
    question_5 = db.Column(db.String(100))
    question_6 = db.Column(db.String(100))
    question_7 = db.Column(db.String(100))
    question_8 = db.Column(db.String(100))
    question_9 = db.Column(db.String(100))
    question_10 = db.Column(db.String(100))

# データベースの初期化
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/save-survey', methods=['POST'])
def save_survey():
    survey_data = request.json
    new_survey = Survey(reader_id=survey_data['reader_id'], 
                        department=survey_data['department'], 
                        department_other=survey_data['department_other'], 
                        doctor_year=survey_data['doctor_year'], 
                        facility_year=survey_data['facility_year'], 
                        images_num=survey_data['images_num'],
                        position=survey_data['position'],
                        skill_1=survey_data['skill_1'],
                        skill_2=survey_data['skill_2'],
                        question_1=survey_data['question_1'],
                        question_2=survey_data['question_2'],
                        question_3=survey_data['question_3'],
                        question_4=survey_data['question_4'],
                        question_5=survey_data['question_5'],
                        question_6=survey_data['question_6'],
                        question_7=survey_data['question_7'],
                        question_8=survey_data['question_8'],
                        question_9=survey_data['question_9'],
                        question_10=survey_data['question_10']
                        )
    db.session.add(new_survey)
    db.session.commit()
    
    return redirect(url_for('thank_you_page'))

@app.route('/export-csv', methods=['GET'])
def export_csv():
    results = Survey.query.all()
    surveys = [{'reader_id': r.reader_id,
                'department': r.department,
                'department_other': r.department_other,
                'doctor_year': r.doctor_year,
                'facility_year': r.facility_year,
                'images_num': r.images_num,
                'position': r.position,
                'skill_1': r.skill_1,
                'skill_2': r.skill_2,
                'question_1': r.question_1,
                'question_2': r.question_2,
                'question_3': r.question_3,
                'question_4': r.question_4,
                'question_5': r.question_5,
                'question_6': r.question_6,
                'question_7': r.question_7,
                'question_8': r.question_8,
                'question_9': r.question_9,
                'question_10': r.question_10
                } for r in results]

    # CSVファイルをメモリ内に生成
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['reader_id',
                'department',
                'department_other',
                'doctor_year',
                'facility_year',
                'images_num',
                'position',
                'skill_1',
                'skill_2',
                'question_1',
                'question_2',
                'question_3',
                'question_4',
                'question_5',
                'question_6',
                'question_7',
                'question_8',
                'question_9',
                'question_10'])  # ヘッダー行
    for survey in surveys:
        cw.writerow([survey['reader_id'],
                survey['department'],
                survey['department_other'],
                survey['doctor_year'],
                survey['facility_year'],
                survey['images_num'],
                survey['position'],
                survey['skill_1'],
                survey['skill_2'],
                survey['question_1'],
                survey['question_2'],
                survey['question_3'],
                survey['question_4'],
                survey['question_5'],
                survey['question_6'],
                survey['question_7'],
                survey['question_8'],
                survey['question_9'],
                survey['question_10']])
    output = si.getvalue()
    si.close()

    output_binary = output.encode()

    # CSVファイルをレスポンスとして返す
    return send_file(
        BytesIO(output_binary),
        mimetype='text/csv',
        as_attachment=True,
        download_name='survey_results.csv'
    )


# アンケート送信後の「ありがとう」ページ
@app.route('/thank-you')
def thank_you_page():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
