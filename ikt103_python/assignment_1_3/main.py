

string1 = input("insert a string please: ")
string2 = input("insert a second string please: ")

if string1 == string2:
    print("are equal")
else:
    print("are not equal")
if string1 in string2 or string2 in string1:
    print("is a substring")
else:
    print("is not a substring")