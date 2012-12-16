# >>> parse("(((())()()(()))()(()(()))()(()))")
# '22528000'

def bracketparse(s):
	primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61]
	try:
		h,s = s[0],s[1:]
		if h == ')':
			return (')'+s),0
		if h != '(':
			raise Exception
		if s[0] == ')':
			return s[1:],0
	
		subs = []
		
		s2='*'+s
		while s2 != s:
			s2 = s
			s,n = bracketparse(s2)
			if n > 32:
				raise Exception
			subs += [n]

		h,s = s[0],s[1:]
		if h != ')':
			raise Exception
		
		return s, reduce(lambda x,(y,z): x*pow(y,z), zip(primes,subs), 1)
	except:
		raise Exception

def parse(s):
	try:
		s,n = bracketparse(s)
		if len(s): return "NO"
		return "%d"%n
	except:
		return "NO"

