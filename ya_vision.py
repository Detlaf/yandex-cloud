import os
import json
import base64
import requests

oauth = ''
catalog_id = 'b1gh30snh01dcojq8ub3'
image_path = 'img/keep_calm.png'
image_dir = 'img'
pdf_dir = 'pdf'

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

def main():
    iam_url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    vision_url = 'https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze'

    iam_token = get_iam_token(iam_url, oauth)
    res_file = open("results.txt", "w")
    pdf_res_file = open("results_pdf.txt", "w")

    for filename in os.listdir(image_dir):
        with open(os.path.join(image_dir, filename), "rb") as f:
            res_file.write(filename)
            res_file.write('\n')
            image_data = encode_file(f)
        text_from_image = extract_image(vision_url, iam_token, catalog_id, image_data)
        json_text = json.loads(text_from_image)
        for i in json_text['results'][0]['results'][0]['textDetection']['pages'][0]['blocks']:
            for j in i['lines']:
                for k in j['words']:
                    res_file.write(k['text'] + ' ')
            res_file.write('\n')

    for filename in os.listdir(pdf_dir):
        with open(os.path.join(pdf_dir, filename), "rb") as f:
            pdf_res_file.write(filename)
            pdf_res_file.write('\n---------------------\n')
            pdf_data = encode_file(f)
        text_from_pdf = extract_pdf(vision_url, iam_token, catalog_id, pdf_data)
        json_text = json.loads(text_from_pdf)
        for i in json_text['results'][0]['results'][0]['textDetection']['pages']:
            for j in i['blocks']:
                for k in j['lines']:
                    for z in k['words']:
                        pdf_res_file.write(z['text'] + ' ')
                pdf_res_file.write('\n')

if __name__ == '__main__':
    main()