import random
import pyqrcode
import PySimpleGUI as sg
import cv2
import os
from decimal import Decimal
# Implementare in python a algoritmului lui shamir de secret sharing,  varianta standard

# functia cu care voi calcula valoarea lui y
# y= polinom[0] + x*polinom[1] + x^2*polinom[2] + ...
marime_camp=2**11-1 # un nr prim marsenne foarte mare
def generare_a(Secretul, shares_necesare):
    A = []
    A.append(Secretul)
    for i in range(0, shares_necesare-1):
        A.append(random.randrange(1, marime_camp))
    return A

def generare_polinom_in_y(a, x):
        y = 0
        gradul_polinom = 1
        for coeficient in a:
            y = y + coeficient * gradul_polinom
            gradul_polinom = gradul_polinom * x
        return y

def shamir_share_generator (numar_shares, shares_necesare, Secretul,a):
    subsecretex = []
    subsecretey= []
    for i in range (0, numar_shares):
        X = random.randrange(1, marime_camp) % marime_camp
        Y = generare_polinom_in_y(a, X)
        subsecretex.append(X)
        subsecretey.append(Y)
    return subsecretex, subsecretey

def shamir_secret_retrieval(subsecretex, subsecretey):
    produsul = []
    suma = 0
    for i in range(len(subsecretex)):
        xi = subsecretex[i]
        yi = subsecretey[i]
        rezultat = Decimal(1)
        for j in range(len(subsecretey)):
            xj = subsecretex[j]
            if i != j:
                rezultat = rezultat * Decimal(Decimal(xj/(xj-xi)))
        rezultat = rezultat * yi
        suma = suma + Decimal(rezultat)
    return int(round(Decimal(suma), 0))



Secretul=25
numar_shares=4
shares_necesare=3
Secretul=Secretul % marime_camp
a = generare_a(Secretul, shares_necesare)
subsecretx, subsecrety = shamir_share_generator(numar_shares, shares_necesare, Secretul, a)
print("Share-urile generate")
for i in range(len(subsecrety)):
    print(subsecrety[i], subsecretx[i], "")
print(shamir_secret_retrieval(subsecretx, subsecrety))
#print(marime_camp)

QR_shares = []
def QR_creator(QR_shares):
    for i in range(numar_shares):
        h = subsecrety[i]
        QR_shares.append(pyqrcode.create(h))
        #print(QR_shares[i].terminal())
        j = i
        str(j)
        j = "share" + str(j)
        j = str(j) + ".png"
        QR_shares[i].png(j, scale=8)
QR_creator(QR_shares)

sg.theme('Dark Blue 3')
sg.SetOptions(background_color='#9FB8AD',
       text_element_background_color='#9FB8AD',
       element_background_color='#9FB8AD',
       #scrollbar_color=None,
       input_elements_background_color='#F7F3EC',
       #progress_meter_color = ('green', 'blue'),
       button_color=('white','#475841'))

layout = [
          [sg.Button('Trimite valori'), sg.Button('Exit')]], # butoanele necesare programului
for i in range(1,shares_necesare+1):
    layout += [sg.Text(f'{i}. '), sg.InputText( key=i)], # facem cate un rand pentru fiecare share necesar
for i in range (shares_necesare+1, 2*shares_necesare+1):
    layout += [sg.Text('Source for Files ', size=(15, 1)), sg.InputText(key=i), sg.FileBrowse()],
layout += [sg.Submit("Trimite fisierele")],
#layout+= []
window = sg.Window('Tester validitate', layout, size = (600, 600)) # titlul aplicatiei
Output_from_app = []
QR_path = []
while True:  # Event Loop
    event, values = window.read()
    #values_list = window.read()
    #print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel':
        break
    if event == 'Trimite valori': # daca apasam pe memorare, in variabila values se face update la valorile noi pe care le-am introdus
        #window['-OUTPUT-'].update(values['-IN-'])
        sg.SystemTray.notify('Tester validitate', 'Datele au fost salvate!')
    if event == 'Trimite fisierele':
        sg.SystemTray.notify('Tester validitate', 'Fisierele au fost trimise cu succes!')
        for i in range(shares_necesare+1, 2*shares_necesare+1):
            QR_path.append(values[i])

    #print(alx, ' ')
