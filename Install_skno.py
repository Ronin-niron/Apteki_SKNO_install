#!/usr/bin/env python3

import datetime
import os
import shutil
import subprocess
import zipfile
import sys

#Переменные
filename = ''
epson = "/dev/prepson"
oki = "/dev/printer"
rmCom = 'rm /home/cashier/.wine/dosdevices/com2'
rmLpt = 'rm /home/cashier/.wine/dosdevices/lpt1'
lnLpt = 'ln -s /dev/prepson ~/.wine/dosdevices/lpt1'
lnCom = 'ln -s /dev/prepson ~/.wine/dosdevices/com2'
fm1402 = 'wine /home/cashier/.wine/drive_c/FM1402/psFMUTools.exe'
Coupon = '/home/cashier/.wine/drive_c/PSTrade/Coupon0.txt'
mvCoupon = 'mv /home/cashier/.wine/drive_c/PSTrade/Coupon0.txt /home/cashier/.wine/drive_c/windows/system32/'
rmfm1402 = 'rm -r /home/cashier/.wine/drive_c/FM1402'
rmfiles = "rm -f /home/cashier/.wine/drive_c/PSTrade/*"
rmDB = 'rm -r /home/cashier/.wine/drive_c/PSTrade/DB'
rmReports = 'rm -r /home/cashier/.wine/drive_c/windows/system32/Reports*'
RM_AdmFrame='rm /home/cashier/.wine/drive_c/windows/system32/AdmFrame*'
RM_borlndmm='rm /home/cashier/.wine/drive_c/windows/system32/borlndmm*'
RM_Discount='rm /home/cashier/.wine/drive_c/windows/system32/Discount*'
RM_Weights='rm /home/cashier/.wine/drive_c/windows/system32/Weights*'
RM_PumpDLL='rm /home/cashier/.wine/drive_c/windows/system32/PumpDLL*'
RM_PsBackOffice='rm /home/cashier/.wine/drive_c/windows/system32/PsBackOffice*'
RM_LOG = 'rm -r /home/cashier/.wine/drive_c/PSTrade/LOG'
scview = 'wine /home/cashier/.wine/drive_c/Program\ Files/Sybase/Sybase\ Central/win32/scview.exe'
log_file = os.getcwd() + '/log'
cashmain_notepad = 'wine notepad.exe CashMain.ini'
#папка с торговой программой PSTrade
PSTrade='/home/cashier/.wine/drive_c/PSTrade'
#папка  файлов фискалки
FM1402='/home/cashier/.wine/drive_c/FM1402'
#папка дисконтных карт
DISCOUNT_Folder='/home/cashier/.wine/drive_c/DiscountCard'
#Cashmain.ini файл настроек торговли
Cashmain_ini='/home/cashier/.wine/drive_c/windows/CashMain.ini'
#Cash.ini файл настрое пользователя и окон торговли
Cash_ini='/home/cashier/.wine/drive_c/windows/Cash.ini'
#папка с сертификатами VPN
VPN='/etc/openvpn'
#файл с настройками навесного оборудования
Devices='/etc/udev/rules.d/99-usb-serial.rules'
#Reports из System32
Reports='/home/cashier/.wine/drive_c/windows/PSTrade/Reports'
#Берем текущуюю дату
GetDate=datetime.datetime.now().strftime("%d-%m-%Y-(%H-%M-%S)")
#имя Бэкапа
Name_BackUP='Auto-BackUP'
#папка для бэкап-файлов
Dir_BackUP='%s-%s' % (Name_BackUP, GetDate)
#папка для BackUP's
BackUP='/home/cashier/.wine/drive_c/%s/%s' % (Name_BackUP, Dir_BackUP)
#папка для BackUP's
BackUP_PSTrade='/home/cashier/.wine/drive_c/%s/%s/PSTrade/' % (Name_BackUP, Dir_BackUP)
#папка для BackUP's
BackUP_FM1402='/home/cashier/.wine/drive_c/%s/%s/FM1402/' % (Name_BackUP, Dir_BackUP)
#папка для BackUP's
BackUP_DISCOUNT_Folder='/home/cashier/.wine/drive_c/%s/%s/DiscountCard/' % (Name_BackUP, Dir_BackUP)
#папка для BackUP's
BackUP_VPN='/home/cashier/.wine/drive_c/%s/%s/openvpn/' % (Name_BackUP, Dir_BackUP)
#папка для BackUP's
BackUP_Reports='/home/cashier/.wine/drive_c/%s/%s/Reports/' % (Name_BackUP, Dir_BackUP)
#папка для BackUP's
BackUP_Sys32='/home/cashier/.wine/drive_c/%s/%s/Sys32/' % (Name_BackUP, Dir_BackUP)
#файл ShopName
Shop_Name='/opt/ShopName.txt'
#BackUP-system32
Sys32='/home/cashier/.wine/drive_c/%s/%s/Sys32' % (Name_BackUP, Dir_BackUP)
#путь к подключенной флэшке
FLASH_DIR='/media/cashier/'
#Диск C
DriveC='/home/cashier/.wine/drive_c/'
#
TMP_STR='/home/cashier/.wine/drive_c/Auto-BackUP/'
########## DLL
AdmFrame='/home/cashier/.wine/drive_c/PSTrade/AdmFrame.dll'
borlndmm='/home/cashier/.wine/drive_c/PSTrade/borlndmm.dll'
Discount='/home/cashier/.wine/drive_c/PSTrade/Discount.dll'
Weights='/home/cashier/.wine/drive_c/PSTrade/Weights.dll'
PumpDLL='/home/cashier/.wine/drive_c/PSTrade/PumpDLL.dll'
PsBackOffice='/home/cashier/.wine/drive_c/PSTrade/PsBackOffice.dll'
Error_TMP = '0'
tex = ''
bool = 0
#Функция Сообщения об ошибке при копировании файлов
def warning_process_copy(file, adress):
    global log_file
    f = open(log_file, 'a', encoding='UTF-8')
    log = f.write('При сборе файлов для %s\n  %s не был найден \n' % (adress, (file.split("/")[-1])))
    f.close()
