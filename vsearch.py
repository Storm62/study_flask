def search4vowels(word: str) -> set:
    """Выводит гласные, найденные в указанном слове"""
    vowels = set('аоеуэюяы')
    return vowels.intersection(set(word))


def search4letters(phrase: str, letters: str = 'аеоуэыюя') -> set:
    """Выводит указанные символы (по умолчанию гласные), найденные в указанной фразе"""
    return set(letters).intersection(set(phrase))
