radio.set_group(58)
radio.set_transmit_serial_number(True)
vlastni_ser_cislo = control.device_serial_number()

stav = 0 # stav 0 je klient, stav 1 je server
volba = 0 # volba klienta
hlasovani = False # stav, jestli je zapnuto hlasovani od serveru
hlasy: List[List[number]] = [] # list hlasu se seriovymi cisly
pocet_hlasu: List[number] = [] # list originalnich hlasu bez seriovych cisel

basic.show_string(String.from_char_code(volba+65))

pocet_hlasu = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def reset_promennych(): #resetuje promenne
    global stav, volba, hlasovani, hlasy
    volba = 0
    hlasovani = False
    hlasy = []
    pocet_hlasu = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def on_received_value(name, value):
    global stav, hlasy, hlasovani, vlastni_ser_cislo
    ser_cislo = radio.received_packet(RadioPacketProperty.SERIAL_NUMBER)

    if stav == 1 and name == "answer" and hlasovani: # kdyz je stav nastaven na server a hlasovani je zapnuto
        hlas = [ser_cislo, value] #zpracovani hlasu
        hlasy.push(hlas) #pushnuti hlasu do listu s hlasy
        radio.send_value("ano", ser_cislo) #posle potvrzeni o prijmuti (name = "ano")
        basic.show_icon(IconNames.HEART)
        basic.clear_screen()

    elif stav == 1 and name == "answer": #kdyz je stav nastaven na server a hlasovani vypnuto
        radio.send_value("ne", ser_cislo) #posle potvrzeni o neprijmuti (name = "ne")


    elif stav == 0 and name == "ano": #kdyz je stav nastaven na klienta a potvrzene prijmuti
        if value == vlastni_ser_cislo: #kdyz se shoduje prijmute ser. cislo s vlastnim ser. cislem
            basic.show_icon(IconNames.YES)
            basic.show_string(String.from_char_code(volba+65))

    elif stav == 0 and name == "ne": #kdyz je stav nastaven na klienta a potvrzene neprijmuti
        if value == vlastni_ser_cislo: #kdyz se shoduje prijmute ser. cislo s vlastnim ser. cislem
            basic.show_icon(IconNames.NO)
            basic.show_string(String.from_char_code(volba+65))
radio.on_received_value(on_received_value)


def vyhodnoceni_hlasu():
    global hlasy, pocet_hlasu
    hlasy.reverse() #otoci list s hlasy, aby zaznamenal jen ty posledni hlasy
    list_ser_cisel: List[number] = [] #list s dosud zaznamenanymi seriovymi cisly

    for list_s_hlasem in hlasy: #projde hlasy a vybere jen ty posledni od kazdeho klienta (serioveho cisla)
        if list_s_hlasem[0] not in list_ser_cisel:
            list_ser_cisel.push(list_s_hlasem[0])
            pocet_hlasu[list_s_hlasem[1]] += 1 #do listu pocet_hlasu uklada pocet originalnich hlasu od kazde moznosti
    
    pozice_hlasu = 0

    for i in pocet_hlasu:
        print(i)

        if i > 0:
            basic.show_string(String.from_char_code(pozice_hlasu+65)) #zobrazi aspon jednoukrat objevenou moznost (A az Z)
            basic.show_number(i) #zobrazi od kazde objevene moznosti jeji pocet
        pozice_hlasu += 1

    reset_promennych()


def on_logo_event_pressed(): #kdyz je stav nastaven na klienta, odesle volbu (0 az 25)
    global stav, volba
    if stav == 0: 
        radio.send_value("answer", volba)

input.on_logo_event(TouchButtonEvent.PRESSED, on_logo_event_pressed)


def on_forever():
    global volba, hlasovani, stav
    #volba = 0
    if input.button_is_pressed(Button.A): 
        if stav == 0: # kdyz je stav nastaven na klenta, zvysi volbu o 1
            volba += 1
            volba = Math.constrain(volba, 0, 25)
            basic.show_string(String.from_char_code(volba+65), 40)
        else:
            if hlasovani: #kdyz je stav nastaven na server a hlasovani je zapnute, vypne hlasovani
                hlasovani = False
                basic.show_icon(IconNames.NO)
                vyhodnoceni_hlasu()
            else:
                hlasovani = True #kdyz je stav nastaven na server a hlasovani vypnute, zapne hlasovani
                basic.show_icon(IconNames.YES)
            basic.clear_screen()
            
    if input.button_is_pressed(Button.B) and stav == 0: # kdyz je stav nastaven na klenta, snizi volbu o 1
        volba -= 1
        volba = Math.constrain(volba, 0, 25)
        basic.show_string(String.from_char_code(volba+65), 40)

    if input.pin_is_pressed(TouchPin.P0): #meni stav z klienta na server a naopak
        if stav == 0:
            stav = 1
        else:
            stav = 0
        basic.show_number(stav)
        basic.clear_screen()
basic.forever(on_forever)
