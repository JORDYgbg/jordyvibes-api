from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

INSTANCES = [
    'https://inv.nadeko.net',
    'https://invidious.nerdvpn.de',
    'https://invidious.privacyredirect.com',
    'https://yt.cdaut.de',
]

@app.route('/audio')
def audio():
    vid = request.args.get('v')
    if not vid:
        return jsonify({'error': 'falta v'}), 400
    
    for base in INSTANCES:
        try:
            r = requests.get(
                f'{base}/api/v1/videos/{vid}',
                params={'fields': 'adaptiveFormats,formatStreams'},
                timeout=8
            )
            if not r.ok:
                continue
            data = r.json()
            
            # Solo audio
            audio_formats = [f for f in data.get('adaptiveFormats', []) 
                           if f.get('type','').startswith('audio/')]
            audio_formats.sort(key=lambda x: x.get('bitrate', 0), reverse=True)
            
            if audio_formats:
                return jsonify({'url': audio_formats[0]['url']})
            
            # Fallback a formatStreams
            streams = data.get('formatStreams', [])
            if streams:
                return jsonify({'url': streams[-1]['url']})
                
        except Exception as e:
            print(f'{base} falló: {e}')
            continue
    
    return jsonify({'error': 'No se pudo obtener audio'}), 500

@app.route('/ping')
def ping():
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
