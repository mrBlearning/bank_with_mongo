
from input_utils import *
import uuid, json
from admin_date import *
from elemente_extras import *

class Client:
    
    def __init__(self, nume, cnp, nr_telefon, adresa):
        self.nume = nume
        self.cnp = cnp
        self.nr_telefon = nr_telefon
        self.adresa = adresa
        self.balanta = 0
        self.tranzactii = []
        
        

    def __str__(self):

        return self.nume + str(self.balanta)

    def retragere(self , suma):

        if self.balanta < suma :
            print("n-ai bani")
            return

        self.balanta = self.balanta - suma
        self.tranzactii.append(Tranzactie("retragere" ,self, suma ))




    def depunere(self, suma):

        self.balanta = self.balanta + suma
        self.tranzactii.append(Tranzactie("depunere" ,self  , suma))

    def transfer(self, destinatar , suma):
        if self.balanta < suma:
            print("No money")
            return
        self.balanta = self.balanta - suma
        destinatar.balanta = destinatar.balanta + suma
        self.tranzactii.append(Tranzactie("transfer" , self,  suma , destinatar))

class Tranzactie:
    
    def __init__(self, tip_tranzactie ,expeditor, suma, destinatar = None):
        self.timestamp = transaction_timestamp()
        self.tip_tranzactie = tip_tranzactie
        self.expeditor = expeditor
        self.suma = suma
        self.destinatar = destinatar
        


    def __str__(self):
        if self.destinatar == None:

            return self.expeditor.nume + "|" +str(self.suma) + "|" + self.tip

        return self.expeditor.nume  + "|" + str(self.suma) + "|" + self.destinatar + "|" + self.tip


def creaza_client(clients_collection):
    """
    Functie care adauga in fisierul "clients.txt" un client, folosind datele de identificare introduse de la tastatura.
    :param dict_clients: dict Dictionarul care stocheaza in memorie datele despre clienti
    """
    # clients_collection = db["clients"]
    cnp = input('Intordu CNP: ')
    nume = introdu_nume('Numele noului client: ')
    telefon = input('Numar de telefon: ')
    adresa = input('Adresa: ')

    new_client = Client(nume, cnp, telefon, adresa)
    clients_collection.insert_one(new_client.__dict__)
    
    

def modifica_sold(client, valoare, dict_clients):
    """
    Functie care modifica soldul unui cont
    :param nume_client: text Numele clientului al carui sold trebuie modificat
    :param valoare: float Valoare cu care soldul va fi modificat. Poate fi pozitiva sau negativa.
    :return sold: float Soldul dupa ce a fost facuta mofidicarea
    """
    if valoare < 0:
        if abs(valoare) < dict_clients[nume_client]['sold']:
            client.retragere(valoare)
            rescrie_fisier_clienti(dict_clients)
        else:
            print('Sold insuficient pentru tranzactia dorita.')
    else:
        if valoare > 0:
            client.depunere(valoare)
    

def transfer(valoare, expeditor ,destinatar, dict_clients, dict_tranzactii):
    # implementeaza logica pentru situatia "fonduri insuficiente"
    """
    Functie care face transferul unei sume de bani intre 2 conturi, cu conditia ca expeditorul sa dispuna de valoare care trebuie transferata
    :param valoare: float Valoare care urmeaza sa fie transferata
    :param nume_expeditor: str Numele expeditorului
    :param nume_destinatar: str Numele destinatarului
    :param dict_clients: dict Dictionarul care stocheaza in memorie datele despre clienti
    """
    if valoare <= 0:
        print('Valoarea transferata trebuie sa fie pozitiva. Transferul nu a fost efectuat.')
    else:
        if expeditor.balanta >= valoare:
            print(f"Soldul initial al clientului {expeditor.name}: {expeditor.balanta}")
            print(f"Soldul initial al clientului {destinatar.name}: {destinatar.balanta}")
            expeditor.transfer(destinatar, valoare)
            print(f"Soldul final al clientului {expeditor.name}: {expeditor.balanta}")
            print(f"Soldul final al clientului {destinatar.name}: {destinatar.balanta}")
        else:
            print('Expeditorul nu are fonduri suficiente. Transferul nu a fost efectuat.')
    

def sterge_client(nume_client, clients_collection):
    print(nume_client)
    clients_collection.delete_one({"nume": nume_client})
    # sold = verifica_sold(nume_client, dict_clients)
    # if sold < 0:
    #     print(f'Pentru inchiderea contului este necesara achitarea sumei restante de: {sold}.')
    # elif sold > 0:
    #     print(f'Contul figureaza cu o sold de {sold}, care va fi restituita clientului.')
    # else:
    #     print(f'Soldul este 0. Contul va fi sters, impreuna cu informatiile despre client.')


def constructor_extras(client, dict_clients):
    tranzactii, perioada = tranzactii_in_perioada(client)
    nume_nr_strada = ['Numele_strazii', '13']
    numarul_contului = 'numarul_contului'
    tip_cont = 'tipul_contului'
    moneda = 'RON'
    cod_client = 'codul_clientului'
    spatii_dupa_nume = pozitie_coloana2_date_client - 1 - len(nume_client)
    spatii_dupa_oras = pozitie_coloana2_date_client - 1 - len(dict_clients[nume_client]['oras'])
    
    print('\n\n')
    print(rand_1)
    print(f"{' '*79}{perioada[0]}-{perioada[1]}")
    print('_'*lungime_rand)
    print(f"{nume_client}{' '*spatii_dupa_nume}Tip Cont:       {tip_cont}")
    print(f"str. {nume_nr_strada[0]}, Nr. {nume_nr_strada[1]}                            Numar cont:     {numarul_contului}")
    print(f"{dict_clients[nume_client]['oras']}{' '*spatii_dupa_oras}Moneda:         {moneda}")
    print(f"{' '*(pozitie_coloana2_date_client-1)}Cod client:     {cod_client}\n")
    print('_'*lungime_rand)
    print(cap_tabel)
    print('_'*lungime_rand)
    print()
    for tranzactie in tranzactii:
        data_formatata = formatere_data_extras_cont(tranzactie.timestamp)
        if  tranzactie.suma < 0:
            pozitie_sfarsit = pozitie_sfarsit_debit
        else:
            pozitie_sfarsit = 100
        spatii_inainte_de_tranzactie = pozitie_detalii_cap_tabel - 2 - len(data_formatata)
        spatii_dupa_tranzactie = pozitie_sfarsit - len(str(tranzactie.suma)) - len(tranzactie.tip_tranzactie) - spatii_inainte_de_tranzactie - len(data_formatata) + 1
        spatii_detalii = pozitie_detalii_cap_tabel - 1
        print(f"{data_formatata}{' '*spatii_inainte_de_tranzactie}{tranzactie.tip_tranzactie}{' '*spatii_dupa_tranzactie}{abs(tranzactie.suma)}")
        for detaliu in tranzactie[1].items():
            if detaliu[0] != 'tip_tranzactie':
                print(f"{' '*spatii_detalii}{detaliu[0]}: {detaliu[1]}")
        print()
    
    print("""
 
MBBank
____________________________________________________________________________________________________

Andrada Perlea             Semnatura                             Mirela Ilie            Semnatura

Sef Serviciu Dezvoltare Produse                                  Sef Serviciu Relatii Clienti
MBBank                                                           MBBank
Sucursala Bucuresti  



"""
         )
    
