import requests, itertools, time

for perm in [''.join(p) for p in itertools.product(['2', '6', '7', '8'], repeat=5)]:
		print(f"trying '{perm}' ... ", end="")
		res = requests.post(
			"https://hhc24-frostykeypad.holidayhackchallenge.com/submit",
			json = { "answer": perm }
		)

		if res.status_code != 400:
			print(f"{res.status_code} - {res.json()} - {perm}")
		else:
			print(" Negative")
			time.sleep(1)