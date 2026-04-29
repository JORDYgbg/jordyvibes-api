from flask import Flask, jsonify, request
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIES = os.path.join(BASE_DIR, 'cookies.txt')

@app.route('/audio')
def audio():
    vid = request.args.get('v')
    if not vid:
        return jsonify({'error': 'falta v'}), 400
    try:
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'cookiefile': COOKIES,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                'Accept-Language': 'es-EC,es;q=0.9',
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['web'],
                }
            },
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f'https://www.youtube.com/watch?v={vid}',
                download=False
            )
            return jsonify({'url': info['url'], 'duration': info.get('duration', 0)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ping')
def ping():
    exists = os.path.exists(COOKIES)
    return jsonify({'cookies_found': exists})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
