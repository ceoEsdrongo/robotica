#codice rubato benvenuti nella sdrongo stalla
#Lideo Angelo - Businaro Giulia 4AI 2024/25 IIS EUGANEO ESTE
#progetto2-0924
#Consegna: creare uno script in micropy per la gestione del robot che garantisca la locomozione 
#di due servo continui FS90R.
#Il robot ha la missione di rilevare la temp media mediante sensore interno 
#Il robot inizia la sua missione dopo aver segnalato con una icona LED all'operatore umano 
#Se durante la sua missione il robot incontra ostacoli si ferma
#Se incontra altri ostacoli si comporta come in precedenza e per evitare lo stallo
#richiede l'intervento di un operatore mediante segnale visivo 



# Importazioni libere
from microbit import *
import music



# Funzioni

#Immagine Display iniziale
def Inizializza():
    display.clear()
    ImmagineAvvio = Image("00000:00000:00900:00000:00000")
    display.show(ImmagineAvvio)
    sleep(SOSPENSIONE_INIZIALE)


#Robot pronto a partire
def Pronto():
    ImmaginePronto = Image("09090:09090:09090:09090:09090")
    display.show(ImmaginePronto)
    PIN_LED_VERDE.write_digital(1)


#Controllo del contatto con un oggetto
def Controllo():
    sleep(TEMPO_CONTROLLO)
    if (PIN_SENSORE_CONTATTO.read_digital() == False):
        return True
    else:
        return False


#Avanzamento del robot
def MotoriAvanti(velocita):
    ImmagineAvanti = Image.ARROW_N
    display.show(ImmagineAvanti)
    motore_destro = 76 - 0.25 * velocita
    motore_sinistro = 76 + 0.25 * velocita
    PIN_MOTORE_DESTRO.write_analog(motore_destro)
    PIN_MOTORE_SINISTRO.write_analog(motore_sinistro)


#Indietreggiamento del robot
def MotoriIndietro(velocita):
    ImmagineIndietreggio = Image.ARROW_S
    display.show(ImmagineIndietreggio)
    motore_destro = 76 + 0.25 * velocita
    motore_sinistro = 76 - 0.25 * velocita
    PIN_MOTORE_DESTRO.write_analog(motore_destro)
    PIN_MOTORE_SINISTRO.write_analog(motore_sinistro)


#robot quando rileva un ostacolo
def OstacoloRilevato():
    MotoriFermi()
    ImmagineOstacolo = Image("00000:99999:99999:99999:00000")
    display.show(ImmagineOstacolo)
    sleep(TEMPO_OSTACOLO)
    MotoriIndietro(MAX_SPEED)
    sleep(TEMPO_SICUREZZA)
    MotoriFermi()
    display.show(ImmagineOstacolo)
    sleep(TEMPO_TAO)
    MotoriAvanti(MAX_SPEED / 100 * 30)
    sleep(TEMPO_SICUREZZA)
    temporimasto = TEMPO_SICUREZZA * 70 / 100
    MotoriAvanti(MAX_SPEED)
    sleep(int(temporimasto))


#Interruzzione della missione
def Stallo():
    ImmagineStallo = Image("00000:99999:00000:99999:00000")
    suono = music.BA_DING
    music.play(suono)
    PIN_LED_ROSSO.write_digital(1)
    display.show(ImmagineStallo)
    MotoriFermi()

#Posizione neutra dei motori
def MotoriFermi():
    PIN_MOTORE_DESTRO.write_analog(POSIZIONE_NEUTRA)
    PIN_MOTORE_SINISTRO.write_analog(POSIZIONE_NEUTRA)


# Parametri
SOSPENSIONE_INIZIALE = 5000  # Pausa iniziale

PERIODO_PWM = 29  # 50 Hz

TEMPO_MISSIONE = 10000  # Tempo dal punto A al punto B

POSIZIONE_NEUTRA = 76  # Posizione neutra di entrambi i motori

MAX_SPEED = 100  # Percentuale di velocità del motore

TEMPO_CONTROLLO = 200  # Millisecondi tra ogni controllo del sensore a infrarossi

TEMPERATURA_RIDUZIONE = 10  # Percentuale di temperatura da diminuire dal valore massimo

TEMPO_OSTACOLO = 5000  # Tempo di attesa del robot in caso ci sia la presenza di un ostacolo

TEMPO_SICUREZZA = 3000  # tempo durante il quale il robot si allontana dall'ostacolo

TEMPO_TAO = 2000  # Tempo di attesa prima di ripartire di nuovo

MAX_TENTATIVI = 5  # Numero massimo di operazioni in caso il robot trovi ostacoli


#Attributi PIN
PIN_MOTORE_DESTRO = pin2
PIN_MOTORE_SINISTRO = pin1
PIN_SENSORE_CONTATTO = pin16
PIN_LED_VERDE = pin8
PIN_LED_ROSSO = pin9

# Boolean
A_Premuto = False   #Bottone A premuto
B_Premuto = True    #Tasto B premuto
Ostacolo = False    #Ostacolo Rilevato




# Main del programma

#Preparativi per l'inizio missione
Inizializza()

PIN_SENSORE_CONTATTO.set_pull(PIN_SENSORE_CONTATTO.PULL_UP)  # Ingresso sia sempre presente un segnale certo
counter = 0
#Inizio della Missione
while True:

    while B_Premuto or counter != MAX_TENTATIVI:   #Viene eseguito finchè il B tasto B è stato premuto e il counter è diverso da 2

        counter = 0 #counter delle volte in cui il robot trova un ostacolo
        
        Pronto()    #Preparazione del robot

        if button_a.get_presses() and B_Premuto:    #Se il tasto A e anche il tasto B è premuto viene dato come valore a A = true e B = false

            PIN_LED_VERDE.write_digital(0)

            A_Premuto = True

            B_Premuto = False

        if A_Premuto and B_Premuto == False:    #Se il tasto A è premuto e il tasto B non viene premuto rileva la temperatura e comincia l'avanzamento del robot alla massima velocità 

            temperatura1 = temperature()

            MotoriAvanti(MAX_SPEED)

            for i in range(int(TEMPO_MISSIONE/1000* 5)): #For che esegue esattamente l'avanzamento con controlli per il  tempo missione

                Ostacolo = False
                
                Ostacolo = Controllo()

                if Ostacolo:

                    OstacoloRilevato()

                    counter += 1

                if counter == MAX_TENTATIVI:

                    break

            MotoriFermi()

            if counter != MAX_TENTATIVI:    #Finchè il counter non vale 5 mostra nel display la temperatura media del robot

                temperatura2 = temperature()

                media_temperature = (temperatura1 + temperatura2) / 2

                media_temperature_finale = media_temperature - media_temperature / TEMPERATURA_RIDUZIONE

                display.scroll("la temperatura media è: " + str(media_temperature_finale))

                B_Premuto = True

            else:   #Se il counter vale 5 verra eseguito uno stallo

                Stallo()
                
                while not B_Premuto: #Fase di stallo nella quale viene controllato se schiacciato il tasto B, quando viene schiacciato il tasto B uscirà da questa fase
                    
                    if button_b.get_presses():
                        PIN_LED_ROSSO.write_digital(0)
                        B_Premuto = True
                        


