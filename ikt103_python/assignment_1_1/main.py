


[print(number,end=" ") for number in range(1 ,11)]
print()
[print(number,end=" ") for number in range(1 ,21) if number % 2 == 0]
print()
[print(number,end=" ") for number in range(1 ,21) if number % 2 != 0]
print()
temp = 1

while True:
    print(temp,end=" ")
    temp+=3
    if temp >= 50: break

print()
number = 40
while number > 1:
    print(number,end=" ")
    number -= 4
print()
for number in range(2,101):
    check = True
    for i in range(2,number):
        if number % i == 0:
            check = False
            break
    if check:
        print(number,end=" ")




