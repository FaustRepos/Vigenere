import encoded_texts
from tools import load_dicts, decrypt, find_words, generate_permutations
from collections import Counter
from itertools import product


def main():
    kasiski_attack(
        encoded_texts.ESDLA,
        min_sequence_length=3,
        max_key_length=12,
        min_lookup_word_lenth=5,
        ñ=False
    )


def kasiski_attack(
    text: str,
    min_sequence_length: int,
    max_key_length: int,
    min_lookup_word_lenth: int,
    ñ: bool = False
):
    if ñ:
        print('Modo ñ activado 😎')
        alpha = 'abcdefghijklmnñopqrstuvwxyz'
    else:
        alpha = 'abcdefghijklmnopqrstuvwxyz'

    print(f'Aplicando método Kasiski con secuencias de longitud {min_sequence_length}+...')

    clean_text = ''.join(c for c in text.lower() if c in alpha)

    print(f'Texto limpio: {len(clean_text)} caracteres')

    distances = find_repeated_sequences(clean_text, min_sequence_length)

    if not distances:
        print('No se encontraron secuencias repetidas')
        return

    print(f'Encontradas {len(distances)} distancias entre repeticiones')

    key_lengths = analyze_distances(distances, max_key_length)

    if not key_lengths:
        print('No se pudieron determinar longitudes de clave probables')
        return

    print(f'Longitudes de clave más probables: {key_lengths[:10]}')

    words = load_dicts(['dicts/0_palabras_todas.txt', 'dicts/passwords.txt'], min_lenth=min_lookup_word_lenth)
    print(f'Diccionario cargado: {len(words):,} palabras')

    best = ''
    best_accuracy = 0

    for key_length in key_lengths[:10]:
        print(f'\nProbando longitud de clave: {key_length}')

        if key_length <= 4:
            print('Longitud pequeña, probando todas las combinaciones...')
            keys_to_test = generate_permutations(max_len=key_length, alphabet=alpha)

            for key in keys_to_test:
                result = decrypt(text, key, alphabet=alpha)
                accuracy = find_words(result, words)

                if accuracy > best_accuracy:
                    best = key
                    best_accuracy = accuracy
                    print(f'Nueva coincidencia de {best_accuracy * 100:.2f}%: {key}')
                    print(result)
        else:
            keys_to_test = find_keys_by_frequency_multiple(clean_text, key_length, alpha, words, text)

            for key, accuracy in keys_to_test:
                if accuracy > best_accuracy:
                    best = key
                    best_accuracy = accuracy
                    print(f'Nueva coincidencia de {best_accuracy * 100:.2f}%: {key}')
                    print(decrypt(text, key, alphabet=alpha))

    if best:
        print(f'\nMejor coincidencia de {best_accuracy * 100:.2f}%: {best}')
        print(decrypt(text, best, alphabet=alpha))
    else:
        print('No se encontró ninguna coincidencia')


def find_repeated_sequences(text: str, min_length: int) -> list[int]:
    distances = []
    sequences = {}

    for length in range(min_length, min(len(text) // 2, 10)):
        for i in range(len(text) - length + 1):
            sequence = text[i:i + length]

            if sequence in sequences:
                for prev_pos in sequences[sequence]:
                    distance = i - prev_pos
                    distances.append(distance)
                sequences[sequence].append(i)
            else:
                sequences[sequence] = [i]

    return distances


def analyze_distances(distances: list[int], max_key_length: int) -> list[int]:
    factors = []

    for distance in distances:
        for i in range(2, min(distance + 1, max_key_length + 1)):
            if distance % i == 0:
                factors.append(i)

    if not factors:
        return []

    factor_counts = Counter(factors)
    sorted_factors = sorted(factor_counts.items(), key=lambda x: x[1], reverse=True)

    return [factor for factor, count in sorted_factors]


def find_key_by_frequency(text: str, key_length: int, alphabet: str) -> str:
    spanish_freq = 'eaosrnidlctumpbgvyqhfzjxkw'

    key = []

    for i in range(key_length):
        subsequence = text[i::key_length]

        char_counts = Counter(subsequence)
        most_common = char_counts.most_common(1)[0][0]

        shift = (alphabet.index(most_common) - alphabet.index(spanish_freq[0])) % len(alphabet)
        key_char = alphabet[shift]
        key.append(key_char)

    return ''.join(key)


def find_keys_by_frequency_multiple(
    clean_text: str,
    key_length: int,
    alphabet: str,
    words: set,
    original_text: str,
    top_candidates: int = 3,
    max_keys: int = 100
) -> list[tuple[str, float]]:
    spanish_freq = 'eaosrnidlctumpbgvyqhfzjxkw'

    candidates_per_position = []

    for i in range(key_length):
        subsequence = clean_text[i::key_length]
        char_counts = Counter(subsequence)
        most_common_chars = [char for char, count in char_counts.most_common(top_candidates)]

        position_candidates = []
        for common_char in most_common_chars:
            for freq_char in spanish_freq[:top_candidates]:
                shift = (alphabet.index(common_char) - alphabet.index(freq_char)) % len(alphabet)
                key_char = alphabet[shift]
                position_candidates.append(key_char)

        candidates_per_position.append(list(set(position_candidates)))

    all_key_combinations = product(*candidates_per_position)

    results = []
    for idx, key_tuple in enumerate(all_key_combinations):
        if idx >= max_keys:
            break

        key = ''.join(key_tuple)
        result = decrypt(original_text, key, alphabet=alphabet)
        accuracy = find_words(result, words)
        results.append((key, accuracy))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:10]


if __name__ == '__main__':
    main()
