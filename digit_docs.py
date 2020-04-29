import os
import argparse
import json
import ya_vision


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image-dir', required=True)
    parser.add_argument('--oauth-path', required=True)
    args = parser.parse_args()

    catalog_id = 'b1gh30snh01dcojq8ub3'
    iam_url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    vision_url = 'https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze'

    oauth = ya_vision.get_oauth(args.oauth_path)
    iam_token = ya_vision.get_iam_token(iam_url, oauth)
    res_file = open("results.txt", "w")

    for subdir, dirs, files in os.walk(args.image_dir):
        for filename in files:
            full_path = os.path.join(subdir, filename)
            res_file.write('-----------------\n' + filename + '\n--------------\n')
            with open(full_path, "rb") as f:
                image_data = ya_vision.encode_file(f)
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                extracted_text = ya_vision.extract_image(vision_url, iam_token, catalog_id, image_data)
            elif filename.endswith('.pdf'):
                extracted_text = ya_vision.extract_pdf(vision_url, iam_token, catalog_id, image_data)
            else:
                extracted_text = None
                print('Unsupported file extension! Must be JPEG, PNG or PDF!')
            if extracted_text is not None:
                print(filename)
                json_text = json.loads(extracted_text)
                results = json_text['results'][0]['results'][0]['textDetection']
                pages = results['pages']
                for page in pages:
                    for block in page['blocks']:
                        for line in block['lines']:
                            for word in line['words']:
                                res_file.write(word['text'] + ' ')
                        res_file.write('\n')
    res_file.close()

if __name__ == '__main__':
    main()