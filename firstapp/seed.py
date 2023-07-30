from faker import Faker
from .models import Employee
def seed_db(num_employees):
    fake = Faker()

    for _ in range(num_employees):
        name = fake.name()
        phone = fake.phone_number()
        dob = fake.date_of_birth(minimum_age=18, maximum_age=62)
        doj = fake.date_between(start_date='-10y', end_date='today')
        address = fake.address().replace('\n', ', ')
        city = fake.city()
        state = fake.state()
        team = fake.random_element(elements=('A', 'B', 'C', 'D', 'E'))
        salary = fake.random_int(min=30000, max=150000)

        Employee.objects.create(
            name=name,
            phone=phone,
            dob=dob,
            doj=doj,
            address=address,
            city=city,
            state=state,
            team=team,
            salary=salary,
        )