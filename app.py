from flask import Flask, jsonify, request
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

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
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f'https://www.youtube.com/watch?v={vid}',
                download=False
            )
            url = info['url']
            return jsonify({'url': url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
