import requests, itertools, time

for perm in [''.join(p) for p in itertools.product(['2', '6', '7', '8'], repeat=5)]:
	if perm[0] is not perm[-1] and perm[1] == perm[-1]:
		if (perm[0] not in list(set(perm[2:4]))) and (perm[1] not in list(set(perm[2:4]))): # and len(list(set(perm[2:4]))) > 1:
			res = requests.post(
				"https://hhc24-frostykeypad.holidayhackchallenge.com/submit",
				json = { "answer": perm }
			)

			if res.status_code != 400:
				print(f"{res.status_code} - {res.json()}- {perm}")
			else:
				time.sleep(1)