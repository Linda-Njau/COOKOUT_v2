import os
os.environ[DATABASE_URL] 'sqlite://'

from datetime import datetime, timedelta
import unittest
from app import app, db
from models import User, Recipe

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = 