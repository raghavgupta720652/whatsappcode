from datetime import timedelta
import datetime
from django.contrib.auth import get_user_model

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView
from .forms import *
import pywhatkit
import pytz
from django.conf import settings
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import datetime
import time
import webbrowser
import pyautogui as gui
import os
# try:
import autoit
# except ModuleNotFoundError:
#     pass

import schedule
# Importing traceback to catch xml button not found errors in the future
import traceback
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options


import time
import datetime
import os
import argparse
import platform
# import openpyxl as excel

# Create your views here.
User = get_user_model()


class UserCreate(CreateView):
    model = User
    form = CreateUserForm
    fields = ["first_name", "last_name", "email", "password", "contact_no"]
    template_name = "signup.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


User = get_user_model()


@csrf_exempt
def login_user(request, template_name=None, extra_context=None):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.admin_verified == True:
                login(request, user)
                return redirect('Webap:add_phone')

            else:
                messages.error(
                    request, 'Please ask admin to verify your account!If already verified please check your email or password!')
                return redirect('Webap:login')

    return render(request, 'login.html', {})


def register(request):
    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():
            if not request.POST.get('email', None) or not request.POST.get('contact_no', None):
                messages.error(
                    request, 'Registration failed! Please enter details.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if User.objects.filter(email=request.POST.get('email', None)):
                messages.error(
                    request, 'User already exist with this email id.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if User.objects.filter(contact_no=request.POST.get('contact_no', None)):
                messages.error(
                    request, 'User already exist with this mobile no.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = User.objects.create(
                email=request.POST.get('email'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                username=request.POST.get('email'),
                password=request.POST.get('password'),
                contact_no=request.POST.get('contact_no'),
                admin_verified=False
            )

            user.set_password(user.password)
            user.save()
            messages.info(
                request, 'Signed Up Successfully!Please wait for admin to verify your account')
            return redirect('Webap:login')
        else:
            return render(request, 'signup.html', {'form': form}, status=201)

    form = CreateUserForm()
    return render(request, 'signup.html', {'form': form})


def logout(request):
    auth.logout(request)

    return redirect('Webap:login')


def phone_add(request):

    if request.method == 'POST':
        p = PhoneNumber.objects.create(
            phone_number=request.POST.get('phone_number'),
            added_by=request.user,

        )

        messages.info(request, 'Phone number added successfully!')
        return redirect('Webap:phone_list')
    else:
        return render(request, 'add_phone.html')


class PhoneListView(View):

    def get(self, request, *args, **kwargs):

        products = PhoneNumber.objects.filter(
            added_by=request.user).order_by("created_on")

        products = products

        return render(request, "phone_data_list.html", {
            "products": products,

        })


class PhoneDelete(View):

    def get(self, request, *args, **kwargs):
        product = PhoneNumber.objects.filter(
            id=request.GET.get("phone_id", None))
        if product:
            product.delete()
            messages.info(request, 'Phone number deleted successfully!')
        return redirect(request.META.get("HTTP_REFERER"))


if platform.system() == 'Darwin':
    # MACOS Path
    chrome_default_path = os.getcwd() + '/driver/chromedriver'
else:
    # Windows Path
    chrome_default_path = os.getcwd() + '/driver/chromedriver.exe'

# parser = argparse.ArgumentParser(description='PyWhatsapp Guide')
# parser.add_argument('--chrome_driver_path', action='store', type=str, default=chrome_default_path,
#                     help='chromedriver executable path (MAC and Windows path would be different)')
# parser.add_argument('--message', action='store', type=str,
#                     default='', help='Enter the msg you want to send')
# parser.add_argument('--remove_cache', action='store', type=str, default='False',
#                     help='Remove Cache | Scan QR again or Not')
# parser.add_argument('--import_contact', action='store', type=str, default='False',
#                     help='Import contacts.txt or not (True/False)')
# parser.add_argument('--enable_headless', action='store', type=str, default='False',
#                     help='Enable Headless Driver (True/False)')
# args = parser.parse_args()

# if args.remove_cache == 'True':
#     os.system('rm -rf User_Data/*')
browser = None
Contact = None
# message = None if args.message == '' else args.message
Link = "https://web.whatsapp.com/"
wait = None
choice = None
docChoice = None
doc_filename = None
unsaved_Contacts = None


def input_contacts():
    global Contact, unsaved_Contacts
    # List of Contacts
    Contact = []
    unsaved_Contacts = []
    while True:
        # Enter your choice 1 or 2
        print("PLEASE CHOOSE ONE OF THE OPTIONS:\n")
        print("1.Message to Saved Contact number")
        print("2.Message to Unsaved Contact number\n")
        x = int(input("Enter your choice(1 or 2):\n"))
        print()
        if x == 1:
            n = int(input('Enter number of Contacts to add(count)->'))
            print()
            for i in range(0, n):
                inp = str(input("Enter contact name(text)->"))
                inp = '"' + inp + '"'
                # print (inp)
                Contact.append(inp)
        elif x == 2:
            n = int(input('Enter number of unsaved Contacts to add(count)->'))
            print()
            for i in range(0, n):
                # Example use: 919899123456, Don't use: +919899123456
                # Reference : https://faq.whatsapp.com/en/android/26000030/
                inp = str(input(
                    "Enter unsaved contact number with country code(interger):\n\nValid input: 91943xxxxx12\nInvalid input: +91943xxxxx12\n\n"))
                # print (inp)
                unsaved_Contacts.append(inp)

        choi = input("Do you want to add more contacts(y/n)->")
        if choi == "n":
            break

    if len(Contact) != 0:
        print("\nSaved contacts entered list->", Contact)
    if len(unsaved_Contacts) != 0:
        print("Unsaved numbers entered list->", unsaved_Contacts)
    input("\nPress ENTER to continue...")


def input_message():
    global message
    # Enter your Good Morning Msg
    print(
        "Enter the message and use the symbol '~' to end the message:\nFor example: Hi, this is a test message~\n\nYour message: ")
    message = ['hello']
    done = False

    while not done:
        temp = input()
        if len(temp) != 0 and temp[-1] == "~":
            done = True
            message.append(temp[:-1])
        else:
            message.append(temp)
    message = "\n".join(message)
    print(message)


def whatsapp_login(chrome_path, headless):
    global wait, browser, Link
    chrome_options = Options()
    # chrome_options.add_argument('--user-data-dir=./User_Data')
    # if headless == 'True':
    #     chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(
        executable_path=chrome_path, options=chrome_options)
    wait = WebDriverWait(browser, 600)
    browser.get(Link)
    browser.maximize_window()
    print("QR scanned")


def send_message(target):
    global message, wait, browser
    try:
        x_arg = '//span[contains(@title,' + target + ')]'
        ct = 0
        while ct != 5:
            try:
                group_title = wait.until(
                    EC.presence_of_element_located((By.XPATH, x_arg)))
                group_title.click()
                break
            except Exception as e:
                print("Retry Send Message Exception", e)
                ct += 1
                time.sleep(3)
        input_box = browser.find_element_by_xpath(
            '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        for ch in message:
            if ch == "\n":
                ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(
                    Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)
        input_box.send_keys(Keys.ENTER)
        print("Message sent successfully")
        time.sleep(1)
    except NoSuchElementException as e:
        print("send message exception: ", e)
        return


def send_unsaved_contact_message():
    global message
    try:
        time.sleep(10)
        browser.implicitly_wait(10)
        input_box = browser.find_element_by_xpath(
            '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        for ch in message:
            if ch == "\n":
                ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(
                    Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)
        input_box.send_keys(Keys.ENTER)
        print("Message sent successfully")
    except Exception as e:
        print("Failed to send message exception: ", e)
        return


def send_attachment():
    # Attachment Drop Down Menu
    try:
        clipButton = browser.find_element_by_xpath(
            '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div/span')
        clipButton.click()
    except:
        traceback.print_exc()
    time.sleep(1)

    # To send Videos and Images.
    try:
        mediaButton = browser.find_element_by_xpath(
            '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div/div/ul/li[1]/button')
        mediaButton.click()
    except:
        traceback.print_exc()
    time.sleep(3)
    hour = datetime.datetime.now().hour
    # After 5am and before 11am scheduled this.
    # if (hour >= 5 and hour <= 11):
    #     image_path = os.getcwd() + "\\Media\\" + 'goodmorning.jpg'
    # # After 9pm and before 11pm schedule this
    # elif (hour >= 21 and hour <= 23):
    #     image_path = os.getcwd() + "\\Media\\" + 'goodnight.jpg'
    # else:  # At any other time schedule this.
    #     image_path = os.getcwd() + "\\Media\\" + 'howareyou.jpg'
    # print(image_path)

    autoit.control_focus("Open", "Edit1")
    autoit.control_set_text("Open", "Edit1", image_path)
    autoit.control_click("Open", "Button1")

    time.sleep(3)
    # Send button
    try:
        whatsapp_send_button = browser.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div')
        whatsapp_send_button.click()
    except:
        traceback.print_exc()

    print("File sent")


def send_files():
    global doc_filename
    # Attachment Drop Down Menu
    clipButton = browser.find_element_by_xpath(
        '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div/span')
    clipButton.click()

    time.sleep(1)
    # To send a Document(PDF, Word file, PPT)
    # This makes sure that gifs, images can be imported through documents folder and they display
    # properly in whatsapp web.
    if doc_filename.split('.')[1] == 'pdf' or doc_filename.split('.')[1] == 'docx' or doc_filename.split('.')[1] == 'pptx':
        try:
            docButton = browser.find_element_by_xpath(
                '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div/div/ul/li[3]/button')

            docButton.click()
        except:
            # Check for traceback errors with XML imports
            traceback.print_exc()
    else:
        try:
            # IMG attatchment button
            docButton = browser.find_element_by_xpath(
                '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div/div/ul/li[1]/button')
            docButton.click()
        except:
            # Check for traceback errors with XML imports
            traceback.print_exc()
    time.sleep(1)
    docPath = os.getcwd() + "\\Documents\\" + doc_filename
    try:
        autoit.control_focus("Open", "Edit1")
    except:
        traceback.print_exc()
    autoit.control_set_text("Open", "Edit1", (docPath))
    autoit.control_click("Open", "Button1")
    time.sleep(3)
    # Changed whatsapp send button xml link.
    whatsapp_send_button = browser.find_element_by_xpath(
        '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div')

    whatsapp_send_button.click()
    print('File sent')


def import_contacts():
    global Contact, unsaved_Contacts
    Contact = []
    unsaved_Contacts = []
    fp = open("contacts.txt", "r")
    while True:
        line = fp.readline()
        con = ' '.join(line.split())
        if con and con.isdigit():
            unsaved_Contacts.append(int(con))
        elif con:
            Contact.append(con)
        if not line:
            break


def sender():
    global unsaved_Contacts
    if len(unsaved_Contacts) > 0:
        for i in unsaved_Contacts:
            link = "https://web.whatsapp.com/send?phone={}&text&source&data&app_absent".format(
                i)
            # driver  = webdriver.Chrome()
            browser.get(link)
            print("Sending message to", i)
            send_unsaved_contact_message()
            if (True):
                try:
                    send_attachment()
                except:
                    print()
            time.sleep(7)


# # For GoodMorning Image and Message
# schedule.every().day.at("07:00").do(sender)
# # For How are you message
# schedule.every().day.at("13:35").do(sender)
# # For GoodNight Image and Message
# schedule.every().day.at("22:00").do(sender)

# # Example Schedule for a particular day of week Monday
# schedule.every().monday.at("08:00").do(sender)


# To schedule your msgs
def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


class PhoneSelectionSendView(View):

    def get(self, request, *args, **kwargs):

        products = PhoneNumber.objects.filter(
            added_by=request.user).order_by("created_on")

        products = products

        return render(request, "phone-selection.html", {
            "products": products,

        })

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            global unsaved_Contacts, message, image_path
            unsaved_Contacts = []
            p = PhoneNumber.objects.filter(
                id__in=request.POST.getlist("selected_products"))
            for product in p:
                number = '91'+product.phone_number
                unsaved_Contacts.append(number)
            message = request.POST.get('message')
            image = request.FILES.get('image')
            print(image)
            image_path = os.path.abspath(image)
            print(image_path)
            raise
            print("SCAN YOUR QR CODE FOR WHATSAPP WEB")
            whatsapp_login(
                os.getcwd() + '/driver/chromedriver.exe', False)
            sender()
            # url = 'https://wa.me/919017161465?text=hello'
            # webbrowser.open(url)
            # time.sleep(3)
            # gui.click(786, 366)
            # time.sleep(3)
            # gui.click(792, 424)
            # time.sleep(10)
            # gui.press('enter')
            # time.sleep(2)

            # driver = webdriver.Chrome()
            # driver.execute_script("window.open('https://web.whatsapp.com/')")
            # wait5 = WebDriverWait(driver, 100)
            # user = driver.find_element_by_xpath('//span[(@title="Attach")]')
            # user.click()
            # message = driver.find_element_by_class_name('_13mgZ')
            # message.send_keys("hello")
            # sendbutton = driver.find_element_by_class_name('_3M-N-')
            # sendbutton.click()
            # raise
            # image = request.POST.get("image")
            # p = PhoneNumber.objects.filter(
            #     id__in=request.POST.getlist("selected_products"))

            # chrome_default_path = os.getcwd() + '/driver/chromedriver.exe'
            # print(chrome_default_path)
            # raise
            # from django.utils import timezone
            # from datetime import datetime
            # for product in p:
            # url = 'https://wa.me/91{}?text={}'.format(
            #     str(product.phone_number), request.POST.get('message'))

            # webbrowser.open(url)
            # time.sleep(3)
            # gui.click(786, 366)
            # time.sleep(3)
            # gui.click(792, 424)
            # time.sleep(10)
            # gui.click(786, 366)
            # if request.POST.get("image"):
            #     gui.click(594, 848)
            #     gui.click(596, 780)
            #     autoit.control_focus("Open", "Edit1")
            #     autoit.control_set_text("Open", "Edit1", image_path)
            #     autoit.control_click("Open", "Button1")
            # gui.locateCenterOnScreen(os.path.abspath(image))
            # print(start)
            # gui.moveTo(start)
            # get_id = webbrowser.Document.GetElementById(
            #     "df9d3429-f0ef-48b5-b5eb-f9d27b2deba6")
            # gui.press(get_id)
            # raise
            # gui.press('enter')
            # time.sleep(2)
            # webbrowser.close()
            #     b = datetime.now()
            #     h = b.hour
            #     m = b.minute
            #     s = b.second
            #     pywhatkit.sendwhatmsg(
            #         "+91" + str(product.phone_number), request.POST.get('message'), h, m+1)

            # products = PhoneNumber.objects.filter(
            #     added_by=request.user).order_by("id")
            messages.info(request, 'Content added successfully!')
            return render(request, "phone-selection.html")
        else:
            return render(request, "phone-selection.html", {"products": products})
