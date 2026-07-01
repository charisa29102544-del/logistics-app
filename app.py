# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# 1. เตรียมฐานข้อมูล
def init_db():
    conn = sqlite3.connect('logistics.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, time TEXT, phone_customer TEXT, job_id TEXT, driver_name TEXT, driver_phone TEXT, license_plate TEXT, province TEXT, port_name TEXT)''')
    conn.commit()
    conn.close()

init_db()

# 2. หน้าบันทึกงาน (ปรับกึ่งกลางแล้ว)
@app.route('/')
def index():
    provinces = ["กรุงเทพมหานคร", "กระบี่", "กาญจนบุรี", "กาฬสินธุ์", "กำแพงเพชร", "ขอนแก่น", "จันทบุรี", "ฉะเชิงเทรา", "ชลบุรี", "ชัยนาท", "ชัยภูมิ", "ชุมพร", "เชียงราย", "เชียงใหม่", "ตรัง", "ตราด", "ตาก", "นครนายก", "นครปฐม", "นครพนม", "นครราชสีมา", "นครศรีธรรมราช", "นครสวรรค์", "นนทบุรี", "นราธิวาส", "น่าน", "บึงกาฬ", "บุรีรัมย์", "ปทุมธานี", "ประจวบคีรีขันธ์", "ปราจีนบุรี", "ปัตตานี", "พระนครศรีอยุธยา", "พะเยา", "พังงา", "พัทลุง", "พิจิตร", "พิษณุโลก", "เพชรบุรี", "เพชรบูรณ์", "แพร่", "ภูเก็ต", "มหาสารคาม", "มุกดาหาร", "แม่ฮ่องสอน", "ยโสธร", "ยะลา", "ร้อยเอ็ด", "ระนอง", "ระยอง", "ราชบุรี", "ลพบุรี", "ลำปาง", "ลำพูน", "เลย", "ศรีสะเกษ", "สกลนคร", "สงขลา", "สตูล", "สมุทรปราการ", "สมุทรสงคราม", "สมุทรสาคร", "สระบุรี", "สระแก้ว", "สิงห์บุรี", "สุพรรณบุรี", "สุราษฎร์ธานี", "สุรินทร์", "สุโขทัย", "หนองคาย", "หนองบัวลำภู", "อ่างทอง", "อำนาจเจริญ", "อุดรธานี", "อุตรดิตถ์", "อุทัยธานี", "อุบลราชธานี"]
    options = "".join([f'<option value="{p}">{p}</option>' for p in provinces])
    return render_template_string(f'''<!DOCTYPE html><html lang="th"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap" rel="stylesheet"><style>body {{ font-family: 'Kanit', sans-serif; background: #eef2f3; margin: 0; min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; }} .form-card {{ background: white; padding: 30px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); width: 100%; max-width: 500px; }} h1 {{ text-align: center; color: #333; }} input, select {{ width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }} button {{ width: 100%; padding: 12px; background: #27ae60; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 10px; }}</style></head><body><div class="form-card"><h1>บันทึกงานขนส่ง</h1><form action="/save" method="POST"><input type="date" name="date" required><input type="time" name="time" required><input type="text" name="phone_customer" placeholder="เบอร์โทรลูกค้า" required><input type="text" name="job_id" placeholder="Job ID" required><input type="text" name="driver_name" placeholder="ชื่อคนขับ" required><input type="text" name="driver_phone" placeholder="เบอร์โทรคนขับ" required><input type="text" name="license_plate" placeholder="ทะเบียนรถ" required><select name="province" required><option value="" disabled selected>-- เลือกจังหวัด --</option>{options}</select><input type="text" name="port_name" placeholder="สถานที่รับและส่ง" required><button type="submit">บันทึกข้อมูล</button></form><a href="/history" style="display:block; text-align:center; margin-top:15px; color:#34495e; text-decoration:none;">ดูตารางคิวงาน</a></div></body></html>''')

