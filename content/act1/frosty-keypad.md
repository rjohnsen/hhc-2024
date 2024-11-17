+++
title = 'Frosty Keypad'
date = 2024-11-17T14:19:14+01:00
draft = true
weight = 2
+++


## Hints

### UV light

Numbers found from lighting at the keypad using the UV light:

```python
[ 2, 6, 7, 8 ]
```

![Frosty Keypad 1](/images/act1/frosty-keypad-1.png)

### Hint from the book

This is the hint we get:

![Frosty Keypad 2](/images/act1/frosty-keypad-2.png)

Thinking about it, it appears to correpond to

```
page:word:letter
```

Using this formula I got:

| Sequence | From book |
| -------- | --------- |
| 2:6:1    | S |
| 4:19:3   | A|
| 6:1:1    | N | 
| 3:10:4   | T |
| 14:8:3   | A | 

Somehow I got "_SANTA_". After much thoughtwork I came up with a scheme on how I can use this word - let's look at it with some _Regex filter_ spectacles:

| Position | Letter | Pattern |
| -------- | ------ | ------- |
| 1  | S | Pos 1 should not be same as pos. 5 |
| 2  | A | Pos 2 should be the same as pos. 5 |
| 3  | N | Pos 3 should not be the same as pos, 1, 2, 4, 5 |
| 4  | T | Pos 4 should not be the same as post 1, 2, 3, 5 |
| 5  | A | Pos 5 should be the same as pos. 2 |

## Solution

### Silver solution

#### Bruteforcer

Given the filter outlined under "Hint from the book", I created the following Python script to calcualte permutations and apply the filter scheme. I picked up the the remote URL and POST format from a BurpSuite session. The script:

```python
import requests, itertools, time

for perm in [''.join(p) for p in itertools.product(['2', '6', '7', '8'], repeat=5)]:
	if perm[0] is not perm[-1] and perm[1] == perm[-1]:
		if (perm[0] not in list(set(perm[2:4]))) and (perm[1] not in list(set(perm[2:4]))) and len(list(set(perm[2:4]))) > 1:
			res = requests.post(
				"https://hhc24-frostykeypad.holidayhackchallenge.com/submit",
				json = { "answer": perm }
			)

			if res.status_code != 400:
				print(perm)
				break
			else:
				time.sleep(1)
```

After just a couple of seconds, it produced the correct pin code:

```
72682
```

![Frosty Keypad 3](/images/act1/frosty-keypad-3.png)