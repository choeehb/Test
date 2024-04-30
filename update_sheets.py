import os
import subprocess
import requests
import json

def get_changed_files():
    # 마지막 커밋 이후 변경된 파일 목록을 가져옴
    changed_files = subprocess.check_output(['git', 'diff', '--name-only', 'HEAD^', 'HEAD']).decode().split()
    # 'sheets' 폴더 내의 .csv 파일만 필터링
    return [f for f in changed_files if f.startswith('sheets/') and f.endswith('.csv')]

def main():
    changed_csv_files = get_changed_files()
    payload = {}

    for csv_file in changed_csv_files:
        with open(csv_file, 'r', encoding='utf-8') as file:
            content = file.read()
            filename_without_extension = os.path.splitext(os.path.basename(csv_file))[0]
            payload[filename_without_extension] = content

    # Apps Script 웹앱 URL
    url = os.environ.get('APPS_SCRIPT_URL')

    # POST 요청으로 데이터 전송
    response = requests.post(url, json=payload)
    print(response.text)

if __name__ == '__main__':
    main()
