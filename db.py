import redis

__db = redis.Redis('localhost')

def add_user(user):
	__db.append('to_notify', ' ' + str(user.id))

def get_users():
	users = str(__db.get('to_notify'))
	return users.strip().split(' ') if users is not None else []

def clear_users():
	__db.delete('to_notify')

def remove_user(user):
	users = get_users()
	
	try:
		users.remove(str(user.id))
	except:
		pass

	__db.set('to_notify', ' '.join(users))