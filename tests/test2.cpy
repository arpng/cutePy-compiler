def main_factorial():
#{
	#$ declations #$
	#declare x
	#declare i, fact
	#$ body of main_factorial #$
	fact = 1;
	i = 1;
	x = int(input());
	x = int(input());
	
	
	while (i<=x):
	#{
		fact = fact * i;
		i = i + 1;
	#}
	print(fact);
#}

if __name__ == "__main__":
	#$ call of main functions #$
	main_factorial();

while (i<=30):
	#{
		if (isPrime(i)==1):
			print(i);
		i = i + 1;
	#}