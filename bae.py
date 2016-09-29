def polyAlphaCipher(text, increment):
	newString = ""
	offset = 1
	for c in text:
		newString = newString + chr( (ord(c) + offset) % 255)
		offset = offset + increment
	return(newString)


def decoder(text, increment):
	newString = ""
	offset = 1
	for c in text:
		newString = newString + chr( (ord(c) - offset) % 255)
		offset = offset + increment
	print(newString)



if __name__ == '__main__':
	decoder(polyAlphaCipher("Welcome to New York", 2), 2)
