# Ataques contra cifrado Vigenère

Este repositorio contiene herramientas para atacar el cifrado Vigenère.

Es un intento de resolver un [puzzle compartido en Reddit](https://www.reddit.com/r/ciberseguridad/comments/1ox7bpf/quien_me_ayuda_con_este_mensaje_cifrado_lo/), que da a entender que es un cifrado Vigenère, pero no responde al método Kasiki. El contenido del puzzle está en el archivo `encoded_texts.py`.

El código permite usar un alfabeto personalizado, por ejemplo para incluir la ñ.

## Ataques

### Ataque por fuerza bruta

Genera todas las posibles claves de una longitud dada y busca coincidencias de cierta longitud en el texto cifrado.

```bash
python attack_by_bruteforce.py
```


### Ataque por diccionario

Carga un diccionario de palabras y busca coincidencias de cierta longitud en el texto cifrado.

```bash
python attack_by_dictionary.py
```

### Ataque por Kasiski híbrido

Busca secuencias repetidas en el texto cifrado y usa la longitud de estas secuencias para determinar la longitud de la clave. Si la longitud de la clave es pequeña, prueba todas las combinaciones posibles.

```bash
python attack_by_kasiki.py
```
