#!/usr/bin/env python3
# coding: utf-8

from decimal import getcontext
from decimal import Decimal as D


class Sampling():
    """classe statistique d'échantillonage et d'estimation

    Cette classe fourni un certains nombre d'outils permettant de calculer des intervales de confiance et des intervales de fluctuation.
    """
    def __init__(self, precision=8):
        """Constructeur de la classe

        :param precision: Précision de la décimale
        :type precision: int

        Le pourcentage est le seuil de confiance.
        Ainsi pour 1.96, l'intervale est juste à 95%
        """
        getcontext().prec = precision
        self.precisionPercent = {
            '99': D('2.58'),
            '95': D('1.96')
        }

    def intervalFluctuation(self, population, prob, precision=95):
        """Permet de calculer un intervale de fluctuation

        :param population: Echantillon de la population étudié
        :param prob: Proportion de présence du caractère dans la population
        :param precision: Le seuil de confiance
        :type population: float
        :type prob: float
        :type precision: int|string
        :rtype: tuple

        :Example:

        >>> sampling = Sampling()
        >>> sampling.intervalFluctuation(10000, 1/1000)
        (Decimal('0.00038050356'), Decimal('0.0016194964'))
        """
        population = D(population)
        prob = D(prob)

        percent = self.precisionPercent[str(precision)]
        if population >= 30 and population * prob >= 5 and population * (1 - prob) >= 5:
            interMin = prob - percent * (
                (prob * (1 - prob)).sqrt() / population.sqrt()
                )
            interMax = prob + percent * (
                (prob * (1 - prob)).sqrt() / population.sqrt()
                )
            return (float(interMin), float(interMax))
        else:
            raise ValueError("N >= 30, (N * P) >= 5, N * (1 - P) >= 5")

    def valideSample(self, featurePop, totalPop, prob, precision=95):
        """Permet de déterminer si l'hypothèse de ``prob`` est juste

        :param featurePop: Population ayant le caractère étudié
        :param totalPop: Echantillon de la population étudié
        :param prob: Proportion de présence du caractère dans la population
        :param precision: Le seuil de confiance
        :type featurePop: float
        :type totalPop: float
        :type prob: float
        :type precision: int|string
        :rtype: bool

        :Example:

        >>> sampling = Sampling()
        >>> sampling.valideSample(15, 10000, 1/1000)
        True
        """
        interval = self.intervalFluctuation(totalPop, prob, precision)
        frequency = featurePop / totalPop
        return interval[0] <= frequency <= interval[1]

    def intervalEstimate(self, featurePop, totalPop, strict=False, precision=95):
        """Permet de calculer un intervale de confiance

        Détermine à partir d'un échantillon la proportion de la population ayant le caractère étudié

        :param featurePop: Population ayant le caractère étudié
        :param totalPop: Echantillon de la population étudié
        :param prob: Proportion de présence du caractère dans la population
        :param strict: Si False utilise la formule simplifier
        :param precision: Le seuil de confiance
        :type featurePop: float
        :type totalPop: float
        :type prob: float
        :type strict: bool
        :type precision: int|string
        :rtype: tuple

        :Example:

        >>> sampling = Sampling()
        >>> sampling.intervalEstimate(22, 100)
        (Decimal('0.12'), Decimal('0.32'))
        >>> sampling.intervalEstimate(22, 100, strict=True)
        (Decimal('0.13880772'), Decimal('0.30119228'))
        """
        percent = self.precisionPercent[str(precision)]

        featurePop = D(featurePop)
        totalPop = D(totalPop)

        frequency = featurePop / totalPop
        if totalPop >= 30 and totalPop * frequency >= 5 and totalPop * (1 - frequency) >= 5:
            if strict:
                interMin = frequency - percent * (
                    (frequency * (1 - frequency)).sqrt() / totalPop.sqrt()
                )
                interMax = frequency + percent * (
                    (frequency * (1 - frequency)).sqrt() / totalPop.sqrt()
                )
            else:
                interMin = frequency - (1 / totalPop.sqrt())
                interMax = frequency + (1 / totalPop.sqrt())
            return (float(interMin), float(interMax))
        else:
            raise ValueError("N >= 30, (N * F) >= 5, N * (1 - F) >= 5")
