from urllib.parse import quote_plus as urlquote
from datetime import timedelta

database_password = '1n9V@ti$2021'
DATABASE_URI = 'mysql+pymysql://innovatis:%s@54.90.39.27:3306/db_innovatis' % urlquote(database_password)
JWT_KEY = '1Mp4ct@1n9V@ti$2021'
ACCESS_EXPIRES = timedelta(hours=12)