import json
import os
import base64
import webview
from pathlib import Path

class Api:
    def __init__(self):
        self.data_file = 'data/tokoh_sejarah.json'
        self.image_folder = 'data/images'
        self.ensure_directories()
        self.load_data()

    def ensure_directories(self):
        Path('data').mkdir(exist_ok=True)
        Path(self.image_folder).mkdir(exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def load_data(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    def save_data(self, data):
        try:
            if 'gambar' in data and data['gambar'].startswith('data:image'):
                img_format = data['gambar'].split(';')[0].split('/')[1]
                img_data = base64.b64decode(data['gambar'].split(',')[1])
                
                img_filename = f"{data['nama'].lower().replace(' ', '_')}_{data['tahunLahir']}.{img_format}"
                img_path = os.path.join(self.image_folder, img_filename)
                
                with open(img_path, 'wb') as f:
                    f.write(img_data)
                
                data['gambar'] = f'images/{img_filename}'

            current_data = self.load_data()
            current_data.append(data)

            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(current_data, f, indent=2, ensure_ascii=False)
            
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def delete_data(self, index):
        try:
            data = self.load_data()
            if 'gambar' in data[index] and data[index]['gambar'].startswith('images/'):
                img_path = os.path.join('data', data[index]['gambar'])
                if os.path.exists(img_path):
                    os.remove(img_path)
            data.pop(index)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

def main():
    api = Api()
    window = webview.create_window(
        'Sistem Admin - Tokoh Sejarah',
        'admin/index.html',
        js_api=api,
        width=1200,
        height=800
    )
    webview.start()

if __name__ == '__main__':
    main() 