source_text_name = 'text.txt'
with open(source_text_name, encoding='utf-8') as f:
    content = f.readlines()
shingles = []
shingle_phrases = []
text = ''.join(content)
text = text.replace('\n', '')
words = text.split(' ')
last_word_id = 0
for i in range(100):
    words_to_write = []
    words_len = 0
    for j in range(last_word_id, len(words)):
        word = words[j]
        if (words_len + len(word)) < 100:
            words_len += len(word)
            words_to_write.append(word)
        else:
            last_word_id = j + 1
            words_to_write.append(word)
            break
    text_to_write = ' '.join(words_to_write)
    with open(f'{i}.txt', 'w+', encoding='utf-8') as f:
        f.writelines(text_to_write)
