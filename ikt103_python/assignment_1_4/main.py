
alphabet = {}
string = input("Give meh a sting: ") # Not sure if i got this one right
{alphabet.update({chr(i):0}) for i in range(97,123)}
[alphabet.update({char:alphabet[char]+1}) if char in alphabet.keys() else alphabet.update({char:1}) for char in string]
[print(f"'{char}' : {quant}") for char,quant in alphabet.items()]



