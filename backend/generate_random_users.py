from faker import Faker
from database import get_db
import crud

# Initialize Faker
fake = Faker()

def create_random_users(n=100):
    db = get_db()
    for _ in range(n):
        name = fake.name()
        email = fake.unique.email()  # Ensure unique emails
        password = fake.password()

        try:
            crud.create_user(db, name, email, password)
            print(f"User created: {name} - {email}")
        except ValueError as e:
            print(f"Error creating user: {e}")
    db.close()
