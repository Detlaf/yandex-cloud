import base64
import json
import requests

def get_oauth(oauth_path):
    f = open(oauth_path, "r")
    oauth = f.read()
    return oauth

def get_iam_token(iam_url, oauth):
    response = requests.post(url=iam_url, json={"yandexPassportOauthToken": oauth})
    json_data = json.loads(response.text)
    if json_data is not None and 'iamToken' in json_data:
        return json_data['iamToken']
    return None

def encode_file(file):
  file_content = file.read()
  return base64.b64encode(file_content).decode('utf-8')

def extract_image(vision_url, iam_token, catalog_id, image_data):
    response = requests.post(vision_url, headers={'Authorization': 'Bearer ' + iam_token}, json={
        'folderId': catalog_id,
        'analyzeSpecs': [
            {
                'content': image_data,
                'features': [
                    {
                        'type': 'TEXT_DETECTION',
                        'textDetectionConfig': {'languageCodes': ['en', 'ru']}
                    }
                ],
            }
        ]})
    return response.text

def extract_pdf(vision_url, iam_token, catalog_id, pdf_data):
    response = requests.post(vision_url, headers={'Authorization': 'Bearer ' + iam_token}, json={
        'folderId': catalog_id,
        'analyzeSpecs': [
            {
                'content': pdf_data,
                'mime_type': 'application/pdf',
                'features': [
                    {
                        'type': 'TEXT_DETECTION',
                        'textDetectionConfig': {'languageCodes': ['en', 'ru']}
                    }
                ],
            }
        ]})
    return response.text
