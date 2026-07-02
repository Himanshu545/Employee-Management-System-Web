import os


class Config:

    SECRET_KEY = "ems_secret_key"

    DATABASE = os.path.join(

        "database",

        "employee.db"

    )

    DEBUG = True