import motor.motor_asyncio
import asyncio
from hashlib import pbkdf2_hmac
import os

our_app_iters = 500_000  # Application specific, read above.
client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)

users_doc = client.login.users


async def find_user(db, hashed_user):
	document = await db.find_one({"user": hashed_user})
	return document

async def insert_user(db, data):
	result = await db.insert_one(data)
	print('result %s' % repr(result.inserted_id))


user_salt = os.urandom(16)
user = "TestUser"
dk_password = pbkdf2_hmac('sha256', b'TestPassword', user_salt, our_app_iters)


data = {'user': user, 'password': dk_password, "salt": user_salt}


async def check_pw(_user, raw_password):
	if _user is not None:
		salt = _user['salt']
		pw_check = pbkdf2_hmac('sha256', raw_password, salt, our_app_iters)
		if pw_check == _user['password']:
			print('logged in')

async def main():

	# await insert_user(users_doc, data)
	_user = await find_user(users_doc, user)
	pw = b"TestPadssword"
	if _user is not None:
		salt = _user['salt']
		pw_check = pbkdf2_hmac('sha256', pw, salt, our_app_iters)
		if pw_check == _user['password']:
			print('logged in')

asyncio.run(main())



