import numpy as np
import cv2


class Pupila(object):
    """
    Aceasta clasa detecteaza irisul si estimeaza pozitia pupilei
    """

    def __init__(self, rama_ochi, prag):
        self.rama_iris = None
        self.limita = prag
        self.x = None
        self.y = None

        self.detectare_iris(rama_ochi)

    @staticmethod
    def procesare_imagine(rama_ochi, prag):
        """
        Face operatii asupra ochiului pentru a izola irisul

        Argumente:
            rama_ochi: cadrul continand ochiul si nimic altceva
            prag: cadrul ochiului
            

        Returns:
            Un cadru reprezentand irisul
        """
        kernel = np.ones((3, 3), np.uint8)
        cadru_nou = cv2.bilateralFilter(rama_ochi, 10, 15, 15)
        cadru_nou = cv2.erode(cadru_nou, kernel, iterations=3)
        cadru_nou = cv2.threshold(cadru_nou, prag, 255, cv2.THRESH_BINARY)[1]

        return cadru_nou

    def detectare_iris(self, rama_ochi):
        """
        Detecteaza irisul si estimeaza pozitia irisului

        Arguments:
            rama_ochi: cadrul continand ochiul si nimic altceva
        """
        self.rama_iris = self.procesare_imagine(rama_ochi, self.limita)

        contururi, _ = cv2.findContours(self.rama_iris, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
        contururi = sorted(contururi, key=cv2.contourArea)

        try:
            momente = cv2.moments(contururi[-2])
            self.x = int(momente['m10'] / momente['m00'])
            self.y = int(momente['m01'] / momente['m00'])
        except (IndexError, ZeroDivisionError):
            pass
