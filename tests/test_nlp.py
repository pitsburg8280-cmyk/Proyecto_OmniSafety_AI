# -*- coding: utf-8 -*-
"""Pruebas del pipeline de recuperación documental."""

from __future__ import annotations

import pytest

from src.nlp import retrieval


def test_fragmentar_respeta_el_solapamiento() -> None:
    texto = " ".join(f"palabra{i}" for i in range(100))
    fragmentos = retrieval.fragmentar(texto, tamano=30, solapamiento=10)
    assert len(fragmentos) > 1
    primero = fragmentos[0].split()
    segundo = fragmentos[1].split()
    assert primero[-10:] == segundo[:10]


def test_fragmentar_rechaza_solapamiento_invalido() -> None:
    with pytest.raises(ValueError):
        retrieval.fragmentar("texto de prueba", tamano=10, solapamiento=10)


def test_similitud_coseno_de_vectores_identicos_es_uno() -> None:
    assert retrieval.similitud_coseno([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]) == pytest.approx(1.0)


def test_similitud_coseno_de_vectores_ortogonales_es_cero() -> None:
    assert retrieval.similitud_coseno([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)


def test_similitud_coseno_rechaza_dimensiones_distintas() -> None:
    with pytest.raises(ValueError):
        retrieval.similitud_coseno([1.0, 2.0], [1.0])


def test_bm25_prioriza_el_documento_con_el_termino() -> None:
    consulta = "presion hidraulica"
    relevante = retrieval.puntuacion_bm25(consulta, "manual de presion hidraulica del sistema")
    irrelevante = retrieval.puntuacion_bm25(consulta, "procedimiento de pintura industrial")
    assert relevante > irrelevante


def test_rango_reciproco_fusiona_y_ordena() -> None:
    fusion = retrieval.rango_reciproco([["a", "b"], ["b", "a"]])
    assert set(fusion) == {"a", "b"}
    assert fusion["a"] == pytest.approx(fusion["b"])


def test_recall_en_k() -> None:
    relevantes = {"a", "b", "c"}
    recuperados = ["x", "a", "y", "b"]
    assert retrieval.recall_en_k(relevantes, recuperados, k=2) == pytest.approx(1 / 3)
    assert retrieval.recall_en_k(relevantes, recuperados, k=4) == pytest.approx(2 / 3)


def test_recall_en_k_sin_relevantes() -> None:
    assert retrieval.recall_en_k(set(), ["a"], k=1) == 0.0


def test_rango_reciproco_medio() -> None:
    relevantes = [{"a"}, {"b"}]
    recuperados = [["a", "x"], ["x", "b"]]
    assert retrieval.rango_reciproco_medio(relevantes, recuperados) == pytest.approx(0.75)


def test_rango_reciproco_medio_valida_longitudes() -> None:
    with pytest.raises(ValueError):
        retrieval.rango_reciproco_medio([{"a"}], [["a"], ["b"]])