#Функция Сообщения об ошибке файлов из папки СКНО
def warning_error_copy_sknoFiles(file):
    global log_file
    f = open(log_file, 'a', encoding='UTF-8')
    log = f.write('\nПри установке файлов из каталога Apteki_SKNO_install не найден %s' % (file.split("/")[-1]))
    f.close()
#Функция Сообщения об ошибке
def warning_error(x, y):
    global log_file
    f = open(log_file, 'a', encoding='UTF-8')
    log = f.write('При сборе файлов для %s\n  %s не был найден \n' % (y, x.split("/")[-1]))
    f.close()
#Функция копирования папки
def copy_dir(x, y, z):
    try:
        if not os.path.exists(x):
            warning_error(x, y)
        else:
            shutil.copytree(x, z)
    except Exception:
        print('Критическая ошибка при копировании %s в %s' % (x, y))
#Функция копирования файла
def copy_file(x, y, z):
    try:
        if not os.path.exists(x):
            warning_error(x, y)
        else:
            shutil.copy(x, z)
    except Exception:
        print('Критическая ошибка при копировании %s в %s' % (x, y))
#Функция удаления файлов
def remove_files():
    from subprocess import Popen, PIPE
    if not os.path.exists(Coupon):
        print("Купон в PSTrade не найден")
    else:
        proc = subprocess.Popen(mvCoupon, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
    proc = subprocess.Popen(rmfm1402, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
    proc = subprocess.Popen(rmfiles, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
    proc = subprocess.Popen(rmDB, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
    proc = subprocess.Popen(rmReports, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
    proc = subprocess.Popen(RM_LOG, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
#Функция удаления файлов ДЛЛ
def remove_dll():
    from subprocess import Popen, PIPE
    proc = subprocess.Popen(RM_PsBackOffice, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
    proc = subprocess.Popen(RM_PumpDLL, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
    proc = subprocess.Popen(RM_Weights, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
    proc = subprocess.Popen(RM_AdmFrame, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
    proc = subprocess.Popen(RM_borlndmm, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
    proc = subprocess.Popen(RM_Discount, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
#Функция запуска SCVIEW
def scview_pass():
    global name_scview
    global passw_scview
    f = open(Cash_ini, 'r', encoding="cp866")
    # Цикл построчного поиска нужной команды
    for oneline in f:
        oneline = oneline.strip(' \t\n\r ')
        if oneline.find('LoginNameEdit_Text') == -1:
            continue
        else:
            name_scview = ('Имя пользователя = ' + oneline.split('=')[1])

    f = open(Cash_ini, 'r', encoding="cp866")
    for oneline in f:
        oneline = oneline.strip(' \t\n\r ')
        if oneline.find('PasswordBEdit_Text') == -1:
            prev_string_oneline = oneline
            continue
        else:
            passw_scview = ('Пароль = ' + oneline.split('=')[1])

    f.close()
#Функция установки СКНО ШАГ1
def step_1():
    global filename
    filename = subprocess.check_output(['zenity','--question', '--title=Установка СКНО ШАГ 1',
                                    '--text= "Внимание перед началом установки СКНО!!\n\n\n\n'
                                    '1.Проверьте равенство сумм в БФП и БД\n'
                                    '(в меню ПС-Торговля пункт Контроль данных БЭП)\n'
                                    '2.Проверьте сумму по Безналу по КСА с банковским терминалом\n'
                                    '3.Выгрузите все чеки за последние несколько смен\n'
                                    '4.Откройте окно выгрузки по Дисконтным картам и нажмите кнопку Выгрузить\n'
                                    '5.Обязательно сделайте инкасацию на всю сумму наличных\n(чтобы наличных по кассе было 0)\n'
                                    '6.Закройте смену\n\n'
                                    'После выполнения всех пунктов нажмите Далее.\nЕсли один из них не выполним нажмите Отмена \n'
                                    'и посоветуйтесь с коллегами по вашей проблеме.',
                                    '--ok-label=Далее', '--cancel-label=Отмена', '--width=600', '--height=400']).decode("utf-8").strip()
    if not os.path.exists(Cashmain_ini):
        global filename
        filename = subprocess.check_output(['zenity', '--warning', '--title=Ошибка!!!', '--text=Ошибка!\n %s не найден!\n Установка остановлена! ' % (Cashmain_ini)])
        sys.exit()
#Функция установки СКНО ШАГ2
def step_2():
    #удаление COM2
    os.system(rmCom)
    #установка LPT
    os.system(lnLpt)
    #запуск FM1402
    from subprocess import Popen,PIPE
    proc = subprocess.Popen(fm1402, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
    #Сообщение для снятии с регистрации КСА
    filename = subprocess.check_output(['zenity', '--question', '--title=Установка СКНО ШАГ 2 Распечатываем отчеты из БЭП',
                                '--text= "В фискальной утилите Снимите фискальный отчет за период расставив галочки в пункты: \n\n\n\n'
                                '1.Данные о перерегистрациях\n'
                                '2.Итоговые суммы из БЭП\n'
                                '3.От Переррегистрации\n'
                                '4.Печать в PC886\n'
                                '5.Порт принтера LPT1(если у вас Epson) если OKI вероятно COM1\n'
                                '(проверьте кнокой Проверка печати)\n\n\n'
                                'После выполнения всех пунктов нажмите Далее.\nЕсли один из них не выполним нажмите Отмена \n'
                                'и посоветуйтесь с коллегами по вашей проблеме', '--ok-label=Далее', '--cancel-label=Отмена', '--width=600', '--height=400']).decode("utf-8").strip()
#Функция установки СКНО ШАГ3
def step_3():
    # Проверка наличия папки бэкапа
    if not os.path.exists(DriveC + Name_BackUP):
        os.mkdir(DriveC + Name_BackUP)
    # если папка есть то проверяем ее на наличие ранее созданных бэкапов с именем Auto_BackUP
    else:
        list = os.listdir(TMP_STR)
        for i in list:
            if i == Name_BackUP:
                # Если такая папка уже есть переименовываем ее
                os.rename('%s%s' % (TMP_STR, i), "%sAuto-BackUP-OLD-%s" % (TMP_STR, GetDate))
    # Создаем папку Auto-BackUP
    os.mkdir(TMP_STR + Dir_BackUP)
    # закрываем все программы
    os.system("sudo killall CashTerminal.exe")
    os.system("sudo killall RemoteModule.exe")
    os.system("sudo killall UnloadDiscountCard.exe")
    os.system("sudo killall dbsrv50.exe")
    os.system("sudo killall dbeng50.exe")
    os.system("sudo killall dbclient.exe")
    os.system("sudo killall OrdersClient.exe")
    log = open(log_file, 'w', encoding='UTF-8')
    log.close()
    # Копируем все нужные файлы
    copy_dir(PSTrade, BackUP, BackUP_PSTrade)
    copy_dir(FM1402, BackUP, BackUP_FM1402)
    copy_dir(DISCOUNT_Folder, BackUP, BackUP_DISCOUNT_Folder)
    copy_file(Cashmain_ini, BackUP, BackUP)
    copy_file(Cash_ini, BackUP, BackUP)
    copy_dir(Reports, BackUP, BackUP_Reports)
    # создаем папку для DLL и копируем их
    os.mkdir(BackUP_Sys32)
    copy_file(AdmFrame, BackUP, BackUP_Sys32)
    copy_file(borlndmm, BackUP, BackUP_Sys32)
    copy_file(Discount, BackUP, BackUP_Sys32)
    copy_file(Weights, BackUP, BackUP_Sys32)
    copy_file(PumpDLL, BackUP, BackUP_Sys32)
    copy_file(PsBackOffice, BackUP, BackUP_Sys32)
#Функция установки СКНО ШАГ4
def step_4():
    global change
#выбор кассы
    change = subprocess.check_output(['zenity', '--list', '--radiolist', '--title=Установка СКНО ШАГ 3, Выбор кассы', '--text=Выберите какая касса(1-я(главная) или (2-я(не главная))',
                                                    '--column=Отметка выбора','--column=Вид кассы',
                                                    'True', '1', 'False', '2'])
    if change == b'1\n':
        remove_files()
        remove_dll()
        return change
    elif change == b'2\n':
        remove_files()
        remove_dll()
        return change
#Функция установки СКНО ШАГ5
def step_5():
    ##############---Переменные----###########
    #Каталог с Install_Skno
    Dir_BackUP = os.getcwd()
    # папка с торговой программой PSTrade
    PSTrade = '/home/cashier/.wine/drive_c/PSTrade'
    # папка  файлов фискалки
    FM1402 = '/home/cashier/.wine/drive_c/FM1402'
    # Reports из System32
    Reports = '/home/cashier/.wine/drive_c/windows/system32/Reports'
    # Берем текущую дату
    GetDate = datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S")
    # имя Бэкапа
    Name_BackUP = 'Auto-BackUP'
    # папка для BackUP's
    BackUP_PSTrade = Dir_BackUP + '/PSTrade'
    # папка для BackUP's
    BackUP_FM1402 = Dir_BackUP + '/FM1402'
    BackUP_Reports = Dir_BackUP + '/SYS/Reports'
    # BackUP-system32
    Sys32 = '/home/cashier/.wine/drive_c/windows/system32'
    # SynkAuto
    SynkAuto = Dir_BackUP + '/SYNC-auto.zip'
    # scripts
    scripts = '/home/cashier/scripts'
    #
    SynkAuto_file = '/home/cashier/scripts/SYNC-auto.zip'
    #Ордер клиент из инстала
    Order_BackUP = Dir_BackUP + '/PSTrade/OrdersClient'
    #путь для OrdersClient
    OrderClientPath = PSTrade + '/OrdersClient'
    ########## DLL из System32
    AdmFrame = Dir_BackUP + '/SYS/AdmFrame.dll'
    borlndmm = Dir_BackUP + '/SYS/borlndmm.dll'
    Discount = Dir_BackUP + '/SYS/Discount.dll'
    Weights = Dir_BackUP + '/SYS/Weights.dll'
    PumpDLL = Dir_BackUP + '/SYS/PumpDLL.dll'
    PsBackOffice = Dir_BackUP + '/SYS/PsBackOffice.dll'
    AdmFrame_file = '/home/cashier/.wine/drive_c/windows/system32/AdmFrame.dll'
    borlndmm_file = '/home/cashier/.wine/drive_c/windows/system32/borlndmm.dll'
    Discount_file = '/home/cashier/.wine/drive_c/windows/system32/Discount.dll'
    Weights_file = '/home/cashier/.wine/drive_c/windows/system32/Weights.dll'
    PumpDLL_file = '/home/cashier/.wine/drive_c/windows/system32/PumpDLL.dll'
    PsBackOffice_file = '/home/cashier/.wine/drive_c/windows/system32/PsBackOffice.dll'
    usb99_file = '/etc/udev/rules.d/99-usb-serial.rules'
    MCTA_vendor = 'SUBSYSTEM=="tty", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="5740", SYMLINK+="mcta"'
    discount_in = Dir_BackUP + '/discount.in'
    Skidki = '/home/cashier/.wine/drive_c/Скидки'
    Discount_in = '/home/cashier/.wine/drive_c/Скидки/discount.in'
#Функция копирования файлов ПСТрэйд из Install_SKNO
    def pstrade_copy(SRC_PATH, DST_PATH):
        for f in os.listdir(SRC_PATH):
            if os.path.isfile(os.path.join(SRC_PATH, f)):
                shutil.copy(os.path.join(SRC_PATH, f), os.path.join(DST_PATH, f))
            if os.path.isdir(os.path.join(SRC_PATH, f)):
                if f == "Adm":
                    tmp = SRC_PATH + '/' + f + '/RemoteModule.exe'
                    adm = '/home/cashier/.wine/drive_c/PSTrade/Adm'
                    shutil.copy(tmp, adm)
                elif f == "OrdersClient":
                    OrdClient = '/home/cashier/.wine/drive_c/PSTrade/OrdersClient'
                    if not os.path.exists(OrdClient):
                        shutil.copytree(Order_BackUP, OrderClientPath)
                    else:
                        tmp = SRC_PATH + '/' + f
                        for i in os.listdir(tmp):
                            if os.path.isfile(os.path.join(tmp, i)):
                                shutil.copy(os.path.join(tmp, i), os.path.join(OrdClient, i))
                else:
                    try:
                        shutil.copytree(os.path.join(SRC_PATH, f), os.path.join(DST_PATH, f))
                    except Exception:
                        shutil.copytree(os.path.join(SRC_PATH, f), os.path.join(DST_PATH, f))

    # функция копирования каталогов
    def copypath(SRC_PATH, DST_PATH):
        # проверка существования каталога в папке с бэкапом
        if not os.path.exists(SRC_PATH):
            warning_error_copy_sknoFiles(SRC_PATH)
        else:
            # проверка существования каталога в образе
            if not os.path.exists(DST_PATH):
                # если нет то копируем
                try:
                    shutil.copytree(SRC_PATH, DST_PATH)
                except Exception:
                    warning_process_copy(SRC_PATH, DST_PATH)
            else:
                # если есть переименовываем старую,кладем новую
                os.rename(DST_PATH, DST_PATH + '-OLD-' + GetDate)
                try:
                    shutil.copy(SRC_PATH, DST_PATH)
                except Exception:
                    warning_process_copy(SRC_PATH, DST_PATH)

    # функция копирования файлов
    def copydll(SRC_PATH, DST_PATH, NAME_FILE):
        # проверка существования каталога в папке с бэкапом
        if not os.path.exists(SRC_PATH):
            # если не найдена выдаем соббщение
            warning_error_copy_sknoFiles(SRC_PATH)
        else:
            # проверка существования файла в образе
            if not os.path.exists(NAME_FILE):
                # если нет то копируем
                try:
                    shutil.copy(SRC_PATH, DST_PATH)
                except Exception:
                    warning_process_copy(SRC_PATH, DST_PATH)
            else:
                # если есть переименовываем старый,кладем новый
                os.remove(NAME_FILE)
                try:
                    shutil.copy(SRC_PATH, DST_PATH)
                except Exception:
                    warning_process_copy(SRC_PATH, DST_PATH)

    # копируем файлы
    def copy_1Kass():
        copypath(SRC_PATH=BackUP_FM1402, DST_PATH=FM1402)
        pstrade_copy(BackUP_PSTrade, PSTrade)
        copypath(SRC_PATH=BackUP_Reports, DST_PATH=Reports)
        copydll(SRC_PATH=SynkAuto, DST_PATH=scripts, NAME_FILE=SynkAuto_file)
        copydll(SRC_PATH=AdmFrame, DST_PATH=Sys32, NAME_FILE=AdmFrame_file)
        copydll(SRC_PATH=Discount, DST_PATH=Sys32, NAME_FILE=Discount_file)
        copydll(SRC_PATH=Weights, DST_PATH=Sys32, NAME_FILE=Weights_file)
        copydll(SRC_PATH=PumpDLL, DST_PATH=Sys32, NAME_FILE=PumpDLL_file)
        copydll(SRC_PATH=borlndmm, DST_PATH=Sys32, NAME_FILE=borlndmm_file)
        copydll(SRC_PATH=PsBackOffice, DST_PATH=Sys32, NAME_FILE=PsBackOffice_file)
        copydll(SRC_PATH=discount_in, DST_PATH=Skidki, NAME_FILE=Discount_in)

    def copy_2Kass():
        copypath(SRC_PATH=BackUP_FM1402, DST_PATH=FM1402)
        pstrade_copy(BackUP_PSTrade, PSTrade)
        copypath(SRC_PATH=BackUP_Reports, DST_PATH=Reports)
        copydll(SRC_PATH=SynkAuto, DST_PATH=scripts, NAME_FILE=SynkAuto_file)
        copydll(SRC_PATH=AdmFrame, DST_PATH=Sys32, NAME_FILE=AdmFrame_file)
        copydll(SRC_PATH=Discount, DST_PATH=Sys32, NAME_FILE=Discount_file)
        copydll(SRC_PATH=Weights, DST_PATH=Sys32, NAME_FILE=Weights_file)
        copydll(SRC_PATH=PumpDLL, DST_PATH=Sys32, NAME_FILE=PumpDLL_file)
        copydll(SRC_PATH=borlndmm, DST_PATH=Sys32, NAME_FILE=borlndmm_file)
        copydll(SRC_PATH=PsBackOffice, DST_PATH=Sys32, NAME_FILE=PsBackOffice_file)
        from subprocess import Popen, PIPE
        proc = subprocess.Popen(rmDB, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
#Добавление строки с вендором СКНО
    def add_string_99usb():
        f = open(Devices, 'r')
        # Цикл построчного поиска нужной команды
        tmp_string = 0
        for oneline in f:
            oneline = oneline.strip(' \t\n\r ')
            # если не нашли нужный текст в строке ищем дальше
            if oneline.find(MCTA_vendor) == -1:
                continue
                # если нашли
            else:
                tmp_string = 1
                break
        f.close()
        if tmp_string == 0:
            f = open(usb99_file, 'a')
            f.write(MCTA_vendor + '\n')
        f.close()
#если выбрано что это касса 1
    if change == b'1\n':
        copy_1Kass()
#если выбрано что это касса 2
    elif change == b'2\n':
        copy_2Kass()
#запуск SynkAuto
    SynkAuto_zip = zipfile.ZipFile(SynkAuto_file)
    SynkAuto_zip.extractall(scripts)
    SynkAuto_zip.close()
    os.system('bash /home/cashier/scripts/SYNC-auto/install.sh')
    add_string_99usb()

#Функция установки СКНО ШАГ6
def step_6():
#Запуск FM1402
    from subprocess import Popen, PIPE
    proc = subprocess.Popen(fm1402, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
#Вызов сообщения для перерегистрации
    filename = subprocess.check_output(['zenity', '--question', '--title=Установка СКНО ШАГ 4 Регистрируем БЭП',
         '--text= "В фискальной утилите произведите регистрацию КСА\n'
         'Распечатайте отчет расставив галочки в пункты:  \n\n\n\n'
         '1.Данные о перерегистрациях\n'
         '2.Данные за период\n'
         '3.Печать в PC886\n'
         '4.Порт принтера LPT1(если у вас Epson) если OKI вероятно COM1\n'
         '(проверьте кнокой Проверка печати)\n\n\n'
         'После выполнения всех пунктов нажмите Далее.\nЕсли один из них не выполним нажмите Отмена \n'
         'и посоветуйтесь с коллегами по вашей проблеме', '--ok-label=Далее', '--cancel-label=Отмена', '--width=600',
         '--height=400']).decode("utf-8").strip()
#Функция установки СКНО ШАГ7
def step_7():
    addCashmain = os.getcwd() + '/AddCashMain.ini'
    udlString = 'ANYDB=FILE NAME=C:\Program Files\Common Files\System\OLE DB\Data Links\TradeLocal.udl'
#Функция удаления и вставки в CashMain
    global text
    global bool
    def ReplaceLineInFile(fileName, sourceText, replaceText):
        global text
        global bool
        if bool == 0:
            file = open(fileName, encoding='cp866', mode='r')
            text = file.read()
            file.close()
            text = text.replace(sourceText, replaceText)
            bool = 1
        else:
            text = text.replace(sourceText, replaceText)

    f = open(addCashmain, 'r', encoding='cp866')
    for oneline in f:
        if oneline == '\n':
            continue
        else:
            oneline = oneline.strip('')
            tmp_string = str(oneline)
            newString = ''
            ReplaceLineInFile(Cashmain_ini, tmp_string, newString)
    f.close()

    s = list(text)
    i = 2
    while i < len(s):
        if s[i - 2] == '\n' and s[i - 1] == '\n' and s[i] == '\n':
            s.pop(i - 1)
        i += 1
    i = 0
    while s[i] == '\n':
        s.pop(i)

    text = ''.join(s)

    file = open(Cashmain_ini, encoding='cp866', mode='w')
    file.write(text)
    file.close()

    text = ''
    file = open(Cashmain_ini, encoding='cp866', mode='r')
    for lineCashMain in file:
        if lineCashMain.find(udlString) == -1:
            text = text + lineCashMain
        else:
            text = text + lineCashMain
            f = open(addCashmain, 'r', encoding='cp866')
            for lineAddCashMain in f:
                text = text + lineAddCashMain
            f.close()
    file.close()
    file = open(Cashmain_ini, encoding='cp866', mode='w')
    file.write(text)
    file.close()
#запускаем CashMain
    os.chdir('/home/cashier/.wine/drive_c/windows')
    from subprocess import Popen, PIPE
    proc = subprocess.Popen(cashmain_notepad, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
    filename = subprocess.check_output(['zenity', '--question', '--title=Установка СКНО ШАГ 5 Вносим данные в CashMain.ini',
         '--text=Вносим данные аптеки (В версии с СКНО они берутся из CashMain.ini)\n'
         'заполняем 3 параметра:\n'
         'P_Name1= \n'
         'P_Name2= \n'
         'P_Name3= \n'
         '\n\n\n\n'
         'После выполнения всех пунктов нажмите Далее.\nЕсли один из них не выполним нажмите Отмена \n'
         'и посоветуйтесь с коллегами по вашей проблеме', '--ok-label=Далее',
         '--cancel-label=Отмена', '--width=500',
         '--height=300']).decode('cp866').strip()

#Функция установки СКНО ШАГ8
def step_8():
#Если  выбрано что это касса 1 открываем БД и выдаем сообщение с именем пользователя и паролем
    global change
    if change == b'1\n':
        scview_pass()
        from subprocess import Popen, PIPE
        proc = subprocess.Popen(scview, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
        filename = subprocess.check_output(['zenity', '--question', '--title=Установка СКНО ШАГ 6 Добавляем пользователя в БД',
                                            '--text= Добавьте пользователя в БД\n'
                                            '\n\n\n'
                                            '%s \n'
                                            '%s \n\n'
                                            'После выполнения всех пунктов нажмите Далее.\nЕсли один из них не выполним нажмите Отмена \n'
                                            'и посоветуйтесь с коллегами по вашей проблеме' % (name_scview, passw_scview), '--ok-label=Далее',
                                            '--cancel-label=Отмена', '--width=500',
                                            '--height=300']).decode("utf-8").strip()
        return change
#Если касса 2 то продолжаем без БД
    elif change == b'2\n':
        return change

    os.system(rmLpt)
    os.system(lnCom)
#Функция установки СКНО ШАГ9
def step_9():
    tmp = os.getcwd() + '/tmp'
    line = ''
    iniFile = '/home/cashier/.wine/drive_c/windows/CashMain.ini'
    changeString = 'skkoComPort'

    def ReplaceLineInFile(fileName, sourceText, replaceText):
        file = open(fileName, encoding="cp866" , mode='r')
        text = file.read()
        file.close()
        file = open(fileName, encoding="cp866", mode='w')
        file.write(text.replace(sourceText, replaceText))
        file.close()

    file = open(tmp, encoding='cp866', mode='w')
    file.close()
    z = 'ls -la ~/.wine/dosdevices |grep com >> tmp'
    os.system(z)

    file = open(tmp, encoding='cp866', mode='r')
    string = 'com4'
    for line in file:
        if line.find('mcta') == -1:
            continue
        else:
            line = line.split(' ')[11]
            if line == string:
                newString = 'skkoComPort=' + line + '\n'
                #ReplaceLineInFile(iniFile, changeString, newString)
                fileCash = open(iniFile, encoding='cp866', mode='r')
                for lineCashMain in fileCash:
                    fileCash = open(iniFile, encoding='cp866', mode='r')
                    if lineCashMain.find(changeString) == -1:
                        continue
                    else:
                        changeString = lineCashMain
                        fileCash.close()
                        ReplaceLineInFile(iniFile, changeString, newString)
            else:
                newString = 'skkoComPort=' + line +'\n'
                ReplaceLineInFile(iniFile, changeString, newString)
    os.system(rmLpt)
    os.system(lnCom)

#Сообщение с подсказкой
    filename = subprocess.check_output(['zenity', '--question', '--title=Установка СКНО ШАГ 7 Подключите СКНО в PS-POS',
         '--text= Подключите СКНО в PS-POS\n'
         '\n\n\n\n'
         'ВАЖНОЕ ЗАМЕЧАНИЕ!!! \n'
         'При нехватке USB портов в КСА и наличии свободных PS/2, связываться с '
         'техподдержкой и рекомендовать установить переходники USB → PS/2 \n'
         'либо заменить USB клавиатуру (мышь) на PS/2.При нехватке USB портов в КСА и отсутствии свободных PS/2,\n'
         'действительно единственным выходом для установки СКНО является использование USB концентраторов '
         '(не обязательно с доп. питанием).\n'
         'Если данное оборудование отсутствует, то для того, что бы освободить USB порт для СКНО и обеспечения работоспособности КСА,\n'
         'можно временно отключить другое USB устройство, за исключением (Чекового принтера, дисплея, покупателя)\n'
         'После выполнения всех пунктов нажмите Далее.\nЕсли один из них не выполним нажмите Отмена \n'
         'и посоветуйтесь с коллегами по вашей проблеме', '--ok-label=Далее',
         '--cancel-label=Отмена', '--width=600',
         '--height=400']).decode("utf-8").strip()

#Сообщение с подсказкой и завершение программы
def step_10():
    global log_file
    log = open(log_file, 'r', encoding='UTF-8')
    log_read = log.read()
    filename = subprocess.check_output(['zenity', '--question', '--title=Установка СКНО Протокол ошибок при выполнении',
                                        '--text= %s\n' % (log_read) ,
                                        '--ok-label=Далее',
                                        '--cancel-label=Отмена', '--width=800',
                                        '--height=450']).decode("utf-8").strip()
    log.close()
    filename = subprocess.check_output(['zenity', '--question', '--title=Завершение установки',
         '--text= Установка СКНО Завершена\n\n\n\n'
         'Вам остается!!! \n'
         '1. Перезагрузить кассу. \n'
         '2. Открыть смену.\n'
         '3. Сделать внесение на 0.01\n'
         '4. Сделать инкассацию на 0.01\n'
         '5. Закрыть смену.\n'
         '6. Позвонить в РУП "ИИЦ"\n'
         '7. Запустить кассу в работу.\n'
         '8. Заполнить акт в трех экземплярах, подписать, дать на подпись кассиру.\n'
         '9. Сфотографировать один экземпляр акта.\n'
         '10 Отправить в вайбере фото Ольге Сушкевич. (Если у Вас нет вайбера,\n'
         'то отправить скан по почте Ольге Сушкевич, копия Светлане Полозковой)\n',
         '--ok-label=Завершить',
         '--cancel-label=Отмена', '--width=600',
         '--height=400']).decode("utf-8").strip()

step_1()
step_2()
step_3()
step_4()
step_5()
step_6()
step_7()
step_8()
step_9()
step_10()