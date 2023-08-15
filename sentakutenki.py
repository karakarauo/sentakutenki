import hashlib
import hmac
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

CHANNEL_SECRET = os.environ.get("995f30a329c41e69eacdea82f4d841e9")

@app.route('/webhook', methods=['POST'])
def webhook():
    # 署名検証
    signature = request.headers['X-Line-Signature']
    body = request.data.decode('utf-8')
    hash = hmac.new(CHANNEL_SECRET.encode('utf-8'), body.encode('utf-8'), hashlib.sha256).digest()
    check_signature = base64.b64encode(hash).decode('utf-8')
    if signature != check_signature:
        abort(400)  # 署名が不一致の場合は400エラーを返す

    data = request.json
    # groupIdをログに表示
    if 'events' in data:
        for event in data['events']:
            if 'source' in event and 'groupId' in event['source']:
                print("Received groupId:", event['source']['groupId'])
    return jsonify(status=200)
