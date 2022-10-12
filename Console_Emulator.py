import zipfile


# Функция для реализации комманды cd
def CD(address, pWay, allFiles):
    # если на вход идет командя перейти к корню
    if address == "~":
        return ""
    # если на вход идет команда поднятся по директории на 1 уровень
    elif address == ".." or address == "-":
        if address == '':
            return pWay
        else:
            pWay = "/" + pWay
            k = len(pWay) - 1
            while pWay[k] != "/":
                pWay = pWay[:-1]
                k -= 1
            pWay = pWay[:-1]
            pWay = pWay[1:]
            return pWay
    # если на вход идет переход к директории с полным адресом
    elif pWay + '/' + address + '/' in allFiles:
        return pWay + '/' + address
    # если на вход идет адрес с названием /root
    elif "/root/" in address:
        addres = address.replace("/root/", '')
        if addres in allFiles:
            return addres
        return "sh: cd: can't cd to " + addres + ". No such file or directory"
    # если на вход идет переход к папке внутри текущей директории
    elif pWay == '' and (address + '/') in allFiles:
        return address
    else:
        return "sh: cd: can't cd to " + address + ". No such file or directory"


# Функция для передвижения по директории
def checkFile(address, pWay, allFiles):
    if "/root" in address:
        address = address.replace("/root/", '')
        if address in allFiles:
            return address
        return "cat: can't open" + address + ". No such file or directory"
    elif pWay + '/' + address in allFiles:
        return pWay + '/' + address
    else:
        return "cat: can't open" + address + ". No such file or directory"


# Функция для реализации комманды ls
def LS(wayL, allFiles):
    count = wayL.count('/')
    wayL += '/'
    # Проверка файлов внутри архива
    for i in allFiles:
        if wayL == '/':
            if wayL in i and i != wayL:
                if count == (i.count('/')):
                    if i[-1] != '/':
                        print(i, end="    ")
                    else:
                        print(i[:-1], end="    ")
                elif count == (i.count('/') - 1) and (i[-1] == '/'):
                    print(i[:-1], end="    ")
        else:
            if wayL in i and i != wayL:
                if count == (i.count('/') - 1):
                    if i[-1] != '/':
                        print(i, end="    ")
                    else:
                        print(i[:-1], end="    ")
                elif count == (i.count('/') - 2) and (i[-1] == '/'):
                    print(i[:-1], end="    ")


# Функция для реализации комманды cat
def CAT(out, Archive):
    with zipfile.ZipFile(Archive) as myzip:
        with myzip.open(out, 'r') as myfile:
            # декодирование в текст
            lines = [x.decode('utf8').strip() for x in myfile.readlines()]
            for line in lines:
                print(line)


# Функция для реализации комманды pwd
def PWD(way):
    if way == "":
        print("/root")
    else:
        print("/root/" + way + "/")


def main():
    # Выбор архива на работу (сделал 2 заготовленных)
    print("Перед началом работы эмулятора, выберете с каким архивом работать.")
    print("Напишите 1 или 2")
    a = ''
    archive_number = input()
    while archive_number != '1' or archive_number != '2':
        if archive_number == '1':
            a = 'Archive_1.zip'
            break
        elif archive_number == '2':
            a = 'Archive_2.zip'
            break
        else:
            print('Вы набрали что-то не то. Попробуйте еще раз')
            archive_number = input()
    # переменная выбранного архива
    z = zipfile.ZipFile(a, 'r')
    # Возвращает элементы архива
    allFiles = (z.namelist())
    print(allFiles)
    # Изначальный путь
    EnterWay = '/root> '
    # путь корня-константа для дальнейшей работы
    ConstWay = 'root/'
    way = ''
    pWay = ""
    command = input(EnterWay)
    # работа пока не будет запрошена комманда завершения
    while command != "exit":
        command = command.split(" ")
        if command[0] == "pwd":
            PWD(pWay)
        elif command[0] == "ls":
            pWay_1 = pWay
            LS(pWay_1, allFiles)
            print()
        elif command[0] == "cd":
            if len(command) == 2:
                result = CD(command[1], pWay, allFiles)
                if "can't cd to " in result:
                    pass
                    print(result)
                else:
                    pWay = result
            else:
                PWD(pWay)
        elif command[0] == "cat":
            out = checkFile(command[1], pWay, allFiles)
            if "cat: can't open" in out:
                print(out)
            else:
                CAT(out, a)
        else:
            print("sh: " + command[0] + " not found")
        command = input(ConstWay + pWay + "> ")
    return


main()
