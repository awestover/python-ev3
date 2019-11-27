"""
draw the space

of possible moves

encoded in thPosTable.csv
"""


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pdb import set_trace as tr

from random import random


df = pd.read_csv("thPosTable.csv")


def parseInp(inp):
	c = inp.split("_")
	c = [float(ci) for ci in c]
	return c


def sparse_get_pts():
	xs = []
	ys = []
	for r in df:
		if r != 'Unnamed: 0':
			for c in df[r]:
				if random() < 0.1:
					if not pd.isnull(c):
						cur = parseInp(c)
						xs.append(cur[0])
						ys.append(cur[1])

	return xs, ys


def get_pts():
	xs = []
	ys = []
	# tr()
	for r in df:
		if r != 'Unnamed: 0':
			for c in df[r]:
				if not pd.isnull(c):
					cur = parseInp(c)
					xs.append(cur[0])
					ys.append(cur[1])

	return xs, ys


def getThSpace():
	th1s = []
	th2s = []

	thCols = df['Unnamed: 0']

	for r in df:
		if r != 'Unnamed: 0':
			i = 0
			for c in df[r]:
				if not pd.isnull(c):
					th1s.append(thCols[i])
					th2s.append(float(r))
				i += 1

	return th1s, th2s


def main():

	th1s, th2s = getThSpace()
	plt.scatter(th1s, th2s)
	plt.show()

	xs, ys = get_pts()

	plt.ylim(0, 15)
	plt.scatter(xs, ys, c='k')

	plt.savefig("space.png")
	plt.show()


if __name__ == "__main__":
	main()



