
word_dict = {}

while True:
    word = input("Give me a word: ")
    if word == "stop": break
    if word in word_dict.keys(): word_dict[word] += 1
    else: word_dict[word] = 1

print("Unique :", len(word_dict))
print("Total :", sum(word_dict.values()))
[print(f"{word} : {count}") for word,count in word_dict.items()]
