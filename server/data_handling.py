import motor.motor_asyncio
from hashlib import pbkdf2_hmac
import os
from pepper import pepper

url = "localhost"
port = 27017

iters = 500_000
client = motor.motor_asyncio.AsyncIOMotorClient(url, port)

db = client.login.users


def hashing(password: str, salt: bytes) -> bytes:
	return pbkdf2_hmac('sha256', (password.encode("utf-8") + pepper),
				salt, iters)


async def find_user(hashed_user):
	document = await db.find_one({"user": hashed_user})
	return document


async def insert_user(usr: str, password: str):
	user_salt = os.urandom(16)
	seasoned_password = hashing(password, user_salt)
	data = {'user': usr, 'password': seasoned_password, "salt": user_salt, "key":
			os.urandom(32).hex()}

	await db.insert_one(data)


async def check_pw(_user: dict, raw_password: str):
	if _user is not None:
		pw_check = hashing(raw_password, _user['salt'])
		return pw_check == _user['password']
