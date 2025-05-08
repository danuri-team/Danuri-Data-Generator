import uuid
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def uuid_bin():
    return uuid.uuid4().bytes

def now():
    return datetime.now()

def random_time():
    return (datetime.min + timedelta(seconds=random.randint(0, 86400))).time()

def generate_mock_data(count: int):
    companies, admins, items, spaces = [], [], [], []
    devices, users, usage_histories, rentals, user_auth_codes = [], [], [], [], []

    for _ in range(count):
        companies.append({
            'id': uuid_bin(),
            'name': fake.company(),
            'create_at': now()
        })

    for _ in range(count):
        admins.append({
            'id': uuid_bin(),
            'company_id': random.choice(companies)['id'],
            'email': fake.email(),
            'password': fake.password(),
            'phone': fake.numerify('010-####-####'),
            'role': random.choice(['ROLE_ADMIN', 'ROLE_DEVICE']),
            'status': random.choice(['AVAILABLE', 'NEED_COMPANY_APPROVE'])
        })

    for _ in range(count):
        total_qty = random.randint(5, 20)
        items.append({
            'id': uuid_bin(),
            'company_id': random.choice(companies)['id'],
            'name': fake.word()[:10],
            'total_quantity': total_qty,
            'available_quantity': random.randint(0, total_qty),
            'status': random.choice(['AVAILABLE', 'NOT_AVAILABLE'])
        })

    for _ in range(count):
        spaces.append({
            'id': uuid_bin(),
            'company_id': random.choice(companies)['id'],
            'name': fake.word()[:50],
            'start_at': random_time(),
            'end_at': random_time()
        })

    for _ in range(count):
        unique_space_ids = random.sample([s['id'] for s in spaces], k=min(count, len(spaces)))

        devices = []
        for space_id in unique_space_ids:
            devices.append({
                'id': uuid_bin(),
                'company_id': random.choice(companies)['id'],
                'device_id': uuid_bin(),
                'role': random.choice(['ROLE_ADMIN', 'ROLE_DEVICE']),
                'create_at': now(),
                'end_at': now() + timedelta(days=random.randint(1, 10))
            })

    for _ in range(count):
        users.append({
            'id': uuid_bin(),
            'company_id': random.choice(companies)['id'],
            'name': fake.first_name()[:20],
            'phone': fake.numerify('010-####-####'),
            'create_at': now(),
            'update_at': now(),
            'age': random.choice(['ADULT', 'ELEMENTARY', 'HIGH', 'MIDDLE', 'OUT_OF_SCHOOL_YOUTH']),
            'sex': random.choice(['FEMALE', 'MALE'])
        })

    for _ in range(count):
        usage_histories.append({
            'id': uuid_bin(),
            'user_id': random.choice(users)['id'],
            'space_id': random.choice(spaces)['id'],
            'start_at': now(),
            'end_at': now() + timedelta(hours=random.randint(1, 3))
        })

    for _ in range(count):
        usage = random.choice(usage_histories)
        item = random.choice(items)
        qty = random.randint(1, item['total_quantity'])
        rentals.append({
            'id': uuid_bin(),
            'item_id': item['id'],
            'usage_id': usage['id'],
            'quantity': qty,
            'returned_quantity': random.randint(0, qty),
            'borrowed_at': usage['start_at'],
            'returned_at': usage['end_at'] if random.random() > 0.3 else None
        })

    for _ in range(count):
        user_auth_codes.append({
            'id': uuid_bin(),
            'auth_code': f"{random.randint(100000, 999999)}",
            'created_at': now(),
            'expired_at': now() + timedelta(minutes=5),
            'phone': fake.numerify('010-####-####')
        })

    return {
        'company': companies,
        'admin': admins,
        'item': items,
        'space': spaces,
        'device': devices,
        'user': users,
        'usage_history': usage_histories,
        'rental': rentals,
        'user_auth_code': user_auth_codes
    }
