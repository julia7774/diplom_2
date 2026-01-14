from faker import Faker

faker = Faker(locale="ru")


def generate_email():
    return faker.email()


def generate_login():
    return faker.user_name()


def generate_password():
    return faker.password(10)