alx=0
check_input = []
for i in range(1, shares_necesare+1):
    print(values[i], ' ')
   # print(type(values[i]))
    a = values[i]
  #  print(type(a))
    if values[i]:
        a = int(a)
        check_input.append(a)
        alx += 1
    if type(a) == str:
        sg.SystemTray.notify('Tester validitate', 'String Introdus!')
        break
 #   print(type(a))
    #a = int(values[i])
    #print(a, " ??? ")
    #if type(a) == int:
        #alx += 1

#print(alx, "ALX")
if alx == shares_necesare:
        for j in range(0, shares_necesare):
            Output_from_app.append(check_input[j]) # introducem in alta variabila partile din secret introduse.

        for i in range (0, shares_necesare):
            #print(Output_from_app, " ")
            print(Output_from_app[i], "\n")
        window.close()
        print("Verificam validitatea shares introduse:\n")
        # print(QR_lista)
        ok = shares_necesare
        contor = 0
        x_polinom = []
        for i in range(0, shares_necesare):
            for j in range(0, numar_shares):
                # print(Output_from_app[i])
                # print(QR_lista[j][1])
                a = int(Output_from_app[i])
                b = int(subsecrety[j])
                if a == b:
                    contor = contor + 1
                    print(contor, " ")
                    x_polinom.append(subsecretx[j])
        # print(contor)
        if (contor != shares_necesare):
            print("Input gresit!\n")
            sg.SystemTray.notify('Tester validitate', 'Date incorecte!')

        else:
            print("OK")
            a = []
            b = []
            for i in range(0, shares_necesare):
                a.append(int(x_polinom[i]))
                b.append((int(Output_from_app[i])))
            for i in range(0, shares_necesare):
                print(a[i], " ", b[i], " ")
            rezultat = shamir_secret_retrieval(a, b)
            print("Secretul este: ")
            print(rezultat)
else:
    window.close()
    sg.SystemTray.notify('Tester validitate', 'Date incorecte!')
#print(QR_shares[1])
#print(type(QR_shares[1]))
#print(QR_shares[1].content)

#fil_path = QR_path[1]
eu = cv2.QRCodeDetector()
val, points, straight_qrcode = eu.detectAndDecode(cv2.imread("share0.png"))
#print (type(val), " ")
#qr_data = val.split(',')
#print(qr_data[0])
#incercare=int(qr_data[0])
#print(incercare)
#print(type(incercare))
QR_file_name= []
Ver = 0
for i in range(0, shares_necesare):
    QR_file_name.append(os.path.basename(QR_path[i]))
    #print(QR_file_name, "\n")
for i in range(0, shares_necesare):
    for j in range(0, numar_shares):
        if QR_file_name[i] =='share'+str(j)+'.png':
            Ver += 1
QR_valori = []
for i in range(0, shares_necesare):
        if(len(QR_file_name[i])>0):
            intermediar, points, straight_qrcode = eu.detectAndDecode(cv2.imread(QR_file_name[i]))
            qr_data = intermediar.split(',')
            #print(intermediar, " ")
            #intermediar = ''
        QR_valori.append(qr_data[0])
x1_polinom = []
if Ver == len(QR_valori):
    for i in range(0, Ver):
        QR_valori[i] = int(QR_valori[i])
        print(type(QR_valori[i]))
else:
    sg.SystemTray.notify('Tester validitate', 'Fisiere Invalide!')
x1_polinom = []
for i in range(0, shares_necesare):
    for j in range(0, numar_shares):
        # print(Output_from_app[i])
        # print(QR_lista[j][1])
        a = int(QR_valori[i])
        b = int(subsecretx[j])
        if a == b:
            x1_polinom.append(subsecretx[j])
    if len(x1_polinom) == len(QR_valori):
        print("DA")
        rezultat1 = shamir_secret_retrieval(x1_polinom, QR_valori)
        print("Secretul este: ")
        print(rezultat1)

