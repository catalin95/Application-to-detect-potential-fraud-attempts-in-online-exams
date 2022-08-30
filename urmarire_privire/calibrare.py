from __future__ import division
import cv2
from .pupila import Pupila


class Calibrare(object):
    # Aceasta clasa calibreaza algoritmul de detectare a pozitiei ochilor

    def __init__(self):
        self.nr_frameuri = 20
        self.limita_stanga = []
        self.limita_dreapta = []

    def calibrare_completa(self):
        # returneaza true daca calibrarea este completa
        return len(self.limita_stanga) >= self.nr_frameuri and len(self.limita_dreapta) >= self.nr_frameuri

    def limita(self, cadru):
        """
        Returneaza limita pentru ochi

        Argument:
            cadru: Indica daca este partea stanga (0) sau partea dreapta (1)
        """
        if cadru == 0:
            return int(sum(self.limita_stanga) / len(self.limita_stanga))
        elif cadru == 1:
            return int(sum(self.limita_dreapta) / len(self.limita_dreapta))

    @staticmethod
    def dimensiune_iris(cadru):
        """
        Returneaza procentajul pe care irisul il ocupa pe suprafata ochiului

        Argumente:
            cadru: cadrul irisului
        """
        cadru = cadru[5:-5, 5:-5]
        inaltime, lungime = cadru.shape[:2]
        nr_pixeli = inaltime * lungime
        nr_puncte_negre = nr_pixeli - cv2.countNonZero(cadru)
        return nr_puncte_negre / nr_pixeli

    @staticmethod
    def gasire_cadru_optim(cadru_ochi):
        """
        Calculeaza valoarea optima a limitei pentru ochi

        Argumente:
            cadru_iris: cadrul irisului care sa fie analizat
        """
        medie_dimensiune_iris = 36 #48
        incercari = {}

        for limita in range(5, 100, 5):
            rama_iris = Pupila.procesare_imagine(cadru_ochi, limita)
            incercari[limita] = Calibrare.dimensiune_iris(rama_iris)

        cadru_optim, marime_iris = min(incercari.items(), key=(lambda p: abs(p[1] - medie_dimensiune_iris)))
        return cadru_optim

    def evaluare(self, cadru_ochi, cadru):
        """
        Mareste calitatea calibrarii luand in considerare imaginea data

        Argumente:
            cadru_ochi: cadrul ochiului
            cadru: indica daca este ochiul stang (0) sau ochiul drept (1)
        """
        limita = self.gasire_cadru_optim(cadru_ochi)

        if cadru == 0:
            self.limita_stanga.append(limita)
        elif cadru == 1:
            self.limita_dreapta.append(limita)
