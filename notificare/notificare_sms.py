from twilio.rest import Client

class Notificare(object):
    
    #variabilele care vor tine datele de cont
    cont_sid = 'conti_sid'
    cont_token = 'cont_token'
    new_cont_sid = 'new_cont_sid'
    new_cont_token = 'new_cont_token'
    #test_cont_sid = ''
    #test_cont_token = ''
    mesaj = ''
    
    def __init__(self, mesaj):
        self.mesaj = mesaj
        
    def trimitere_notificare(self):
        client = Client(self.new_cont_sid, self.new_cont_token)
        
        sms_trimis = client.messages.create(
                                             #from_ ='number',
                                             from_='number',
                                             body = self.mesaj,
                                             to = 'number'
                                           )

        
        print('Notificare trimisa')


    def trimite_notificare_caz_nedetectare_miscare(self):
        client = Client(self.cont_sid, self.cont_token)
        
        sms_trimis = client.messages.create(
                                             #from_ ='+15139734159',
                                             from_='number',
                                             body = 'Tentativa frauda detectata - Imposibilitate detectare miscare',
                                             to = 'number'
                                           )

        
        print('Notificare trimisa - caz nedetectare miscare')
        
        
#notificare = Notificare("Tentativa frauda detectata")
#notificare.trimitere_notificare()
