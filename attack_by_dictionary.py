import encoded_texts
from tools import load_dicts, decrypt, find_words


def main():
    dictionary_attack(encoded_texts.ESDLA, min_lookup_word_lenth=5, ñ=False)


def dictionary_attack(text: str, min_lookup_word_lenth: int, ñ: bool = False):
    if ñ:
        print('Modo ñ activado 😎')
        alpha = 'abcdefghijklmnñopqrstuvwxyz'
    else:
        alpha = 'abcdefghijklmnopqrstuvwxyz'

    print(f'Buscando clave verificando coincidencias de longitud {min_lookup_word_lenth}+...')

    words = load_dicts(['dicts/0_palabras_todas.txt', 'dicts/passwords.txt'])
    print(f'Diccionario cargado: {len(words):,} palabras')

    lookup_words = set(w for w in words if len(w) >= min_lookup_word_lenth)
    print(f'Palabras de longitud {min_lookup_word_lenth}+: {len(lookup_words):,}')

    i = 0
    best = ''
    best_accuracy = 0
    total_len = len(words)
    for word in words:
        i += 1
        if i % 100_000 == 0:
            print(f'Procesado {i / total_len * 100:.2f}%')

        result = decrypt(text, word, alphabet=alpha)
        accuracy = find_words(result, lookup_words)

        if accuracy > best_accuracy:
            best = word
            best_accuracy = accuracy
            print(f'Nueva coincidencia de {best_accuracy * 100:.2f}%: {best}')
            print(result)

    if best:
        print(f'Mejor coincidencia de {best_accuracy * 100:.2f}%: {best}')
        print(decrypt(text, best, alphabet=alpha))
    else:
        print('No se encontró ninguna coincidencia')


if __name__ == '__main__':
    main()
