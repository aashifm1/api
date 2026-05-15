import os, hashlib, time, uuid
from flask import Flask, request, jsonify
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
app = Flask(__name__)

def get_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    token = auth_header.split(" ")[-1] 
    res = supabase.table("sessions").select("*").eq("token", token).execute()
    if res and res.data and res.data[0]['expires_at'] > time.time():
        return res.data[0]['email']
    return None

# home
@app.route('/', methods=['GET'])
def home():
    return "secure mini payment api"
    
# register
@app.route('/register', methods=['POST'])
def register():
    d = request.json or {}
    email, pw = d.get('email'), d.get('password')
    if not email or not pw: return "missing fields", 400
    hpw = hashlib.sha256(pw.encode()).hexdigest()
    try:
        supabase.table("users").insert({"email": email, "password": hpw}).execute()
        return "Registered", 201
    except: return "error or duplicate", 409

# login
@app.route('/login', methods=['POST'])
def login():
    ip, now = request.remote_addr, time.time()
    attempts = supabase.table("attempts").select("*").eq("ip", ip).execute().data
    if len([a for a in attempts if now - a['time'] < 60]) >= 5: return "rate limited", 429
    
    d = request.json or {}
    email, pw = d.get('email'), d.get('password')
    hpw = hashlib.sha256(pw.encode()).hexdigest()
    user = supabase.table("users").select("*").eq("email", email).eq("password", hpw).execute().data
    
    if user:
        token = str(uuid.uuid4())
        supabase.table("sessions").insert({"token": token, "email": email, "expires_at": now + 3600}).execute()
        return jsonify({"token": token})
    
    supabase.table("attempts").insert({"ip": ip, "time": now}).execute()
    return "invalid credentials", 401

# payment process
@app.route('/payment', methods=['POST'])
def payment():
    u = get_user()
    if not u: return "Unauthorized", 401
    d = request.json or {}
    a, c, m = d.get('amount'), d.get('currency'), d.get('merchant_id')
    if not all([a, c, m]) or not isinstance(a, (int, float)) or a <= 0: return "invalid input", 400
    
    recent = supabase.table("transactions").select("*").eq("user_email", u).eq("amount", a).eq("merchant", m).order("time", desc=True).limit(1).execute().data
    if recent and time.time() - recent[0]['time'] < 300: return "duplicate", 409
    
    supabase.table("transactions").insert({"user_email": u, "amount": a, "currency": c, "merchant": m, "time": time.time()}).execute()
    return "Paid", 201

# history
@app.route('/transactions', methods=['GET'])
def transactions():
    u = get_user()
    if not u: return "Unauthorized", 401
    return jsonify(supabase.table("transactions").select("*").eq("user_email", u).execute().data)

if __name__ == "__main__":
    app.run(port=5000)