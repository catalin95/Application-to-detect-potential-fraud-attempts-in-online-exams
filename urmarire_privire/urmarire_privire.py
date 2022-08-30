from __future__ import division
import os
import cv2
import dlib

from urmarire_privire import pupila
from .ochi import Ochi
from .calibrare import Calibrare


class Detectare(object):
    # Ne returneaza informatii importante cum ar fi pozitia ochilor si a pupilelor si ne permite sa vedem daca ochii sunt inchisi sau deschisi

    def __init__(self):
        self.cadru = None
        self.ochi_stang = None
        self.ochi_drept = None
        self.calibrare = Calibrare()

        # _folost pentru a detecta fata
        self._face_detector = dlib.get_frontal_face_detector()

        
        # folosim acest model pentru a obtine reperele faciale
        cwd = os.path.abspath(os.path.dirname(__file__))
        #model_path = os.path.abspath(os.path.join(cwd, "trained_models/shape_predictor_68_face_landmarks.dat"))
        model_path = os.path.abspath(os.path.join(cwd, "modele/prezicator.dat"))
        self._predictor = dlib.shape_predictor(model_path)

    @property
    def locatie_pupile(self):
        #Verifica daca pupilele au fost localizate
        
        try:
            int(self.ochi_stang.pupila.x)
            int(self.ochi_stang.pupila.y)
            int(self.ochi_drept.pupila.x)
            int(self.ochi_drept.pupila.y)
            return True
        except Exception:
            return False

    def _analizeaza(self):
        #Detecteaza fata si intializeaza obiectul ochi
        
        cadru = cv2.cvtColor(self.cadru, cv2.COLOR_BGR2GRAY)
        faces = self._face_detector(cadru)

        try:
            repere = self._predictor(cadru, faces[0])
            self.ochi_stang = Ochi(cadru, repere, 0, self.calibrare)
            self.ochi_drept = Ochi(cadru, repere, 1, self.calibrare)

        except IndexError:
            self.ochi_stang = None
            self.ochi_drept = None

    def reset(self, cadru):
        """
        Reseteaza cadrul si il analizeaza

        Argumente:
            cadru: cadrul pentru a fi analizat
        """
        self.cadru = cadru
        self._analizeaza()

    def coordonate_pupila_stanga(self):
        #Returneaza coordonatele pupilei stanga
        
        if self.locatie_pupile:
            x = self.ochi_stang.origine[0] + self.ochi_stang.pupila.x
            y = self.ochi_stang.origine[1] + self.ochi_stang.pupila.y
            return (x, y)

    def coordonate_pupila_dreapta(self):
        #Returneaza coordonatele pupilei dreapta
        
        if self.locatie_pupile:
            x = self.ochi_drept.origine[0] + self.ochi_drept.pupila.x
            y = self.ochi_drept.origine[1] + self.ochi_drept.pupila.y
            return (x, y)

    def raport_orizontal(self):
        """
        Returneaza un numar intre 0.0 si 1.0 care indica directia orizontala a privirii.
        Extrema dreapta este 0.0. centrul este 0.5 si extrema stanga este 1.0
        """
        if self.locatie_pupile:
            pupila_stanga = self.ochi_stang.pupila.x / (self.ochi_stang.centru[0] * 2 - 5)  #- 10
            pupila_dreapta = self.ochi_drept.pupila.x / (self.ochi_drept.centru[0] * 2 - 5)   #- 10
            return (pupila_stanga + pupila_dreapta) / 2

    def raport_vertical(self):
        """
        Returneaza un numar intre 0.0 si 1.0 care indica directia verticala a privirii.
        Extrema de sus este 0.0, centrul este 0.5 si extrema de jos este 1.0
        """
        if self.locatie_pupile:
            pupila_stanga = self.ochi_stang.pupila.y / (self.ochi_stang.centru[1] * 2 - 5)
            pupila_dreapta = self.ochi_drept.pupila.y / (self.ochi_drept.centru[1] * 2 - 5)
            return (pupila_stanga + pupila_dreapta) / 2

    def este_la_dreapta(self):
        #Returneaza true daca userul se uita la dreapta
        
        if self.locatie_pupile:
            return self.raport_orizontal() <= 0.50#0.35

    def este_la_stanga(self):
        #Returneaza true daca userul se uita la stanga
        
        if self.locatie_pupile:
            return self.raport_orizontal() >= 0.65

    def este_in_centru(self):
        # Returneaza true daca userul se uita in centru
        
        if self.locatie_pupile:
            return self.este_la_dreapta() is not True and self.este_la_stanga() is not True

    def clipeste(self):
        # Returneaza true daca userul isi inchide ochii
        
        if self.locatie_pupile:
            ratie_clipire = (self.ochi_stang.blinking + self.ochi_drept.blinking) / 2
            return ratie_clipire > 3.8

    def cadru_adnotat(self):
        # Returneaza cadrul principal cu pupilele evidentiate
        
        cadru = self.cadru.copy()

        if self.locatie_pupile:
            color = (0, 255, 0)
            x_left, y_left = self.coordonate_pupila_stanga()
            x_right, y_right = self.coordonate_pupila_dreapta()
            cv2.line(cadru, (x_left - 5, y_left), (x_left + 5, y_left), color)
            cv2.line(cadru, (x_left, y_left - 5), (x_left, y_left + 5), color)
            cv2.line(cadru, (x_right - 5, y_right), (x_right + 5, y_right), color)
            cv2.line(cadru, (x_right, y_right - 5), (x_right, y_right + 5), color)

        return cadru
