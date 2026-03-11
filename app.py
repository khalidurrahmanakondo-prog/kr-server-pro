from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "KR Downloader Engine is Running! v2.0"

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    # yt-dlp শক্তিশালী কনফিগারেশন
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'referer': 'https://www.google.com/',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ভিডিওর সব তথ্য বের করা
            info = ydl.extract_info(video_url, download=False)
            
            # সরাসরি ভিডিও লিঙ্ক বা ফরম্যাট চেক করা
            video_link = info.get('url')
            if not video_link and 'formats' in info:
                video_link = info['formats'][-1].get('url')

            return jsonify({
                "status": "success",
                "title": info.get('title', 'KR_Video'),
                "url": video_link,
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration'),
                "source": info.get('extractor_key')
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
