filename = input('Введите название файла: ')
with open(filename, encoding='utf-8') as f:
	content = f.readlines()
content = [x.strip() for x in content]
count = 0
for line in content:
	words = line.split(' ')
	count += len(words)
print(count)
