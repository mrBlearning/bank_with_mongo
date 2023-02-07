# schimbati link-ul de conectare la baza de date (randul 10)

import json
import pymongo
from operatiuni import *
from input_utils import introdu_nume, introdu_numar
from IPython.display import clear_output
from admin_date import *

db_client = pymongo.MongoClient("link de conectare la mongoDB")

db = db_client["bankingDB"]
clients_collection = db["clients"]

while True:
    print("""
    Meniu:

    1. Creaza Client nou
    2. Afiseaza clientii (scrie filtru optional)
    3. Verifica soldul unui client
    4. Modifica soldul (depunere / retragere)
    5. Transfer intre clienti
    6. Genereaza extras de cont
    7. Sterge date client (inchidere cont)
    8. Clear screen
    9. Exit
    """)
    optiune = input('alege un numar din meniu: ')
    print()
    
    if optiune == '1':
        creaza_client(clients_collection)
        
    elif optiune == '2':
        print("""--------------------------------------------------------
Lista clientilor:
        """)
        clients_names = clients_collection.find({}, {"_id":0, "nume": 1})
        for name in clients_names:
            print(name["nume"])
        print('--------------------------------------------------------')

    elif optiune == '3':
        nume_client = introdu_nume('Numele clientului: ')
        if nume_client in dict_clients:
            print(f'Soldul pentru clientul "{nume_client}": {verifica_sold(nume_client, dict_clients)}')
        else:
            print('Client inexistent.')
        print()

    elif optiune == '4':
        nume_client = introdu_nume('Numele clientului: ')
        if nume_client in dict_clients:
            valoare = introdu_numar(f'Valoarea cu care se modifica soldul clientului "{nume_client}": ')
            if valoare > 0 or valoare < 0:
                print(f"Soldul initial al clientului {nume_client}: {verifica_sold(nume_client, dict_clients)}")
                modifica_sold(nume_client, valoare, dict_clients)
                print(f'Soldul final al clientului "{nume_client}": {verifica_sold(nume_client, dict_clients)}')
                log_depunere_retragere(nume_client, valoare, dict_tranzactii, dict_clients)
            else:
                print('0 nu este o suma valida pentru operatiune.')
        else:
            print('Client inexistent.')
        print()

    elif optiune == '5':
        valoare = introdu_numar('Valoarea transferului: ')
        nume_expeditor = introdu_nume('Numele clientului expeditor: ')
        nume_destinatar = introdu_nume('Numele clientului destinatar: ')
        transfer(valoare, nume_expeditor, nume_destinatar, dict_clients, dict_tranzactii)

    elif optiune == '6':
        """
        """
        nume_client = introdu_nume('Numele clientului: ')
        constructor_extras(nume_client, dict_tranzactii, dict_clients)

    elif optiune == '7':
        nume_client = introdu_nume('Numele clientului: ')
        sterge_client(nume_client, clients_collection)
        
    elif optiune == '8':
        clear_output(wait=True)
    
    elif optiune == '9' or optiune == 'exit':
        db_client.close()
        break
    
    elif optiune == '10':
        pass