# 3. ระบบ Save
@app.route('/save', methods=['POST'])
def save_data():
    data = (request.form.get('date'), request.form.get('time'), request.form.get('phone_customer'), request.form.get('job_id'), request.form.get('driver_name'), request.form.get('driver_phone'), request.form.get('license_plate'), request.form.get('province'), request.form.get('port_name'))
    conn = sqlite3.connect('logistics.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO jobs (date, time, phone_customer, job_id, driver_name, driver_phone, license_plate, province, port_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
    conn.commit()
    conn.close()
    return redirect('/history')

# 4. หน้า History
@app.route('/history')
def show_history():
    search = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    per_page = 20
    offset = (page - 1) * per_page
    conn = sqlite3.connect('logistics.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE job_id LIKE ? OR driver_name LIKE ? OR license_plate LIKE ? ORDER BY id DESC LIMIT ? OFFSET ?", ('%'+search+'%', '%'+search+'%', '%'+search+'%', per_page, offset))
    jobs = cursor.fetchall()
    conn.close()
    start_no = offset + 1
    html = '''<!DOCTYPE html><html lang="th"><head><meta charset="UTF-8"><link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap" rel="stylesheet"><style>body { font-family: 'Kanit', sans-serif; background: #f4f7f6; padding: 10px; } h1 { text-align: center; color: #2c3e50; } .controls { background: white; padding: 15px; border-radius: 10px; display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); } .table-container { overflow-x: auto; background: white; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); } table { width: 100%; min-width: 900px; border-collapse: collapse; } th, td { padding: 10px; border-bottom: 1px solid #ddd; text-align: center; font-size: 13px; } th { background: #2c3e50; color: white; } .status-badge { background: #e8f8f0; color: #27ae60; padding: 5px 10px; border-radius: 15px; font-size: 12px; font-weight: bold; border: 1px solid #27ae60; } .pagination { margin: 20px 0; display: flex; justify-content: center; gap: 10px; } a { text-decoration: none; padding: 8px 15px; background: #3498db; color: white; border-radius: 5px; } a.secondary { background: #95a5a6; }</style></head><body><h1>ตารางคิวงาน</h1><div class="controls"><form action="/history" method="GET" style="display:flex; gap:5px;"><input type="text" name="q" placeholder="ค้นหา..." value="''' + search + '''" style="padding:8px; border:1px solid #ccc; border-radius:5px;"><button type="submit">ค้นหา</button><a href="/history" class="secondary">ล้างค่า</a></form><a href="/" style="background:#27ae60;">หน้าหลัก</a></div><div class="table-container"><table><tr><th>ลำดับ</th><th>วันที่</th><th>โทรลูกค้า</th><th>Job ID</th><th>คนขับ</th><th>โทรคนขับ</th><th>ทะเบียน</th><th>จังหวัด</th><th>สถานที่</th><th>สถานะ</th></tr>'''
    for i, j in enumerate(jobs):
        html += f'<tr><td>{start_no + i}</td><td>{j[1]}</td><td>{j[3]}</td><td>{j[4]}</td><td>{j[5]}</td><td>{j[6]}</td><td>{j[7]}</td><td>{j[8]}</td><td>{j[9]}</td><td><span class="status-badge">✓ เรียบร้อย</span></td></tr>'
    html += '</table></div><div class="pagination">'
    if page > 1: html += f'<a href="/history?page={page-1}&q={search}" class="secondary"><< หน้าก่อน</a>'
    html += f'<a href="/history?page={page+1}&q={search}">หน้าถัดไป >></a></div></body></html>'
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)




# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# ส่วนหัว HTML สำหรับ PWA
HEADER_PWA = '''
<link rel="manifest" href="/manifest.json">
<script>
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js');
  }
</script>
'''

def init_db():
    conn = sqlite3.connect('logistics.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, time TEXT, phone_customer TEXT, job_id TEXT, driver_name TEXT, driver_phone TEXT, license_plate TEXT, province TEXT, port_name TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    provinces = ["กรุงเทพมหานคร", "กระบี่", "กาญจนบุรี", "กาฬสินธุ์", "กำแพงเพชร", "ขอนแก่น", "จันทบุรี", "ฉะเชิงเทรา", "ชลบุรี", "ชัยนาท", "ชัยภูมิ", "ชุมพร", "เชียงราย", "เชียงใหม่", "ตรัง", "ตราด", "ตาก", "นครนายก", "นครปฐม", "นครพนม", "นครราชสีมา", "นครศรีธรรมราช", "นครสวรรค์", "นนทบุรี", "นราธิวาส", "น่าน", "บึงกาฬ", "บุรีรัมย์", "ปทุมธานี", "ประจวบคีรีขันธ์", "ปราจีนบุรี", "ปัตตานี", "พระนครศรีอยุธยา", "พะเยา", "พังงา", "พัทลุง", "พิจิตร", "พิษณุโลก", "เพชรบุรี", "เพชรบูรณ์", "แพร่", "ภูเก็ต", "มหาสารคาม", "มุกดาหาร", "แม่ฮ่องสอน", "ยโสธร", "ยะลา", "ร้อยเอ็ด", "ระนอง", "ระยอง", "ราชบุรี", "ลพบุรี", "ลำปาง", "ลำพูน", "เลย", "ศรีสะเกษ", "สกลนคร", "สงขลา", "สตูล", "สมุทรปราการ", "สมุทรสงคราม", "สมุทรสาคร", "สระบุรี", "สระแก้ว", "สิงห์บุรี", "สุพรรณบุรี", "สุราษฎร์ธานี", "สุรินทร์", "สุโขทัย", "หนองคาย", "หนองบัวลำภู", "อ่างทอง", "อำนาจเจริญ", "อุดรธานี", "อุตรดิตถ์", "อุทัยธานี", "อุบลราชธานี"]
    options = "".join([f'<option value="{p}">{p}</option>' for p in provinces])
    return render_template_string(f'''<!DOCTYPE html><html lang="th"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">{HEADER_PWA}<link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap" rel="stylesheet"><style>body {{ font-family: 'Kanit', sans-serif; background: #eef2f3; margin: 0; min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; }} .form-card {{ background: white; padding: 30px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); width: 100%; max-width: 500px; }} h1 {{ text-align: center; color: #333; }} input, select {{ width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }} button {{ width: 100%; padding: 12px; background: #27ae60; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 10px; }}</style></head><body><div class="form-card"><h1>บันทึกงานขนส่ง</h1><form action="/save" method="POST"><input type="date" name="date" required><input type="time" name="time" required><input type="text" name="phone_customer" placeholder="เบอร์โทรลูกค้า" required><input type="text" name="job_id" placeholder="Job ID" required><input type="text" name="driver_name" placeholder="ชื่อคนขับ" required><input type="text" name="driver_phone" placeholder="เบอร์โทรคนขับ" required><input type="text" name="license_plate" placeholder="ทะเบียนรถ" required><select name="province" required><option value="" disabled selected>-- เลือกจังหวัด --</option>{options}</select><input type="text" name="port_name" placeholder="สถานที่รับและส่ง" required><button type="submit">บันทึกข้อมูล</button></form><a href="/history" style="display:block; text-align:center; margin-top:15px; color:#34495e; text-decoration:none;">ดูตารางคิวงาน</a></div></body></html>''')

@app.route('/save', methods=['POST'])
def save_data():
    data = (request.form.get('date'), request.form.get('time'), request.form.get('phone_customer'), request.form.get('job_id'), request.form.get('driver_name'), request.form.get('driver_phone'), request.form.get('license_plate'), request.form.get('province'), request.form.get('port_name'))
    conn = sqlite3.connect('logistics.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO jobs (date, time, phone_customer, job_id, driver_name, driver_phone, license_plate, province, port_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
    conn.commit()
    conn.close()
    return redirect('/history')

# เพิ่ม Route สำหรับไฟล์ PWA
@app.route('/manifest.json')
def manifest():
    return app.send_static_file('manifest.json')

@app.route('/sw.js')
def sw():
    return app.send_static_file('sw.js')

@app.route('/history')
def show_history():
    search = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    per_page = 20
    offset = (page - 1) * per_page
    conn = sqlite3.connect('logistics.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE job_id LIKE ? OR driver_name LIKE ? OR license_plate LIKE ? ORDER BY id DESC LIMIT ? OFFSET ?", ('%'+search+'%', '%'+search+'%', '%'+search+'%', per_page, offset))
    jobs = cursor.fetchall()
    conn.close()
    start_no = offset + 1
    html = f'''<!DOCTYPE html><html lang="th"><head><meta charset="UTF-8">{HEADER_PWA}<link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap" rel="stylesheet"><style>body {{ font-family: 'Kanit', sans-serif; background: #f4f7f6; padding: 10px; }} h1 {{ text-align: center; color: #2c3e50; }} .controls {{ background: white; padding: 15px; border-radius: 10px; display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }} .table-container {{ overflow-x: auto; background: white; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }} table {{ width: 100%; min-width: 900px; border-collapse: collapse; }} th, td {{ padding: 10px; border-bottom: 1px solid #ddd; text-align: center; font-size: 13px; }} th {{ background: #2c3e50; color: white; }} .status-badge {{ background: #e8f8f0; color: #27ae60; padding: 5px 10px; border-radius: 15px; font-size: 12px; font-weight: bold; border: 1px solid #27ae60; }} .pagination {{ margin: 20px 0; display: flex; justify-content: center; gap: 10px; }} a {{ text-decoration: none; padding: 8px 15px; background: #3498db; color: white; border-radius: 5px; }} a.secondary {{ background: #95a5a6; }}</style></head><body><h1>ตารางคิวงาน</h1><div class="controls"><form action="/history" method="GET" style="display:flex; gap:5px;"><input type="text" name="q" placeholder="ค้นหา..." value="{search}" style="padding:8px; border:1px solid #ccc; border-radius:5px;"><button type="submit">ค้นหา</button><a href="/history" class="secondary">ล้างค่า</a></form><a href="/" style="background:#27ae60;">หน้าหลัก</a></div><div class="table-container"><table><tr><th>ลำดับ</th><th>วันที่</th><th>โทรลูกค้า</th><th>Job ID</th><th>คนขับ</th><th>โทรคนขับ</th><th>ทะเบียน</th><th>จังหวัด</th><th>สถานที่</th><th>สถานะ</th></tr>'''
    for i, j in enumerate(jobs):
        html += f'<tr><td>{start_no + i}</td><td>{j[1]}</td><td>{j[3]}</td><td>{j[4]}</td><td>{j[5]}</td><td>{j[6]}</td><td>{j[7]}</td><td>{j[8]}</td><td>{j[9]}</td><td><span class="status-badge">✓ เรียบร้อย</span></td></tr>'
    html += '</table></div><div class="pagination">'
    if page > 1: html += f'<a href="/history?page={page-1}&q={search}" class="secondary"><< หน้าก่อน</a>'
    html += f'<a href="/history?page={page+1}&q={search}">หน้าถัดไป >></a></div></body></html>'
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)