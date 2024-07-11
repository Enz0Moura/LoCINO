#!LoCINO/venv/bin
import os
import sys

from db_session import create_tables

if __name__ == '__main__':
    create_tables(use_my_sql=True)