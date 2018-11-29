#!/usr/bin/env python3
import os


REQUIRED_ENV_VARS = (
    'AZ_GROUP',
    'AZ_LOCATION',
    'APP_SERVICE_APP_NAME',
    'POSTGRES_SERVER_NAME',
    'POSTGRES_ADMIN_USER',
    'POSTGRES_ADMIN_PASSWORD',
    'APP_DB_NAME',
)


def verify_environment():
    missing = []
    for v in REQUIRED_ENV_VARS:
        if v not in os.environ:
            missing.append(v)
    if missing:
        print("Required Environment Variables Unset:")
        print("\t" + "\n\t".join(missing))
        print("Exiting.")
        exit()


if __name__ == '__main__':
    verify_environment()
