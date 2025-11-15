from tools import generate_permutations, decrypt, find_words, load_dicts
import encoded_texts


def main():
    bruteforce(encoded_texts.ESDLA, max_permutation_length=4, min_lookup_word_lenth=5, ñ=False)


def bruteforce(text: str, max_permutation_length: int, min_lookup_word_lenth: int, ñ: bool = False):
    if ñ:
        print('Modo ñ activado 😎')
        alpha = 'abcdefghijklmnñopqrstuvwxyz'
    else:
        alpha = 'abcdefghijklmnopqrstuvwxyz'

    print((
        f'Permutando claves de longitud <= {max_permutation_length} '
        f'con coincidencias de longitud {min_lookup_word_lenth}+...'
    ))

    words = load_dicts(['dicts/0_palabras_todas.txt', 'dicts/passwords.txt'], min_lenth=min_lookup_word_lenth)
    print(f'Diccionario cargado: {len(words):,} palabras')

    i = 0
    best = ''
    best_accuracy = 0
    total_len = len(alpha) ** max_permutation_length
    for key in generate_permutations(max_len=max_permutation_length, alphabet=alpha):
        i += 1
        if i % 100_000 == 0:
            print(f'Procesado {i / total_len * 100:.2f}%')

        result = decrypt(text, key, alphabet=alpha)
        accuracy = find_words(result, words)

        if accuracy > best_accuracy:
            best = key
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
