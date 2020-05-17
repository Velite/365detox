from datetime import timedelta


class Config(object):
	SECRET_KEY = "Iq|3,WXuG'$^+8L86Pc$^hfmYid11>43@#sD=D61UP>6mO$R[I42J1D/8)W'S^"
	PERMANENT_SESSION_LIFETIME = timedelta(hours = 3)
	DATABASE = "sqliteext:///test.db"


class TestConfig(Config):
	DEBUG = True
	DROP_DB = True
