import os
import json
import base64
import requests

oauth = ''
catalog_id = 'b1gh30snh01dcojq8ub3'
image_path = 'img/keep_calm.png'
image_dir = 'img'

def get_iam_token(iam_url, oauth):
    response = requests.post(url=iam_url, json={"yandexPassportOauthToken": oauth})
    json_data = json.loads(response.text)
    if json_data is not None and 'iamToken' in json_data:
        return json_data['iamToken']
    return None

def encode_file(file):
  file_content = file.read()
  return base64.b64encode(file_content).decode('utf-8')

def request_vision(vision_url, iam_token, catalog_id, image_data):
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

def main():
    iam_url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    vision_url = 'https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze'

    iam_token = get_iam_token(iam_url, oauth)
    res_file = open("results.txt", "w")

    for filename in os.listdir(image_dir):
        with open(os.path.join(image_dir, filename), "rb") as f:
            res_file.write(filename)
            res_file.write('\n')
            image_data = encode_file(f)
        text_from_image = request_vision(vision_url, iam_token, catalog_id, image_data)
        json_text = json.loads(text_from_image)
        for i in json_text['results'][0]['results'][0]['textDetection']['pages'][0]['blocks']:
            for j in i['lines']:
                for k in j['words']:
                    res_file.write(k['text'])
                    res_file.write('\n')

if __name__ == '__main__':
    main()