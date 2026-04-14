import time
import requests
import urllib3
import SpecialFriend_pb2
from flask import Flask, render_template_string, jsonify, request
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# --- Backend Logic ---
urllib3.disable_warnings()
GUEST_UID = "4295035549"
GUEST_PASSWORD = "A_PXHWR__1WKSG"
AeSkEy = b'Yg&tc%DEuh6%Zc^8'
AeSiV  = b'6oyZDr22E3ychjM%'
BASE_URL = "https://clientbp.ggwhitehawk.com"

def enc(d):
    return AES.new(AeSkEy, AES.MODE_CBC, AeSiV).encrypt(pad(d, 16))

def dec(d):
    try: return unpad(AES.new(AeSkEy, AES.MODE_CBC, AeSiV).decrypt(d), 16)
    except: return d

def build_uid_protobuf(uid):
    def to_varint(n):
        res = bytearray()
        while n >= 0x80:
            res.append((n & 0x7f) | 0x80)
            n >>= 7
        res.append(n)
        return bytes(res)
    return enc(b"\x08" + to_varint(int(uid)))

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CKR UNKNOWN | PRO</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <style>
        body {
            background: #05070a;
            font-family: 'Inter', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            overflow: hidden;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(30px) saturate(200%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 40px;
            width: 340px;
            padding: 30px;
            box-shadow: 0 30px 60px rgba(0,0,0,0.8);
        }
        .input-field {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 18px;
            color: white;
            text-align: center;
            font-weight: 700;
            transition: 0.3s;
        }
        .input-field:focus {
            border-color: #0ea5e9;
            background: rgba(255, 255, 255, 0.08);
            outline: none;
        }
        .btn-ios {
            background: #ffffff;
            color: #000;
            border-radius: 18px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
        }
        .btn-ios:active { transform: scale(0.94); opacity: 0.8; }
        
        .terminal {
            background: rgba(0, 0, 0, 0.5);
            border-radius: 20px;
            font-family: 'JetBrains Mono', monospace;
            display: none; /* Initially hidden */
            animation: fadeIn 0.5s ease forwards;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .data-label { color: rgba(255,255,255,0.5); font-weight: 600; font-size: 11px; }
        .data-value { color: #ffffff; font-weight: 900; font-size: 14px; }
    </style>
</head>
<body>
    <div class="glass-card">
        <div class="text-center mb-8">
            <h1 class="text-2xl font-black tracking-tighter text-white">CKR <span class="text-sky-500">UNKNOWN</span></h1>
            <p class="text-[9px] text-gray-500 font-bold uppercase tracking-[3px] mt-1">Duo Extractor</p>
        </div>

        <div class="space-y-4">
            <input type="text" id="uid" placeholder="PLAYER UID" class="input-field w-full py-4 text-lg">
            <button onclick="fetchData()" id="btn" class="btn-ios w-full py-4 text-xs">View Details</button>
        </div>

        <div id="outputContainer" class="terminal mt-6 p-5 border border-white/5">
            <div id="loader" class="text-center py-2 text-sky-400 font-bold text-[10px] animate-pulse">EXTRACTING...</div>
            <div id="result" class="hidden space-y-3">
                </div>
        </div>

        <div class="mt-8 text-center">
            <p class="text-[10px] text-gray-600 font-bold">
            </p>
        </div>
    </div>

    <script>
        async function fetchData() {
            const uid = document.getElementById('uid').value;
            const container = document.getElementById('outputContainer');
            const resultBox = document.getElementById('result');
            const loader = document.getElementById('loader');

            if(!uid) return;

            // UI Logic: Show Terminal
            container.style.display = 'block';
            resultBox.classList.add('hidden');
            loader.classList.remove('hidden');

            try {
                const response = await fetch('/get_data', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({uid: uid})
                });
                const res = await response.json();

                loader.classList.add('hidden');
                resultBox.classList.remove('hidden');

                if(res.status === 'success') {
                    resultBox.innerHTML = `
                        <div class="flex justify-between border-b border-white/5 pb-2">
                            <span class="data-label">PARTNER</span>
                            <span class="data-value">${res.data.partner_uid}</span>
                        </div>
                        <div class="flex justify-between border-b border-white/5 pb-2">
                            <span class="data-label">INTIMACY</span>
                            <span class="data-value text-yellow-400">${res.data.score}</span>
                        </div>
                        <div class="flex justify-between border-b border-white/5 pb-2">
                            <span class="data-label">LEVEL</span>
                            <span class="data-value">LVL ${res.data.level}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="data-label">DAYS</span>
                            <span class="data-value">${res.data.days_active} DAYS</span>
                        </div>
                    `;
                } else {
                    resultBox.innerHTML = `<div class="text-red-500 text-[11px] font-bold text-center uppercase tracking-wider">[!] ${res.message}</div>`;
                }
            } catch (err) {
                loader.classList.add('hidden');
                resultBox.classList.remove('hidden');
                resultBox.innerHTML = `<div class="text-red-500 text-[11px] font-bold text-center uppercase">[!] Connection Error</div>`;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE)

@app.route('/get_data', methods=['POST'])
def get_data():
    uid = request.json.get('uid')
    try:
        t_url = f"https://spidey-jwt-gen.vercel.app/guest?uid={GUEST_UID}&password={GUEST_PASSWORD}"
        token = requests.get(t_url, timeout=10).json().get("token")
        if not token: return jsonify({"status": "error", "message": "Auth Failed"})

        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/x-www-form-urlencoded", "X-GA": "v1 1", "ReleaseVersion": "OB53"}
        payload = build_uid_protobuf(uid)
        resp = requests.post(f"{BASE_URL}/GetSpecialFriendList", headers=headers, data=payload, timeout=10, verify=False)
        
        if resp.status_code == 200:
            dec_data = dec(resp.content)
            proto = SpecialFriend_pb2.SpecialFriendResponse()
            proto.ParseFromString(dec_data)
            if not proto.HasField("duo_info"): return jsonify({"status": "error", "message": "No Duo Found"})

            d = proto.duo_info
            s = d.score
            lv = 1
            if s < 301: lv = 2
            elif s < 501: lv = 3
            elif s < 801: lv = 4
            elif s < 1201: lv = 5
            else: lv = 6

            return jsonify({"status": "success", "data": {"partner_uid": str(d.partner_uid), "level": lv, "score": s, "days_active": d.days_active}})
        return jsonify({"status": "error", "message": "Server Error"})
    except Exception as e: return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
