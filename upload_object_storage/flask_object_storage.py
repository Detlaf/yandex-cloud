import os
import boto3
from func_object_storage import list_files, upload_file
from flask import Flask, render_template, request, redirect, send_file

BUCKET = ''
UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)


@app.route('/')
def entry_point():
    return 'Interacting with Yandex Object Storage'

@app.route("/storage")
def storage():
    contents = list_files(s3, BUCKET)
    return render_template('storage.html', contents=contents)

@app.route("/upload", methods=['POST'])
def upload():
    f = request.files['file']
    f.save(os.path.join(UPLOAD_FOLDER, f.filename))
    upload_file(s3, f"uploads/{f.filename}", BUCKET)

    return redirect("/storage")

if __name__ == '__main__':
    app.run(debug=True)