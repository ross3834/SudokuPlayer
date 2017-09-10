from sys import argv
from csv import reader

def GetPuzzle(filename:str):
	if filename[-4:] != ".csv":
		filename += ".csv"
	try:
		with open(filename, 'rt') as sfile:
			puzzle = reader(sfile, delimiter=',')
			for row in puzzle:
				for box in row.strip():
					pass
	except FileNotFoundError:
		print("\"" + filename + "\" Could not be found.")
if __name__ == "__main__":
	GetPuzzle(argv[1])
