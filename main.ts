radio.setGroup(58)
let stav = 0
//  stav 0 je klient, stav 1 je server
let volba = 0
//  volba klienta
let hlasovani = false
//  stav, jestli je zapnuto hlasovani od serveru
let vlastni_ser_cislo = control.deviceSerialNumber()
let hlasy : number[][] = []
radio.setTransmitSerialNumber(true)
basic.showString(String.fromCharCode(volba + 65))
let pocet_hlasu : number[] = []
pocet_hlasu = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
function reset_promennych() {
    // resetuje promenne
    
    volba = 0
    hlasovani = false
    hlasy = []
    let pocet_hlasu = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}

radio.onReceivedValue(function on_received_value(name: string, value: number) {
    let hlas: number[];
    
    let ser_cislo = radio.receivedPacket(RadioPacketProperty.SerialNumber)
    if (stav == 1 && name == "answer" && hlasovani) {
        //  kdyz je stav nastaven na server a hlasovani je zapnuto
        hlas = [ser_cislo, value]
        // zpracovani hlasu
        hlasy.push(hlas)
        // pushnuti hlasu do listu s hlasy
        radio.sendValue("ano", ser_cislo)
        // posle potvrzeni o prijmuti (name = "ano")
        basic.showIcon(IconNames.Heart)
        basic.clearScreen()
    } else if (stav == 1 && name == "answer") {
        // kdyz je stav nastaven na server a hlasovani vypnuto
        radio.sendValue("ne", ser_cislo)
    } else if (stav == 0 && name == "ano") {
        // posle potvrzeni o neprijmuti (name = "ne")
        // kdyz je stav nastaven na klienta a potvrzene prijmuti
        if (value == vlastni_ser_cislo) {
            // kdyz se shoduje prijmute ser. cislo s vlastnim ser. cislem
            basic.showIcon(IconNames.Yes)
            basic.clearScreen()
        }
        
    } else if (stav == 0 && name == "ne") {
        // kdyz je stav nastaven na klienta a potvrzene neprijmuti
        if (value == vlastni_ser_cislo) {
            // kdyz se shoduje prijmute ser. cislo s vlastnim ser. cislem
            basic.showIcon(IconNames.No)
            basic.clearScreen()
        }
        
    }
    
})
function vyhodnoceni_hlasu() {
    
    hlasy.reverse()
    // reversne list s hlasy, aby zaznamenal jen ty posledni hlasy
    let list_ser_cisel : number[] = []
    //  list s dosud zaznamenanymi seriovymi cisly
    for (let list_s_hlasem of hlasy) {
        if (list_ser_cisel.indexOf(list_s_hlasem[0]) < 0) {
            list_ser_cisel.push(list_s_hlasem[0])
            pocet_hlasu[list_s_hlasem[1]] += 1
        }
        
    }
    let pozice_hlasu = 0
    for (let i of pocet_hlasu) {
        if (i > 0) {
            basic.showString(String.fromCharCode(pozice_hlasu + 65))
            basic.showNumber(i)
        }
        
        pozice_hlasu += 1
    }
    // print(pocet_hlasu)
    reset_promennych()
}

input.onLogoEvent(TouchButtonEvent.Pressed, function on_logo_event_pressed() {
    // kdyz je stav nastaven na klienta, odesle volbu (0 az 25)
    
    if (stav == 0) {
        radio.sendValue("answer", volba)
    }
    
})
basic.forever(function on_forever() {
    
    if (input.buttonIsPressed(Button.A)) {
        if (stav == 0) {
            //  kdyz je stav nastaven na klenta, zvysi volbu o 1
            volba += 1
            volba = Math.constrain(volba, 0, 25)
            basic.showString(String.fromCharCode(volba + 65))
        } else {
            if (hlasovani) {
                // kdyz je stav nastaven na server a hlasovani je zapnute, vypne hlasovani
                hlasovani = false
                basic.showIcon(IconNames.No)
                vyhodnoceni_hlasu()
            } else {
                hlasovani = true
                // kdyz je stav nastaven na server a hlasovani vypnute, zapne hlasovani
                basic.showIcon(IconNames.Yes)
            }
            
            basic.clearScreen()
        }
        
    }
    
    if (input.buttonIsPressed(Button.B) && stav == 0) {
        //  kdyz je stav nastaven na klenta, snizi volbu o 1
        volba -= 1
        volba = Math.constrain(volba, 0, 25)
        basic.showString(String.fromCharCode(volba + 65))
    }
    
    if (input.pinIsPressed(TouchPin.P0)) {
        // meni stav z klienta na server a naopak
        if (stav == 0) {
            stav = 1
        } else {
            stav = 0
        }
        
        basic.showNumber(stav)
        basic.clearScreen()
    }
    
})
