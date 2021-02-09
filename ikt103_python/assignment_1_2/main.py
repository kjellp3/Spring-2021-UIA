string = input("GIVE ME A STRING GODDAMMIT ")
print(len(string))
if string == string[::-1]:
    print("is a palindrome")
else:
    print("is not a palindrome")
print(string[::-1])
#print("".join(list(reversed(string)))) A stupid way of doing it