def move_words(string, words_to_remove):
    string_list = string.split()
    result_words = [word for word in string_list if word.lower() not in words_to_remove]
    result = ' '.join(result_words)
    print(result)


string = "What is hello?"
stop_words = ['what', 'is', 'a']

move_words(string, stop_words)