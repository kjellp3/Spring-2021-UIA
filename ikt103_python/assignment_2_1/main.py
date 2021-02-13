import math

num_list = []

while True:
    num = float(input("Give me a number: "))
    if num == float(0): break
    num_list.append(num)

if len(num_list) != 0:
    num_list.sort(reverse=True)
    print("Average :", round(sum(num_list)/len(num_list),2))
    print("Median :", num_list[math.floor(len(num_list)/2)] if len(num_list) % 2 != 0 else round((num_list[int(len(num_list)/2-1)] + num_list[int(len(num_list)/2)])/2,2))
    print("Descending :", " ".join([str(num) for num in num_list]))
