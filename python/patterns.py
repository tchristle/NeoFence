import random

def ranrec(a_show):
	while a_show:
		x1=random.randint(0,29)
		x2=random.randint(x1,29)
		y1=random.randint(0,55)
		y2=random.randint(y1,55)
		c=random.randint(0,384)
		rectf(x1,y1,x2,y2,c)
		time.sleep(5)