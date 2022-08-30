import cv2
from  urmarire_privire import Detectare, Tentativa_Frauda, Timp
from notificare import Notificare

privire = Detectare()
webcam = cv2.VideoCapture(1)

# obiectele de care ne vom folosi pentru a implementa logica de functionare a aplicatiei
interpretare_miscare = Tentativa_Frauda(contor=90)
timp = Timp()
notificare_noua = Notificare('Tentativa frauda detectata')

while True:
    # Primim un nou cadru de la camera
    _, cadru = webcam.read()

    # Trimitem acest cadru catre Detectare pentru analiza
    privire.reset(cadru)

    cadru = privire.cadru_adnotat()
    text = ""
    timp.incepe_masurare_timp()
    timp.determina_timp_trecut()

    if interpretare_miscare.imposibilitate_detectare_miscare():
        notificare_noua.trimite_notificare_caz_nedetectare_miscare()
        #print("Nu se poate detecta miscare")

    if privire.clipeste():
        
        text = "Clipeste"
        
    elif privire.este_la_dreapta():
        
        text = "Priveste dreapta"
        interpretare_miscare.numarare_miscare_ochi_dreapta()
        
        if interpretare_miscare.detectare_tentativa_frauda_faza1(timp.timp_trecut):
            notificare_noua.trimitere_notificare()
            print("Notificare trimisa f1")
            
        if interpretare_miscare.detectare_tentativa_frauda_faza2(timp.timp_trecut):
            notificare_noua.trimitere_notificare()
            print("Notificare trimisa f2")
            
        
    elif privire.este_la_stanga():
        
        text = "Priveste stanga"
        interpretare_miscare.numarare_miscare_ochi_stanga()

        if interpretare_miscare.detectare_tentativa_frauda_faza1(timp.timp_trecut):
            notificare_noua.trimitere_notificare()
            print("Notificare trimisa f1")
        
        if interpretare_miscare.detectare_tentativa_frauda_faza2(timp.timp_trecut):
            notificare_noua.trimitere_notificare()
            print("Notificare trimisa f2")
            
        
    elif privire.este_in_centru(): 
        text = "Priveste centru"
        interpretare_miscare.numarare_miscare_ochi_centru()
        
        if interpretare_miscare.detectare_tentativa_frauda_faza3(timp.timp_trecut):
            notificare_noua.trimitere_notificare()
            print("Notificare trimisa f3")

    cv2.putText(cadru, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
    cv2.imshow("Demo", cadru)

    if cv2.waitKey(1) == 27:
        break
   
webcam.release()
cv2.destroyAllWindows()
