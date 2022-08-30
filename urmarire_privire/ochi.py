import math
import numpy as np
import cv2
from .pupila import Pupila


class Ochi(object):
    #Aceasta clasa creeaza un nou cadru pentru a izola ochiul si a initializa detectarea pupilei

    PUNCT_OCHI_STANG = [36, 37, 38, 39, 40, 41]
    PUNCT_OCHI_DREPT = [42, 43, 44, 45, 46, 47]

    def __init__(self, cadru_original, repere, cadru, calibrare):
        self.cadru = None
        self.origine = None
        self.centru = None
        self.pupila = None
        self.puncte_de_reper = None

        self._analizeaza(cadru_original, repere, cadru, calibrare)

    @staticmethod
    def _punct_mijloc(p1, p2):
        """
        Returneaza punctul de mijloc (x, y) intre 2 puncte

        Argumente:
            p1 : primul punct
            p2 : al doilea punct
        """
        x = int((p1.x + p2.x) / 2)
        y = int((p1.y + p2.y) / 2)
        return (x, y)

    def _izoleaza(self, cadru, repere, arata):
        """
        Izoleaza un ochi, pentru a avea un cadru fara alta parte a fetei

        Argumente:
            cadru : cadrul continand fata
            repere: repere faciale pentru regiunea fetei
            arata: arata dupa un ochi
            
        """
        regiune = np.array([(repere.part(point).x, repere.part(point).y) for point in arata])
        regiune = regiune.astype(np.int32)
        self.puncte_de_reper = regiune

        # Aplicarea unei masti pentru a obtine doar ochiul
        inaltime, lungime = cadru.shape[:2]
        cadru_negru = np.zeros((inaltime, lungime), np.uint8)
        masca = np.full((inaltime, lungime), 255, np.uint8)
        cv2.fillPoly(masca, [regiune], (0, 0, 0))
        ochi = cv2.bitwise_not(cadru_negru, cadru.copy(), mask = masca)

        # Decuparea ochiului
        margine = 5
        min_x = np.min(regiune[:, 0]) - margine
        max_x = np.max(regiune[:, 0]) + margine
        min_y = np.min(regiune[:, 1]) - margine
        max_y = np.max(regiune[:, 1]) + margine

        self.cadru = ochi[min_y:max_y, min_x:max_x]
        self.origine = (min_x, min_y)

        inaltime, lungime = self.cadru.shape[:2]
        self.centru = (lungime / 2, inaltime / 2)

    def _ratie_clipire(self, repere, arata):
        """
        Calculeaza ratia care poate sa indice daca un ochi este inchis sau nu

        Argumente:
            repere: repere faciale pentru regiunea fetei
            arata: arata catre un ochi

        Returneaza:
            Ratia de clipire calculata
        """
        stanga = (repere.part(arata[0]).x, repere.part(arata[0]).y)
        dreapta = (repere.part(arata[3]).x, repere.part(arata[3]).y)
        sus = self._punct_mijloc(repere.part(arata[1]), repere.part(arata[2]))
        jos = self._punct_mijloc(repere.part(arata[5]), repere.part(arata[4]))

        latime_ochi = math.hypot((stanga[0] - dreapta[0]), (stanga[1] - dreapta[1]))
        lungime_ochi = math.hypot((sus[0] - jos[0]), (sus[1] - jos[1]))

        try:
            ratie = latime_ochi / lungime_ochi
        except ZeroDivisionError:
            ratie = None

        return ratie

    def _analizeaza(self, cadru_original, repere, cadru, calibrare):
        """
        Detecteaza si izoleaza ochiul intr-un cadru nou
        Trimite datele catre calibrare si initializeaza obiectul Pupila

        Argumente:
            cadrul_original: cadrul trimis de utilizator
            repere: repere faciale pentru regiunea fetei
            cadru: indica daca este ochiul stang sau drept
            calibrare: administreaza limita
        """
        if cadru == 0:
            arata = self.PUNCT_OCHI_STANG
        elif cadru == 1:
            arata = self.PUNCT_OCHI_DREPT
        else:
            return

        self.blinking = self._ratie_clipire(repere, arata)
        self._izoleaza(cadru_original, repere, arata)

        if not calibrare.calibrare_completa():
            calibrare.evaluare(self.cadru, cadru)

        limita = calibrare.limita(cadru)
        self.pupila = Pupila(self.cadru, limita)
