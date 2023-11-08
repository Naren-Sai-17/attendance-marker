

from deepface import DeepFace
import numpy as np 
import os
import csv
import shutil
from flask import Flask,request, redirect, render_template, send_file
from werkzeug.utils import secure_filename
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kecret sey'    
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

with open('static/encoding_dict.json', 'r') as json_file:
    encoding_dict = json.load(json_file)

def findCosineDistance(source_representation, test_representation):
    a = np.matmul(np.transpose(source_representation), test_representation)
    b = np.sum(np.multiply(source_representation, source_representation))
    c = np.sum(np.multiply(test_representation, test_representation))
    return 1 - (a / (np.sqrt(b) * np.sqrt(c)))

def get_roll_number(embedding_obj):
    unknown_encoding = np.array(embedding_obj['embedding'])
    unknown_roll_no = '1001'
    mx_similarity = findCosineDistance(unknown_encoding, np.array(encoding_dict['1001'][0]))
    for roll_no,encodings in encoding_dict.items():
        for encoding in encodings:
            similarity = findCosineDistance(unknown_encoding, np.squeeze(np.array(encoding)))
            if similarity < mx_similarity:
                mx_similarity = similarity
                unknown_roll_no = roll_no
    return unknown_roll_no

def get_roll_numbers(photo_path):
    roll_numbers = []
    embedding_objs = DeepFace.represent(img_path = photo_path, model_name='ArcFace',detector_backend = 'retinaface',enforce_detection=False)
    for embedding_obj in embedding_objs:
        roll_numbers.append(get_roll_number(embedding_obj))
    return roll_numbers

def update_csv(date, roll_numbers):
    dir = f'sheets/{date}.csv'
    if not os.path.exists(dir):
        shutil.copyfile('sheets/reference.csv', dir)
    sheet = pd.read_csv(dir,dtype = str)
    for roll_number in roll_numbers:
        rno = '22000' + roll_number
        sheet.loc[sheet['Roll number'] == (rno) , 'Status' ] = 'Present'
    sheet.to_csv(f'sheets/{date}.csv',index=False)

def update_pdf(date):
    sheet_path = f'sheets/{date}.csv'
    pdf_path = f'pdfs/{date}.pdf'
    df = pd.read_csv(sheet_path)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    data = [df.columns.tolist()] + df.values.tolist()
    table = Table(data)
    list1=[('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)]
    c = 0
    for row in df.iterrows():
        c+=1
        status=row[1][-1]
        if status=='Absent':
            list1.append((('BACKGROUND', (2,c), (2,c), colors.red)))
    style = TableStyle(list1)
    table.setStyle(style)
    elements = [table]
    doc.build(elements)

def update_tot(date,roll_numbers):
    dict1 = {}

    with open('sheets/total_attendance.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            roll_number = row['Roll number']
            dict1[roll_number] = int(row['Attendance'])
    dir = f'sheets/{date}.csv'
    dir2 = 'sheets/total_attendance.csv'
    if not os.path.exists(dir):
        shutil.copyfile('sheets/reference.csv', dir)
    sheet = pd.read_csv(dir,dtype = str)
    sheet2 = pd.read_csv(dir2,dtype = str)
    print(roll_numbers)
    for roll_number in roll_numbers:
        # print(roll_number)
        rno = '22000' + roll_number
        print(rno)
        if not sheet.loc[sheet['Roll number'] == (rno) , 'Status' ].iloc[0] == 'Present':
            dict1[rno]+=1
    for row in sheet2.iterrows():
        row[1]['Attendance']=dict1[row[1]['Roll number']]
    sheet2.to_csv(dir2, index=False)
    
    # print(roll_numbers)
    print(dict1)
            
            
    # sheet.to_csv(f'sheets/{date}.csv',index=False)
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['GET', 'POST'])
def process_image():
    print(request.files)
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect("/")
        file = request.files['file']
        if file.filename == '':
            return redirect("/")
        if not allowed_file(file.filename):
            return redirect("/")
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads/',filename)
        file.save(filepath)
        date = request.form.get('date')
        roll_numbers = get_roll_numbers(filepath)
        # print(list(set(roll_numbers)))
        update_tot(date,list(set(roll_numbers)))
        update_csv(date,roll_numbers)
        update_pdf(date) 
        return redirect("/")
@app.route('/download-pdf', methods=['GET'])

def download_pdf():
    file_path = "pdfs/" + str(request.args.get('date')) + ".pdf"
    return send_file(
        file_path,
        as_attachment = True,
        download_name = file_path,
        mimetype='text/pdf'
    )

@app.route('/download-xls', methods=['GET'])
def download_xls():
    file_path = "sheets/" + str(request.args.get('date')) + ".csv"
    return send_file(
        file_path,
        as_attachment = True,
        download_name = file_path + ".csv",
        mimetype='text/csv'
    )

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
