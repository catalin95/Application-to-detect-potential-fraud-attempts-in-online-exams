from twilio.rest import Client

class Notificare(object):
    
    #variabilele care vor tine datele de cont
    cont_sid = 'ACe52f3238b49c33adad91beeb9eac7a19'
    cont_token = '7c0934e86b85d5f01c219a9afb5bfc47'
    new_cont_sid = 'ACecc04998179bde8efe8995d94a5dd5a7'
    new_cont_token = 'c6ac7755ac3d382208b951b6c01458b8'
    #test_cont_sid = 'ACf3aff70e6130995922ede5e9a3bb790e'
    #test_cont_token = '1bcb9473f9d858c53e2e099e9e27efeb'
    mesaj = ''
    
    def __init__(self, mesaj):
        self.mesaj = mesaj
        
    def trimitere_notificare(self):
        client = Client(self.new_cont_sid, self.new_cont_token)
        
        sms_trimis = client.messages.create(
                                             #from_ ='+15139734159',
                                             from_='+19854972850',
                                             body = self.mesaj,
                                             to = '+40785628812'
                                           )

        
        print('Notificare trimisa')


    def trimite_notificare_caz_nedetectare_miscare(self):
        client = Client(self.cont_sid, self.cont_token)
        
        sms_trimis = client.messages.create(
                                             #from_ ='+15139734159',
                                             from_='+19854972850',
                                             body = 'Tentativa frauda detectata - Imposibilitate detectare miscare',
                                             to = '+40785628812'
                                           )

        
        print('Notificare trimisa - caz nedetectare miscare')
        
        
#notificare = Notificare("Tentativa frauda detectata")
#notificare.trimitere_notificare()