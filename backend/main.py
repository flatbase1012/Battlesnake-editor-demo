from flask import Flask, request, jsonify
import os
import uuid

app = Flask(__name__)

# コード保存用ディレクトリ（存在しなければ作成）
SAVE_DIR = 'saved_codes'
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route('/api/save', methods=['POST'])
def save_code():
    data = request.get_json()
    if not data or 'code' not in data:
        return jsonify({"status": "error", "message": "コードが送信されていません"}), 400

    code = data['code']
    # 一意なファイル名を生成してコードを保存（例：拡張子 .py）
    file_id = str(uuid.uuid4())
    file_path = os.path.join(SAVE_DIR, f"{file_id}.py")
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
    except Exception as e:
        return jsonify({"status": "error", "message": f"保存に失敗しました: {str(e)}"}), 500

    print("Received and saved code to", file_path)
    return jsonify({"status": "success", "message": "コードが保存されました", "file_id": file_id}), 200

if __name__ == '__main__':
    # 外部からアクセスできるように host を 0.0.0.0 に指定
    app.run(host='0.0.0.0', port=8080)

