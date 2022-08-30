import time

class Timp(object):
    start_time = time.time()
    end_time = 0
    timp_trecut = 0
    
    def __init__(self):
        pass
    
    def incepe_masurare_timp(self):
        self.end_time = time.time()
       

    def determina_timp_trecut(self):
        self.timp_trecut = self.end_time - self.start_time
        
        
class Log(object):
    
    file = None
    
    def __init__(self):
        pass
    
    def creare_log(self):
        self.file = open("Log.txt", 'a')
        
    def incepe_logare(self, pozitie, contor):
        self.file.write(f"Contor {pozitie}: {contor}\n")
        
    def inchidere_log(self):
        self.file.close()
       
        
        
class Tentativa_Frauda(object):
    
    contor_pozitie_ochi_stanga = 0
    contor_pozitie_ochi_dreapta = 0
    contor_pozitie_ochi_centru = 0
    contor_imposibilitate_detectare_miscare = 0
    contor = 0
    trimis_f1 = False
    trimis_f2 = False
    trimis_f3 = False
    faza1 = False
    faza2 = False
    faza3 = False
    
    def __init__(self, faza1 = True, faza2 = True, faza3 = True, contor = 180):
        self.contor = contor
        self.faza1 = faza1
        self.faza2 = faza2
        self.faza3 = faza3
    
    def numarare_miscare_ochi_stanga(self):
        self.contor_pozitie_ochi_stanga += 1
        log_nou = Log()
        log_nou.creare_log()
        log_nou.incepe_logare("stanga", self.contor_pozitie_ochi_stanga)
        log_nou.inchidere_log()
        
    def numarare_miscare_ochi_dreapta(self):
        self.contor_pozitie_ochi_dreapta += 1
        log_nou = Log()
        log_nou.creare_log()
        log_nou.incepe_logare("dreapta", self.contor_pozitie_ochi_dreapta)
        log_nou.inchidere_log()
        
    def numarare_miscare_ochi_centru(self):
        self.contor_pozitie_ochi_centru += 1
        log_nou = Log()
        log_nou.creare_log()
        log_nou.incepe_logare("centru", self.contor_pozitie_ochi_centru)
        log_nou.inchidere_log()
        
        
    def detectare_tentativa_frauda_faza1(self, timp_trecut):    
        if self.faza1:        
            if self.contor_pozitie_ochi_dreapta > (5 * self.contor_pozitie_ochi_stanga) and (timp_trecut > self.contor) and not self.trimis_f1:   
                self.trimis_f1 = True
                return self.trimis_f1
            
            elif self.contor_pozitie_ochi_stanga > (5 * self.contor_pozitie_ochi_dreapta) and (timp_trecut > self.contor) and not self.trimis_f1:
                self.trimis_f1 = True
                return self.trimis_f1
            
            else:
                return False
            
    def detectare_tentativa_frauda_faza2(self, timp_trecut):
        if self.faza2:  
            if self.contor_pozitie_ochi_dreapta > (12 * self.contor_pozitie_ochi_stanga) and (timp_trecut > 2 * self.contor) and not self.trimis_f2:   
                self.trimis_f2 = True 
                return self.trimis_f2
            
            elif self.contor_pozitie_ochi_stanga > (12 * self.contor_pozitie_ochi_dreapta) and (timp_trecut > 2 * self.contor) and not self.trimis_f2:
                self.trimis_f2 = True
                return self.trimis_f2
            
            else:
                return False
        
    def detectare_tentativa_frauda_faza3(self, timp_trecut):
        if self.faza3:
            if self.contor_pozitie_ochi_centru > (12 * self.contor_pozitie_ochi_stanga) and (timp_trecut > self.contor) and not self.trimis_f3:
                self.trimis_f3 = True
                return self.trimis_f3
            
            elif self.contor_pozitie_ochi_centru > (12 * self.contor_pozitie_ochi_dreapta) and (timp_trecut > self.contor) and not self.trimis_f3:
                self.trimis_f3 = True
                return self.trimis_f3
            
            else:
                return False
        

    def imposibilitate_detectare_miscare(self):
        self.contor_imposibilitate_detectare_miscare += 1
        if self.contor_imposibilitate_detectare_miscare == 1200 and self.contor_pozitie_ochi_centru == 0 and self.contor_pozitie_ochi_dreapta == 0 and self.contor_pozitie_ochi_dreapta == 0:
            return True
        else:
            return False