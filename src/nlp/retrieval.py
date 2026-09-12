# -*- coding: utf-8 -*-
"""Utilidades del pipeline de recuperación aumentada."""

from __future__ import annotations

from collections import Counter


def tokenizar(texto: str) -> list[str]:
    """Tokeniza en minúsculas y normaliza espacios en blanco."""
    limpio = "".join(caracter if caracter.isalnum() or caracter.isspace() else " " for caracter in texto.lower())
    return [token for token in limpio.split() if token]


def fragmentar(texto: str, tamano: int = 512, solapamiento: int = 50) -> list[str]:
    """Divide el texto en fragmentos con solapamiento controlado."""
    if tamano <= 0:
        raise ValueError("El tamaño del fragmento debe ser mayor que cero")
    if solapamiento < 0 or solapamiento >= tamano:
        raise ValueError("El solapamiento debe estar entre cero y el tamaño del fragmento")

    palabras = texto.split()
    if not palabras:
        return []

    paso = tamano - solapamiento
    fragmentos = []
    for inicio in range(0, len(palabras), paso):
        bloque = palabras[inicio:inicio + tamano]
        if bloque:
            fragmentos.append(" ".join(bloque))
        if inicio + tamano >= len(palabras):
            break
    return fragmentos


def similitud_coseno(vector_a: list[float], vector_b: list[float]) -> float:
    """Calcula la similitud coseno entre dos vectores."""
    if len(vector_a) != len(vector_b):
        raise ValueError("Los vectores deben tener la misma dimensión")
    producto = sum(a * b for a, b in zip(vector_a, vector_b))
    norma_a = sum(a * a for a in vector_a) ** 0.5
    norma_b = sum(b * b for b in vector_b) ** 0.5
    if norma_a == 0 or norma_b == 0:
        return 0.0
    return round(producto / (norma_a * norma_b), 6)


def puntuacion_bm25(consulta: str, documento: str, k1: float = 1.5, b: float = 0.75,
                    longitud_media: float = 200.0) -> float:
    """Aproximación simplificada de BM25 para ordenar fragmentos."""
    terminos = tokenizar(consulta)
    palabras_documento = tokenizar(documento)
    if not terminos or not palabras_documento:
        return 0.0

    frecuencias = Counter(palabras_documento)
    longitud = len(palabras_documento)
    puntuacion = 0.0
    for termino in set(terminos):
        frecuencia = frecuencias.get(termino, 0)
        if frecuencia == 0:
            continue
        denominador = frecuencia + k1 * (1 - b + b * longitud / max(longitud_media, 1.0))
        puntuacion += (frecuencia * (k1 + 1)) / denominador
    return round(puntuacion, 6)


def rango_reciproco(listas: list[list[str]], k: int = 60) -> dict[str, float]:
    """Fusiona varios rankings mediante combinación recíproca de rangos."""
    puntuaciones: dict[str, float] = {}
    for lista in listas:
        for posicion, identificador in enumerate(lista, start=1):
            puntuaciones[identificador] = puntuaciones.get(identificador, 0.0) + 1.0 / (k + posicion)
    return {clave: round(valor, 8) for clave, valor in sorted(puntuaciones.items(), key=lambda x: -x[1])}


def recall_en_k(relevantes: set[str], recuperados: list[str], k: int) -> float:
    """Calcula el recall en los primeros k resultados recuperados."""
    if not relevantes:
        return 0.0
    recuperados_k = set(recuperados[:k])
    return round(len(relevantes & recuperados_k) / len(relevantes), 6)


def rango_reciproco_medio(relevantes: list[set[str]], recuperados: list[list[str]]) -> float:
    """Calcula el rango recíproco medio sobre un conjunto de consultas."""
    if len(relevantes) != len(recuperados):
        raise ValueError("La cantidad de consultas y de listas recuperadas debe coincidir")
    valores = []
    for esperados, obtenidos in zip(relevantes, recuperados):
        for posicion, identificador in enumerate(obtenidos, start=1):
            if identificador in esperados:
                valores.append(1.0 / posicion)
                break
        else:
            valores.append(0.0)
    return round(sum(valores) / len(valores), 6) if valores else 0.0
