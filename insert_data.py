import os
import pymysql
from generate_data import generate_mock_data

# DB 연결 설정
conn = pymysql.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    charset='utf8mb4'
)
cursor = conn.cursor()

# 생성할 mock 데이터 개수 입력
count = int(input("테이블당 mock 데이터 개수: "))
data = generate_mock_data(count)

# 1. company
for c in data['company']:
    cursor.execute("""
        INSERT INTO company (id, name, created_at)
        VALUES (%s, %s, %s)
    """, (c['id'], c['name'], c['created_at']))

# 2. admin
for a in data['admin']:
    cursor.execute("""
        INSERT INTO admin (id, company_id, email, password, phone, role, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (a['id'], a['company_id'], a['email'], a['password'], a['phone'], a['role'], a['status']))

# 3. item
for i in data['item']:
    cursor.execute("""
        INSERT INTO item (id, company_id, name, total_quantity, available_quantity, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (i['id'], i['company_id'], i['name'], i['total_quantity'], i['available_quantity'], i['status']))

# 4. space
for s in data['space']:
    cursor.execute("""
        INSERT INTO space (id, company_id, name, start_at, end_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (s['id'], s['company_id'], s['name'], s['start_at'], s['end_at']))

# 5. device
for d in data['device']:
    cursor.execute("""
        INSERT INTO device (id, company_id, role, created_at)
        VALUES (%s, %s, %s, %s)
    """, (d['id'], d['company_id'], d['role'], d['created_at']))

# 6. user
for u in data['user']:
    cursor.execute("""
        INSERT INTO user (id, company_id, name, phone, age, sex, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (u['id'], u['company_id'], u['name'], u['phone'], u['age'], u['sex'], u['created_at'], u['updated_at']))

# 7. usage_history
for uh in data['usage_history']:
    cursor.execute("""
        INSERT INTO usage_history (id, space_id, user_id, start_at, end_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (uh['id'], uh['space_id'], uh['user_id'], uh['start_at'], uh['end_at']))

# 8. rental
for r in data['rental']:
    cursor.execute("""
        INSERT INTO rental (id, item_id, usage_id, quantity, returned_quantity, borrowed_at, returned_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (r['id'], r['item_id'], r['usage_id'], r['quantity'], r['returned_quantity'], r['borrowed_at'], r['returned_at']))

# 9. user_auth_code
for uac in data['user_auth_code']:
    cursor.execute("""
        INSERT INTO user_auth_code (id, auth_code, created_at, expired_at, phone)
        VALUES (%s, %s, %s, %s, %s)
    """, (uac['id'], uac['auth_code'], uac['created_at'], uac['expired_at'], uac['phone']))

# 최종 커밋
conn.commit()
cursor.close()
conn.close()

print("모든 mock 데이터가 DB에 삽입되었습니다.")
