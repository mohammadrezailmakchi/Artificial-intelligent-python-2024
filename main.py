# اضافه کردن ماژول های مختلف
# Add different modules
from pathlib import Path
import pygetwindow as gw  
import customtkinter as customtkinter
from PIL import Image,ImageTk
from openai import OpenAI
from dotenv import load_dotenv
import threading
import tkinter as tk
import os
import datetime
import requests
import sounddevice as sd
import soundfile as sf
import numpy as np
from awesometkinter.bidirender import render_text
import pygame
import ctypes
from CTkMessagebox import CTkMessagebox
import pywinstyles
from CTkToolTip import *
import webbrowser
from pydub import AudioSegment
import os, shutil
from tkinterdnd2 import TkinterDnD, DND_FILES
import base64
import uuid

# ابزارهای pygame را مقداردهی اولیه کنید
# initializing pygame
pygame.init()

# ماژول pygame.mixer را برای پخش صداها مقداردهی اولیه کنید
# Pygame.mixer module to play the sound of sounds
pygame.mixer.init()

# متغیرهای محیطی را از فایل .env به محیط بارگذاری کنید
# Upload the environmental variables from the .env file to the environment
load_dotenv()

# حالت ظاهری برنامه را به "تیره" تنظیم کنید
# Set the app's appearance to "dark"
# "سیستم" حالت ظاهری را همانند حالت ظاهری سیستم تنظیم می‌کند
# The "system" adjusts the appearance of the appearance of the system
customtkinter.set_appearance_mode("dark")        

# رنگ پیش‌فرض ویجت‌ها را به "تیره-آبی" تنظیم کنید
# Adjust the default color of the widgets to the "dark-water"
# تم‌های پشتیبانی شده: سبز، تیره-آبی، آبی
# Supported themes: green, dark-water, blue
customtkinter.set_default_color_theme("dark-blue")

# DPI awareness اتوماتیک برای customtkinter را غیرفعال کنید
# Disable DPI Automatic for Customtkinter
customtkinter.deactivate_automatic_dpi_awareness()

# فریم پنجره چت
# Chat window frame
class ChatFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
 
# ساخت کلاس App
# Build the app class
class App(customtkinter.CTk):
    # طرح GUI در init نوشته می‌شود
# GUI design is written in Init
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def show_error(title, message):
            # نمایش پیام خطا
# View the error message
            CTkMessagebox(title=title, message=message, icon="cancel")

        def show_info(title, message):
            # نمایش پیام اطلاعات یا خبر دادن
# Display the message of information or to report
            CTkMessagebox(title=title, message=message)

        # تنظیم عنوان پنجره به "Artificial Intelligent"
# Set the window title to “Artificial Intelligent”
        self.title("Artificial Intelligent")

        

        # گرفتن رزولوشن نمایشگر
# Getting the display resolution
        try:
            pywinstyles.apply_style(self, "optimized")
        except:
            pass

        #تعریف متغییر برای طول و عرض صفحه نمایش     
# Definition of variable for the length and width of the screen
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()

        #تعریف تابع برای باز کردن وب سایت
# Definition of function to open the website

        #این یکی برای اینکه فایل html را باز کنیم
# This one to open the HTML file
        def WebURLOpening(url):
            dir_path = os.path.dirname(os.path.realpath(__file__))
            webbrowser.open(url=dir_path + url)

        #تابع برای باز کردن ویدیوی آموزشی
# Function to open the tutorial video
        def VideoTutorial():
            dir_path = os.path.dirname(os.path.realpath(__file__))
            os.startfile((dir_path + "\\VideoTutorial\\VideoTutorial.mp4"))

        

        #این یکی برای باز کردن یک سایت در اینترنت
# This one to open a site on the Internet
        def site_open (url):
            webbrowser.open (url=url)

        # تعریف طول و عرض برنامه بر حسب متغییر های طول و عرض گرفته شده از سیستم       
# Definition of the length and width of the program in terms
        self.geometry(f"{width}x{height}")

        

        #تعریف متغییر برای گرفتن رزولوشن سیستم 
# Variable Definition to Get System Resolution
        scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

        #تعریف رزولوشن ابزار های برنامه برحسب رزولوشن سیستم 
# Definition of System Tools Resolution Definition
        if width == 1920 and height == 1080 :
            customtkinter.set_widget_scaling(1.25)

        elif width == 1600 and height == 1024 :
            customtkinter.set_widget_scaling(1.05)
        
        elif width == 1600 and height == 900 :
            customtkinter.set_widget_scaling(1.025)

        elif width == 1440 and height == 1080 :
            customtkinter.set_widget_scaling(0.95)

        elif width == 1400 and height == 1050 :
            customtkinter.set_widget_scaling(0.925)

        elif width == 1366 and height == 768 :
            customtkinter.set_widget_scaling(0.85)

        elif width == 1280 and height == 1024 :
            customtkinter.set_widget_scaling(0.845)

        elif width == 1280 and height == 960 :
            customtkinter.set_widget_scaling(0.84)

        elif width == 1280 and height == 720 :
            customtkinter.set_widget_scaling(0.8)

        elif width == 1152 and height == 864 :
            customtkinter.set_widget_scaling(0.75)

        elif width == 1024 and height == 768 :
            customtkinter.set_widget_scaling(0.675)

        elif width == 800 and height == 600 :
            customtkinter.set_widget_scaling(0.525)
        else :     
            #ایجاد یک پیام خطا برای رزولوشن نامناسب
# Create an error message for inappropriate resolution
            show_error("Bad Scaling", render_text(" از قسمت تنظیمات ویندوز رزولوشن صفحه خود را روی حالت پیشنهادی قرار دهید"))
        


        #ایجاد یک متغییر برای ایجاد حافظه ی هوش مصنوعی 
# Create a variable to create artificial intelligence memory
        self.conversations = {}  

        #نام گذاری پیش فرض برای حافظه ی هوش مصنوعی
# Default naming for artificial intelligence memory
        self.current_room = "Default" 

        #نام گذاری پیش فرض برای حافظه ی هوش مصنوعی
# Default naming for artificial intelligence memory
        self.current_roomS = "DefaultS" 

        self.current_roomGPTHNAI = "DefaultGPTHNAI"  
        #تعریف متغییر برای گرفتن حالت ارسال
# Definition of variable to get the submission mode
        self.sending = False  
        #تعریف متغییر برای حالت اولین ارسال 
# Definition of variable for the first submission mode
        self.first_response = True
        #تعریف یک key بر حسب نام پیش فرض برا یذخیره حافظه ی هوش مصنوعی
# Define a Key by default name to store artificial intelligence memory
        self.conversations[self.current_room] = [] 

        #تعریف یک key بر حسب نام پیش فرض برا یذخیره حافظه ی هوش مصنوعی
# Define a Key by default name to store artificial intelligence memory
        self.conversations[self.current_roomS] = [] 

        #مثل عمل فوق اما برای قسمت GPTHNAI
# Like the above action but for the gpthnai part
        self.conversations[self.current_roomGPTHNAI] = [] 

        #ایجاد اولیه ارتباط با API
# Create initial relationship with API
        self.client = OpenAI()

        # وارد کردن ای پی ای کی از فایل env برای اتصال دستی به ای پی ای
# Enter the EPK from the ENV file to manually connect to APA
        api_key = os.getenv('OPENAI_API_KEY')

        # مقدار دهی اولیه مدل هوش مصنوعی
# The initial value of the artificial intelligence model
        self.AIMODEL = "gpt-3.5-turbo-0125" 

        #ساخت یک لیست برای نام های فونت
# Making a list for font names
        self.Fonts = ["VAZIRMATN MEDIUM", "Arial"]

        #تلاش برای مقدار دهی اولیه فونت به فونت وزیر متن
# Trying to give the font to the font of the text minister
        try:
            self.CurrentFont = "VAZIRMATN MEDIUM"
        except:
            self.CurrentFont = "Arial"

        #استایل های فونت 
# Fonts styles
        self.FontsStyles = ["bold", "italic", "normal"]

        #استایل کنونی فونت
# Current font style
        self.CurrentFontBoldState = "normal"

        #سایز های مختلف برای فونت
# Different sizes for fonts
        self.FontsSizes = ["8","10","12","14","16","18","20","22","24","26","28","30","32","34","36"]

        #مقدار دهی اولیه سایز فونت
# The initial amount of font size
        self.CurrentFontSize = 14
        
        #مقدار دهی اولیه برای متغییر برای گرفتن پیام از ورودی یا همان Entery
# Initial value for variables to get a message from the input or the same ENTERY
        self.ChatBoxEnteryValue = ""

        #آیا در حال ضبط صدا است یا نه
# Whether or not the sound recording or not
        self.is_recording = False

        #ایجاد یک لیست برای ذخیره ی تکه ها یا قطعه های صدا
# Create a list to store pieces or pieces of sound
        self.AudioChunks = []

        #مقدار دهی استاندارد برای کیفیت ضبط صدا CD-quality
# Standard value for the quality of the CD-CD-CD
        self.samplerate = 44100

        #Stereo ضبط به صورت 
# Stereo recorded as
        self.channels = 2

        #مقدار دهی برای حالت فعال یا غیر فعال انتخاب زبان برای بخش GPTHNAI
# Value for active or inactive mode of language selection for gpthnai section
        self.LanguageSelectionForGPTHNAIState = "normal"

        #ایجاد یک متغییر برای یافتن محل کنونی اجرا شدن فایل
# Create a variable to find the current location of the file
        dir_path = os.path.dirname(os.path.realpath(__file__))

        #ایجاد متغییر های حاوی آیکون ها برای قرار دادن آنها در کلید ها
# Create variables containing icons to put them in keys
        self.CopyIcon = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\copy_384px.png"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\copy_384px.png"),
                                  size=(20, 20))
        
        self.PasteIcon = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\paste_384px.png"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\paste_384px.png"),
                                  size=(20, 20))
        
        self.SendIcon = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\sent_384px.png"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\sent_384px.png"),
                                  size=(20, 20))
        
        self.TalkingStart = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\record_384px.png"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\record_384px.png"),
                                  size=(384, 384))
        
        self.TalkingStop = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\stop_circled_384px.png"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\stop_circled_384px.png"),
                                  size=(384, 384))
        
        self.TTSStart = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\voice_384px.png"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\voice_384px.png"),
                                  size=(20, 20))
        
        self.TTSStop = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\stop_circled_384px.png"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\stop_circled_384px.png"),
                                  size=(20, 20))
        self.ImageAI = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\night_landscape.png"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\night_landscape.png"),
                                  size=(20, 20))
        
        self.InfoIcon = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\info_384px.png"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\info_384px.png"),
                                  size=(20, 20))
        
        self.SettingIcon = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\settings_384px.png"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\settings_384px.png"),
                                  size=(20, 20))
        
        self.HelpIcon = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\help_384px.png"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\help_384px.png"),
                                  size=(20, 20))
        
        self.VideoTutorial = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\video_384px.png"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\video_384px.png"),
                                  size=(20, 20))
        
        self.UpgradeIcon = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\upgrade_384px.png"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\upgrade_384px.png"),
                                  size=(20, 20))
        
        self.ClearIcon = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\clear_symbol_192px.png"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\clear_symbol_192px.png"),
                                  size=(20, 20))
        
        self.EmailIcon = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\GmailLogo_192px.png"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\GmailLogo_192px.png"),
                                  size=(20, 20))
        
        self.WebIcon = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\website_192px.png"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\website_192px.png"),
                                  size=(20, 20))
        
        self.GPT4VSGPT3IMG = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\GPT-4.jpg"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\GPT-4.jpg"),
                                  size=(851.2, 116.2))
        
        self.GPT4VSGPT3IMG_en = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\GPTTESTTakers.png"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\GPTTESTTakers.png"),
                                  size=(851.2, 116.2))
        
        self.FullEditionOnIcon = customtkinter.CTkImage(dark_image=Image.open(f"{dir_path}\\Icons\\ok_384px.png"),
                                  light_image=Image.open(f"{dir_path}\\Icons\\ok_384px.png"),
                                  size=(20,20))


        # مقدار دهی اولیه برای انتخاب زبان برای بخش GPTHNAI
# Initial value to choose the language for the gpthnai section
        self.LanguageSelectionChoice = "فارسی"

        #مقدار دهی اولیه برای اینکه حالت ساخت عکس فعال می باشد یا نه
# Initial value to whether or not the photo mode is enabled or not
        self.IMGGENERATION = False

        #تعریف متغییر برای قرار دادن آدرس کامل فایل
# Definition of variable to put the full file address
        self.full_path = ""

        #ساخت متغییر برای تایین وضیعت کامل بودن نسخه یا نه
# Making variables to determine the complete status of the version or not
        self.Full_Edition = False

        #ساخت یک لیست برای انتخاب مدل زبانی
# Build a list to select a language model
        self.AIMODEL_List = ["Chat GPT 3.5"]

        self.Application_Language = "fa"

        self.Images_For_Vision_List = []

        #دکمه فعالسازی/غیرفعالسازی حالت عکس
# Photo Mode Activation/Disable button
        self.IMGGENERATIONBUTTON = customtkinter.CTkButton(master=self,text="", fg_color="#51829B" , image=self.ImageAI,width=20, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: Drag_and_Drop())
        
        #ساختن یک دیکشنری برای اینکه اطلاعات را بطور دستی به ای پی ای مورد نظر ارسال کنیم قابل توجه است که این نوع ارسال در وبسایت خود ای پی ای در قسمت Docs موجود می باشد
# Making a dictionary to manually send information to the desired APA is noteworthy that this type of submission is available on your website in the DOCS section.
        self.headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
                }

        #ساختن یک تابع برای اینکه پیام ها و فایل های تصویری را در یک ساختار مناسب و مورد قبول ای پی ای پیاده سازی کرده و به حافظه ی هوش مصنوعی بیافزاید
# Making a function to implement messages and image files in an appropriate, accepted structure and add to artificial intelligence memory
        def process_content(role,text,messages,image_list=None):
            text_content = text

            #اگر لیست تصلویر خالی نبود
# If the listing of the Esteghir was not blank
            if image_list != None:
                base64_images = [(encode_image(image_path), get_file_extension(image_path)) for image_path in image_list]

                content = [
                    {
                        "type": "text",
                        "text": text_content
                    }
                    ] + [
                    {
                        "type": "image_url",
                        "image_url": {
                        "url": f"data:image/{file_extension[1::]};base64,{base64_image}"
                    }
                    } for base64_image, file_extension in base64_images
                    ]
            else:

                content = [
                    {
                    "type": "text",
                    "text": text_content
                    }
                    ]

                # ساختار پایانی پیام
# The final structure of the message
            message = {
                    "role": role,
                    "content": content
                }

            messages.append(message)
        #ساختن یک تابع برای اینکه پیام ها را در یک ساختار مناسب و مورد قبول ای پی ای پیاده سازی کرده و به حافظه ی هوش مصنوعی بیافزاید دقت کنید تفاوت این تابع با تابع قبلی در این است که این تابع پیام های غیر تصویری را ساختار بندی می کند
# Build a function to implement messages in an appropriate, accepted structure and add to artificial intelligence memory.
        def process_content_Streaming(role,text,messages,image_list=None):
            text_content = text

                # Final message structure
            message = {
                    "role": role,
                    "content": text_content
                }

            messages.append(message)

        def get_file_extension(file_path):
            file_extension = os.path.splitext(file_path)[1]
            return file_extension


        # تابع برای رمز گذاری تصاویر
# Function for encryption images
        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
            
            #تابع برای انتقال به تسخه فارسی و کامل برنامه
# Function to transfer to the Persian version of the program
        def ConfigureFullEdition_fa():
            self.AIMODEL_List = ["Chat GPT 3.5","Chat GPT 4"]
            self.UpgradeAccount.configure(text=render_text("  کامل   "),image=self.FullEditionOnIcon,fg_color="#55AD9B",hover_color="#55AD9B")
            self.IMGGENERATIONBUTTON.grid(row=3, column=2, padx=2, pady=2)
            self.AIMODEL = "gpt-4o"

            #تابع برای انتقال به نسخه انگلیسی و کامل برنامه
# Function to move to the English version and the full program
        def ConfigureFullEdition_en():
            self.AIMODEL_List = ["Chat GPT 3.5","Chat GPT 4"]
            self.UpgradeAccount.configure(text=render_text("Full Edition"),image=self.FullEditionOnIcon,fg_color="#55AD9B",hover_color="#55AD9B")
            self.IMGGENERATIONBUTTON.grid(row=3, column=2, padx=2, pady=2)
            self.AIMODEL = "gpt-4o"

            #تابع انتقال به نسخه کامل برنامه فارسی توجه کنید که فرق این تابع با تابع قبلی در این است که این تابع برای بررسی درستی و صحت کلید در قسمت ورودی کلید ساخته شده است 
# Note the transfer function of the full version of the Persian program, which is the difference between this function and the previous function is that this function is made to evaluate the correctness and accuracy of the key in the key input.
        def Upgration_fa():
            UpgradeKey = self.EnteryUpgrade.get()
            if UpgradeKey == "Khawrazmi":
                self.Full_Edition = True
                self.EAS.configure(text_color="#51da4c",text=render_text("برنامه با موفقیت به نسخه کامل ارتقا یافت."))
                ConfigureFullEdition_fa()
            else:
                self.EAS.configure(text_color="red",text=render_text("کد ویژه اشتباه می باشد."))

            1#کار همان تابع قبلی را انجام می دهد اما انگلیسی
        def Upgration_en():
            UpgradeKey = self.EnteryUpgrade.get()
            if UpgradeKey == "Khawrazmi":
                self.Full_Edition = True
                self.EAS.configure(text_color="#51da4c",text=render_text("The Program Is Fully Upgraded Now"))
                ConfigureFullEdition_en()
            else:
                self.EAS.configure(text_color="red",text=render_text("The Special Key Is Incorrect"))

        #تعریف تابع برای ایجاد افکت تایپ کردن
# Define function to create typing effects
        def typeit(widget, index, string):
            if len(string) > 0:
                widget.insert(index, string[0], "tag-right")
                if len(string) > 1:
                    index = widget.index("%s + 1 char" % index)

                    widget.after(100, typeit, widget, index, string[1:])

        #تعریف تابع برای پاک کردن حافظه ی هوش مصنوعی و همچنین پیام ها از بخش چت فریم این تابع همچنین حافظه ی هوش مصنوعی بخش GPTHNAI را هم پاک می کند
# Definition of the function to erase artificial intelligence memory as well as messages from the chat section of this function also erases the GPTHNAI section of the artificial intelligence memory.
        def ClearFrame():
            frame = self.ChatFrame
            for widget in frame.winfo_children():
                widget.destroy()
            self.current_room = "Default"
            self.current_roomGPTHNAI = "DefaultGPTHNAI"
            self.first_response = True
            self.conversations[self.current_room] = []
            self.conversations[self.current_roomGPTHNAI] = []

        #تعریف تابع برای کپی کردن
# Define the function to copy
        def copy_to_clipboard(text):
            self.clipboard_append(text)

        #تعریف تابع برای گرفتن مقدار قرار دادن آن در متغییر برای بخش انتخاب زبان قسمت GPTHNAI
# Define the function to get the amount of placement in the variable for the language selection section of the gpthnai section
        def LanguageSelection(choice):
            self.LanguageSelectionChoice = choice

        #تعریف تابع برای ارسال درخواست و دریافت تصویر ساخته شده توسط هوش مصنوعی
# Definition of function to submit request and receive image made by artificial intelligence
        def fetch_responseIMGGENERATION():
            #مقدار دهی متغییر به حالت True برای نشان جلو گیری از ارسال پیام توسط کاربر و ایجاد اختلال
# Variable value to TRUE mode to prevent the user from sending a message and disrupt
            self.sending = True
            
            #ارسال درخواست برای ساختن عکس به هوش مصنوعی
# Send request to make a photo to artificial intelligence
            show_info("Info","هوش مصنوعی در حال ساخت عکس می باشد")
            try:
                response = self.client.images.generate(
                prompt=self.ChatBoxEnteryValue,
                model="dall-e-3",
                n=1,
                size="1024x1024")
            except Exception as e:
                print(e)
                show_error("خطا در ساخت عکس", "خطا در ساختن عکس لطفا وضیعت دی ان اس خو درا چک کرده و برنامه را یکبار باز و بسته کنید")
            img_url = response.data[-1].url
            
            #ایجاد کادر و لیبل ها برای دریافت پیام از طرف هوش مصنوعی
# Create boxes and labels to receive message from artificial intelligence
            master = self.ChatFrame

            # ایجاد کادر
# Creating a box
            frame = customtkinter.CTkFrame(master, fg_color="#E0AED0",width=1400, **kwargs)
            frame.pack( padx=20, pady=20, anchor="e")

            # ایجاد لیبل ها یا همان ویدجت برای نوشتن متن
# Create labels or the same widget to write text
            master = frame
            label = customtkinter.CTkLabel(frame, text="AI",text_color="Black",font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            labeltext = customtkinter.CTkLabel(frame, text=render_text(f"{img_url} The generated image URL only exist for 60 minutes. You can download or save the image by going to this URL \n\n ادرس تصویر ساخته شده فقط برای 60 دقیقه معتبر است. شما می توانید به رفتن به این آدرس تصویر ساخته شده را دانلود و سا ذخیره نمایید"), width=1020,text_color="Black",font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            
            #ایجاد دکمه یا کلید برای کپی کردن متن
# Create button or key to copy the text
            CopyButton = customtkinter.CTkButton(master,text="", image=self.CopyIcon,width=50,fg_color="transparent", font=(self.CurrentFont, self.CurrentFontSize), command=lambda: copy_to_clipboard(img_url))
            
            labeltext.pack( padx=20, pady=5)  
            label.pack( padx=20, pady=5)
            CopyButton.pack(padx=2, pady=2)
            
            #افزودن پیام ارسال شده توسط هوش مصنوعی به حافظه ی هوش مصنوعی
# Adding Message Posted by AI to Artificial Intelligence Memory
            self.conversations[self.current_room].append({"role": "assistant", "content": f"{img_url} \n\n The generated image URL only exist for 60 minutes. You can download or save the image by going to this URL \n\n ادرس تصویر ساخته شده فقط برای 60 دقیقه معتبر است. شما می توانید به رفتن به این آدرس تصویر ساخته شده را دانلود و سا ذخیره نمایید"})
            
            #دانلود کردن تصویر توسط تابع و آدرس تصویر ارسال شده توسز هوش مصنوعی
# Download the image by the function and image address sent by Tassez Artificial Intelligence
            download_image(img_url)

            #باز کردن تصویر دانلود شده توسط محل آن که از تابع فوق مقدار دهی شده است
# Open the image downloaded by its location that is a value of the above function
            open_and_display_image(self.full_path)

            

            #فعال کردن کلید حالت تصویر هوش مصنوعی
# Enable the Image Mode of Artificial Intelligence Mode
            self.IMGGENERATIONBUTTON.configure(text="", state="normal")
            self.sending = False

            #ایجاد یک تول تیپ برای اینکه توضیحات کلید درحال هاور(Hover) دیده شود
# Create a Type -Tap to make the Hover key description (Hover) be seen
            Copy_Button_Tip = CTkToolTip(CopyButton, delay=0.25, message=render_text("کپی متن"), y_offset=-20)

            #تغییر متن محل نگه دار ورودی 
# Change the location of the input holder
            self.ChatEntery.configure(placeholder_text="متن مورد نظر خود را بنویسید")
            self.IMGGENERATIONBUTTON.configure(text="" , fg_color="#51829B")
            self.IMGGENERATION = False 


        #تعریف تابع دانلود تصویر
# Definition of image download function
        def download_image(url):
            try:
                
                # گرفتن زمان کنونی
# Getting the current time
                current_datetime = datetime.datetime.now()
                
                # فرمت کردن زمان کنونی
# Formatting the current time
                formatted_datetime = current_datetime.strftime('%Y-%m-%d-%H-%M')

                # ارسال یک در خواست برای دانلود تصویر از آدرس گرفته شده
# Send a request to download the image from the address taken
                try:
                    response = requests.get(url)
                    response.raise_for_status()  

                    #چک کردن وضیعت برای قابل دانلود بودن یا نبودن
# Checking the situation to be downloadable or not
                    content_type = response.headers.get('content-type')
                    if not content_type:
                        #ایجاد پیغام ارور برای دانلود در صورت دانلود نشده
# Create Error Message to Download if Unpamrated
                        raise ValueError("Could not determine the file type from the server response.")
                except:
                    pass

                

                # قرار دادن پسوند فایل دانلود شده البته اگر بود
# Putting the downloaded file extension of course if it was
                if 'image/jpeg' in content_type:
                    extension = 'jpg'
                elif 'image/png' in content_type:
                    extension = 'png'
                elif 'image/gif' in content_type:
                    extension = 'gif'
                else:
                    extension = "webp"

                # مقدار دهی و ایجاد یک متغییر برای آدرس کامل تصویر دانلود شده
# Value and create a variable for the complete downloaded image address
                self.full_path = f"Generated_Images\\{formatted_datetime}.{extension}"

                # مطمئن شددن از اینکه آیا فولدر وجود دارد یا نه
# To make sure whether there is a folder or not
                os.makedirs(os.path.dirname(self.full_path), exist_ok=True)

                # دانلود 
# Download
                with open(self.full_path, 'wb') as file:
                    file.write(response.content)
                #اگر ارور داد بگذر و ارور نده
# If the Error Draws and does not.
            except Exception as e:
                pass
        
        #ایجاد یک تابع برای باز کردن و نمایش تصویر
# Create a function to open and display the image
        def open_and_display_image(file_path):
            try:
                # Open the image file
                with Image.open(file_path) as img:
                    # Display the image
                    img.show()
                    
            except IOError as e:
                pass

            #ایجاد یک تابع برای پخش صدا از طریق نام فایل در همین پوشه
# Create a function to play sound through the file name in the same folder
        def play_sound(FileName):

            #تعریف یک متغییر برای ذخیره مقدار کلید در آن برای تغییرات
# Define a variable to save the key value in that for changes
            button = self.GPTHNAIPersianRecordingButton
            sound_file = FileName
            sound = pygame.mixer.Sound(sound_file)
            sound.play(loops=0) #پخش کردن صدا

            #چنل 5 چنل صدا است
# Channel 5 is the channel
            voice = pygame.mixer.Channel(5)

            #چک کردن برای اینکه ببینیم برنامه در حال پخش صدا است یا نه         
# Check to see if the app is playing sound or not
            if not voice.get_busy():
                #فعال کردن انتخاب گر زبان
# Activate the language selector
                self.LanguageSelectionForGPTHNAIState = "normal"
                button.configure(state="normal")
            
            #یک تابع برای تبدیل صدا به متن توسط هوش مصنوعی
# A function to convert sound to text by artificial intelligence
        def SpeechTranscription(audio_file):

            #ایجاد یک متغییر برای یافتن محل کنونی اجرا شدن فایل
# Create a variable to find the current location of the file
            dir_path = os.path.dirname(os.path.realpath(__file__))

            #نام پوشه فایل های صدای کاربر
# Name of User Voice File Folder
            folder_name = "InputAudio"

            #محل پوشه فایل ها صدای کاربر
# File folder
            PathToFolder = f"{dir_path}\\{folder_name}"

            #بررسی برای تایین موجودیت پوشه یا نه
# Checking for the existence of folder or not
            if os.path.exists(PathToFolder):

                #حذف کردن داده های پوشه برای ایجاد داده های جدید در آینده
# Remove folder data to create new data in the future
                for filename in os.listdir(PathToFolder):
                    file_path = os.path.join(PathToFolder, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        pass

                

            #اگر پوشه وجود نداشت
# If the folder did not exist
            else:

                #ساخت پوشه جدید
# Making a new folder
                os.makedirs(PathToFolder)

            #وارد کردن فایل صوتی اصلی به برنامه
# Enter the original audio file to the app
            audio_file = AudioSegment.from_mp3(audio_file)

            #گرفتن انداره فایل صوتی
# The audio file.
            DurationOfAudio = audio_file.duration_seconds

            #تعداد دقیقه ها در فایل صوتی
# The number of minutes in the audio file
            CountsOfAudio = int(DurationOfAudio // 60)

            #تعداد به اضافه یک زیرا ممکن است داده متغییر قبل اعشاری می بوده باشد
# Number plus one because it may have been the variable data before the decimal
            CountsOfAudio += 1

            #دقیقه آغازین قیچی کردن فایل صوتی
# The first minute of scissing the audio file
            startMin = 0

            #دقیقه پایان قیچی کردن فایل صوتی
# Minute ending the audio file scissors
            endMin = 1

            #انجام تقسیمات لازم و برش فایل به تعداد دقیقه ها به علاوه آن یک دقیقه ناقص
# Do the necessary divisions and cut the file to the number of minutes plus it is an incomplete minute
            for i in range(CountsOfAudio):
                filename = "InputAudio"
                if i == CountsOfAudio-1:
                    splited_audio = audio_file[(startMin+i)*60*1000::]
                    splited_audio.export(f"{PathToFolder}\\{filename}-{i}.mp3", format="mp3")
                    break
                
                else:
                    splited_audio = audio_file[(startMin+i)*60*1000:(endMin+i)*60*1000]
                    splited_audio.export(f"{PathToFolder}\\{filename}-{i}.mp3", format="mp3")

            #تعریف یک متغییر برای ذخیره مقدار کلید در آن برای تغییرات
# Define a variable to save the key value in that for changes
            button = self.GPTHNAIPersianRecordingButton

            #اگر زبان در حالت فارسی بود گفتار به متن را به حالت فارسی بگذار
# If the language was in Persian, put the text in Persian in Persian
            if "فارسی" in self.LanguageSelectionChoice:

                #لیستی برای جکع آوری تکه های تبدیل گفتگو به متن
# List to collect converting dialogs to text
                Transcription_List = []
                
                #ارسال در خواست به هوش مصنوعی
# Send request to artificial intelligence
                for i in range(CountsOfAudio):
                #باز کردن فایل صدا برای تبدیل
# Open the sound file to convert
                    audio_file = open(f"{PathToFolder}\\{filename}-{i}.mp3", "rb")
                    transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    language="fa",
                    file=audio_file)

                    Transcription_List.append(transcript.text)

                Complete_Transcription = " ".join(Transcription_List)

                #اضافه کردن متن گفته شده توسط کاربر به حافظه ی هوش مصنوعی
# Add the text said by the user to the memory of artificial intelligence
                self.conversations[self.current_roomGPTHNAI].append({"role": "user", "content": Complete_Transcription})

                #ارسال درخواست به هوش مصنوعی برای پاسخ گویی به متن کاربر
# Send request to artificial intelligence to answer user text
                stream = self.client.chat.completions.create(
                model=self.AIMODEL,
                messages=self.conversations[self.current_roomGPTHNAI])

                #دریافت پاسخ هوش مصنوعی
# Receive Artificial Intelligence Answer
                response = stream.choices[0].message.content

                #ایجاد یک تغییر و ذخیره محلل ذخیره کردن صدای ارسال شده ی هوش مصنوعی
# Create a change and save the site. Save the voice sent by artificial intelligence
                speech_file_path = Path(__file__).parent / "GPTHNAIOUTPUT.mp3"

                #ارسال در خواست به هوش مصنوعی برای دریافت صدای متن به گفتار
# Send request to artificial intelligence to receive text voice to speech
                with self.client.audio.speech.with_streaming_response.create(
                model="tts-1",
                voice="alloy",
                response_format="wav",
                input=response
                ) as audioresponse:
                    
                    #ذخیره کردن فایل صوتی
# Save the audio file
                    audioresponse.stream_to_file(speech_file_path)

                #پخش کردن فایل صوتی توسط  تابع
# Playing the audio file by the function
                play_sound(speech_file_path)

            #اگر زبان در حالت فارسی بود گفتار به متن را به حالت فارسی بگذار
# If the language was in Persian, put the text in Persian in Persian
            elif "زبان" in self.LanguageSelectionChoice:

                Transcription_List = []
                
                #ارسال در خواست به هوش مصنوعی
# Send request to artificial intelligence
                for i in range(CountsOfAudio):
                #باز کردن فایل صدا برای تبدیل
# Open the sound file to convert
                    audio_file = open(f"{PathToFolder}\\{filename}-{i}.mp3", "rb")
                    transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file)

                #ساختار بندی کردن و چسباندن کلمات و تکه ها به یکدیگر 
# Structuring and paste words and pieces to each other
                    Transcription_List.append(transcript.text)

                Complete_Transcription = " ".join(Transcription_List)

                #اضافه کردن متن گفته شده توسط کاربر به حافظه ی هوش مصنوعی
# Add the text said by the user to the memory of artificial intelligence
                self.conversations[self.current_roomGPTHNAI].append({"role": "user", "content": Complete_Transcription})

                #ارسال درخواست به هوش مصنوعی برای پاسخ گویی به متن کاربر                stream = self.client.chat.completions.create(
# Send request to artificial intelligence to respond to user text stream = self.client.chat.completions.create (
                stream = self.client.chat.completions.create(
                model=self.AIMODEL,
                messages=self.conversations[self.current_roomGPTHNAI])

                #دریافت پاسخ هوش مصنوعی
# Receive Artificial Intelligence Answer
                response = stream.choices[0].message.content

                #ایجاد یک تغییر و ذخیره محلل ذخیره کردن صدای ارسال شده ی هوش مصنوعی
# Create a change and save the site. Save the voice sent by artificial intelligence
                speech_file_path = Path(__file__).parent / "GPTHNAIOUTPUT.mp3"
                
                #ارسال در خواست به هوش مصنوعی برای دریافت صدای متن به گفتار
# Send request to artificial intelligence to receive text voice to speech
                with self.client.audio.speech.with_streaming_response.create(
                model="tts-1",
                voice="alloy",
                response_format="wav",
                input=response
                ) as audioresponse:
                    #ذخیره کردن فایل صوتی
# Save the audio file
                    audioresponse.stream_to_file(speech_file_path)
                
                #پخش کردن فایل صوتی توسط  تابع
# Playing the audio file by the function
                play_sound(speech_file_path)

                #فعال کردن انتخاب گر زبان
# Activate the language selector
                self.LanguageSelectionForGPTHNAIState = "normal"
                button.configure(state="normal")
                RecordPasteButton_Tip = CTkToolTip(button, delay=0.25, message=render_text("ضبط صدا"), y_offset=-20)

            #ایجاد تابع برای ضبط کردن صدا
# Create a function to record sound
        def toggle_recording():
            #تعریف یک متغییر برای ذخیره مقدار کلید در آن برای تغییرات
# Define a variable to save the key value in that for changes
            button = self.GPTHNAIPersianRecordingButton
            
            #غیر فعال کردن انتخاب گر زبان
# Disable Language Selection
            self.LanguageSelectionForGPTHNAIState = "disabled"

            #اگر حالت ضبط فعال نیست
# If the recording mode is not enabled
            if not self.is_recording:

                #حالت ضبط را فعال کن
# Enable recording mode
                self.is_recording = True

                # ایجاد متغییر ها برای ضبط
# Create variables for recording
                self.GPTHNAIPersianRecordingButton.configure(image=self.TalkingStop)
                self.AudioChunks = []
                # شروع کردن برای ضبط
# Start to record
                threading.Thread(target=record).start()
            
            #اگر حالت ضبط فعال است
# If the recording mode is enabled
            else:

                #کلید را به غیر فعال کن 
# Keep the key to disable
                button.configure(state="disabled")

                #حالت ضبط را غیر فعال کن
# Disable the recording mode
                self.is_recording = False
                self.GPTHNAIPersianRecordingButton.configure(image=self.TalkingStart)
                # صدا را ذخیره کن
# Save the sound
                save_file()
            Button_Tip = CTkToolTip(button, delay=0.25, message=render_text("ضبط صدا"), y_offset=-20)



        #ایجاد یک تابع برای ضبط صدا
# Create a function for sound recording
        def record():
            """صدا را از میکروفون ضبط میکند"""

            with sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=audio_callback):
                while self.is_recording:
                    sd.sleep(100)  # Wait briefly to reduce CPU usage

        def audio_callback(indata, frames, time, status):
            """این برای این است که تکه های صدا را جمع کند"""
            self.AudioChunks.append(indata.copy())

        def save_file():
            """ذخیره کردن فایل صوتی"""
            

            filename = 'GPTHNAIINPUT_Complete.mp3'
            data = np.concatenate(self.AudioChunks, axis=0)
            sf.write(filename, data, self.samplerate)
            SpeechTranscription(filename)
        
        #تابع برای تعویض نوع فونت
# Function to replace the font type
        def FontSelection(choice):
            try:
                self.CurrentFont = choice
                self.CurrentFontSize = int(choice)
                self.SettingMainLabel.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                self.SettingAppereanceLabel.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                self.ChatEntery.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                self.FontsComboBoxLabel.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                self.FontsStyleComboBoxLabel.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                self.FontsSizeComboBoxLabel.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                self.SendButton.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                self.PasteButton.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                self.GPTHNAIPersianRecordingButton.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                self.MainChatTabview.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                self.GPTHNAI.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                self.MainTabview.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                self.LanguageSelectionForGPTHNAI.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))

            except:
                pass

            #تابع برای تعویض استایل فونت
# Function to replace font style
        def FontStyleSelection(choice):
            self.CurrentFontSize = int(choice)
            self.SettingMainLabel.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.SettingAppereanceLabel.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.ChatEntery.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.FontsComboBoxLabel.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.FontsStyleComboBoxLabel.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.FontsSizeComboBoxLabel.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.SendButton.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.PasteButton.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.GPTHNAIPersianRecordingButton.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.MainChatTabview.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.GPTHNAI.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.MainTabview.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.LanguageSelectionForGPTHNAI.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))


            #تابع برای تعویض اندازه فونت
# Function to replace font size
        def FontSizeSelection(choice):
            self.CurrentFontSize = int(choice)
            self.SettingMainLabel.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.SettingAppereanceLabel.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.ChatEntery.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.FontsComboBoxLabel.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.FontsStyleComboBoxLabel.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.FontsSizeComboBoxLabel.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.SendButton.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.PasteButton.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.GPTHNAIPersianRecordingButton.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.MainChatTabview.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.GPTHNAI.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.MainTabview.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.LanguageSelectionForGPTHNAI.configure(font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            


        # تابع جایگذاری متن از کلیپبورد
# The text function of the clipboard
        def paste_from_clipboard(Entery):
            #جاگذاری متن از کلیپبورد
# The placement of the text from the clipboard
            try:
                clipboard_text = self.clipboard_get()  # فراخوانی کلیپبورد
                Entery.insert("end", clipboard_text) 
            except tk.TclError:
                pass
        def fetch_response():

            #یک تابع جهت ساخت دکمه پخش صدا
# A function to build the sound play button
            def SoundPlayButton(text):
                button = SoundCreation
                speech_file_path = Path(__file__).parent / "TextAudioOutPut.mp3"
                with self.client.audio.speech.with_streaming_response.create(
                model="tts-1",
                voice="alloy",
                response_format="wav",
                input=text
                ) as audioresponse:
                    audioresponse.stream_to_file(speech_file_path)
                sound_file = speech_file_path
                sound = pygame.mixer.Sound(sound_file)
                sound.play(loops=0)  # صوت را یکبار پخش کند


            response_text = ""

            #اگر لیست تصاویری که برای تحلیح تصائیر است خالی بود
# If the list of images that was for the analysis of the images was empty
            if len(self.Images_For_Vision_List) != 0:

                
                #ساختار بندی و ارسال پیام حاوی تصاویر بصورت دستی به ای پی ای
# Structuring and sending messages containing images manually to APA
                data = {
                    "model": self.AIMODEL,
                    "messages": self.conversations[self.current_room],
                    "max_tokens": 500
                    }

                self.Images_For_Vision_List = []
                
                response = requests.post("https://api.openai.com/v1/chat/completions", headers=self.headers, json=data)

                json_data = response.json()
                
                response_text = json_data['choices'][0]['message']['content']
                response_text_for_conversation = json_data['choices'][0]['message']['content']
                TextClipboardReady = ""
                master = self.ChatFrame
                frame = customtkinter.CTkFrame(master, width=1400,fg_color="#AAD7D9", **kwargs)
                frame.pack( padx=20, pady=20)

                # یک لیبل به فریم اضافه میکند
# Adds a label to the frame

                label = customtkinter.CTkLabel(frame, text="AI",text_color="Black",font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                labeltext = customtkinter.CTkLabel(frame, text="", width=1330,text_color="Black", pady=10, justify="center",font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                CopyButton = customtkinter.CTkButton(master=frame,text="", image=self.CopyIcon,width=50,fg_color="transparent", font=(self.CurrentFont, self.CurrentFontSize), command=lambda: copy_to_clipboard(TextClipboardReady))
                CopyButton.pack(padx=2, pady=2)
                label.pack( padx=20, pady=5)
                labeltext.pack(pady=5)
                Codeframe = customtkinter.CTkFrame(master, width=0,fg_color="#E493B3", **kwargs)
                labelCodeLanguage = customtkinter.CTkLabel(Codeframe, text="",text_color="Black",font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))  
                LabelCode = customtkinter.CTkLabel(Codeframe, text="", width=1330,text_color="Black", pady=10,font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                CodeCopyButton = customtkinter.CTkButton(master=Codeframe,text="",fg_color="transparent", image=self.CopyIcon,width=50, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: copy_to_clipboard(LabelCode.cget("text")))
                
                    
                # دریافت کردن تکه کلمه ها از AI
# Receive the piece of words from AI
                
                        
                if "۰" in response_text:
                    response_text = response_text.replace("۰","0")

                if "۱" in response_text:
                    response_text = response_text.replace("۱","1")

                if "۲" in response_text:
                    response_text = response_text.replace("۲","2")

                if "۳" in response_text:
                    response_text = response_text.replace("۳","3")

                if "۴" in response_text:
                    response_text = response_text.replace("۴","4")

                if "۵" in response_text:
                    response_text = response_text.replace("۵","5")

                if "۶" in response_text:
                    response_text = response_text.replace("۶","6")

                if "۷" in response_text:
                    response_text = response_text.replace("۷","7")

                if "۸" in response_text:
                    response_text = response_text.replace("۸","8")

                if "۹" in response_text:
                    response_text = response_text.replace("۹","9")

                if "؟" in response_text:
                    response_text = response_text.replace("؟","?")
                if "!" in response_text:
                    response_text = response_text.replace("!","!")
                #شرط نبودن متن
# The condition of the text is not
                if not response_text.startswith("```"):
                    if "```" not in response_text:
                        words = response_text.split()
                        wrapped_lines = []
                        line = ''
                        for word in words:
                            text_line = line + word + ' '  # اضافه کردن فاصله
                            linewidth = self.currentFontMixed.measure(text=text_line)
                            if linewidth < 1250:
                                line = text_line  # درصورت عدم خطا ادامه بده
                            else:
                                # تابع طولانی بودن متن - اینتر زدن
# Function of the long text - Inter
                                wrapped_lines.append(line)
                                line = word + ' '  # شروع لاین جدید از کلمه آخر
                        if line:
                            wrapped_lines.append(line)

                        TextClipboardReady = ('\n\n'.join(wrapped_lines))
                        labeltext.configure(text=render_text(('\n\n'.join(wrapped_lines))))
                    if "```" in response_text:
                        splited = response_text.split("```")
                        #اگر طول لیست بر دو بخش پذیر نباشد پس مقدار های متغیر را از لیست ریافت کرده و در تابع جایگذاری کن
# If the list length is not over two segments, then take the variable value from the list and place it in the function
                        if len(splited) % 2 != 0:
                            codeStructure = splited[len(splited)-2]
                            CodeSplited = codeStructure.split("\n")
                            ProgrammingLanguage = CodeSplited[0]
                            MainCode = codeStructure.replace(ProgrammingLanguage, "")
                            CopyButton.pack( padx=20, pady=20)
                            Codeframe.pack( padx=20, pady=20)
                            labelCodeLanguage.pack( padx=20, pady=5)
                            LabelCode.pack(pady=5)
                            labelCodeLanguage.configure(text=ProgrammingLanguage)
                            LabelCode.configure(text=MainCode)
                            TextSplited = ""
                            for i in range(len(splited)):
                                if i % 2 == 0:
                                    TextSplited += splited[i]

                            words = TextSplited.split()
                            wrapped_lines = []
                            line = ''
                            for word in words:
                                text_line = line + word + ' '  #اضافه کردن فاصله بین کلمات
                                linewidth = self.currentFontMixed.measure(text=text_line)
                                if linewidth < 1250:
                                    line = text_line  # درصورت عدم خطا ادامه دهبد
                                else:
                                    wrapped_lines.append(line)
                                    line = word + ' ' 
                            if line:
                                wrapped_lines.append(line)
                            TextClipboardReady = ('\n\n'.join(wrapped_lines))
                            labeltext.configure(text=render_text(('\n\n'.join(wrapped_lines))))
                #تابع شناسایی Bash ها از ورودی پیام ها جهت نوشتن بصورت کد برنامه نویسی
# Bash Identification Function from Message Input to Write in Programming Code
                if response_text.startswith("```"):
                    if "```" in response_text:
                        splited = response_text.split("```")
                        del splited[0]
                        #اگر طول لیست بر دو بخش پذیر نباشد پس مقدار های متغیر را از لیست ریافت کرده و در تابع جایگذاری کن
# If the list length is not over two segments, then take the variable value from the list and place it in the function
                        if len(splited) % 2 == 0:
                            codeStructure = splited[len(splited)-2]
                            CodeSplited = codeStructure.split("\n")
                            ProgrammingLanguage = CodeSplited[0]
                            MainCode = codeStructure.replace(ProgrammingLanguage, "")
                            labelCodeLanguage.configure(text=ProgrammingLanguage)
                            LabelCode.configure(text=MainCode)
                            TextSplited = ""
                            for i in range(len(splited)):
                                if i % 2 == 0:
                                    TextSplited += splited[i]
                            #جدا کردن کلمات متغیر بر حسب فاصله از یکدیگر
# Separate variable words by distance from each other
                            words = TextSplited.split()
                            wrapped_lines = []
                            line = ''
                            for word in words:
                                text_line = line + word + ' '  # اضافه کردن فاصله
                                linewidth = self.currentFontMixed.measure(text=text_line)
                                if linewidth < 1250:
                                    line = text_line  # اگر خطا وجود ندارد ادامه بده
                                else:
                                    wrapped_lines.append(line)
                                    line = word + ' '  # کد بعدی را از آخرین کلمه شروع کن
                            if line:
                                wrapped_lines.append(line)
                            TextClipboardReady = ('\n\n'.join(wrapped_lines))
                            labeltext.configure(text=render_text(('\n\n'.join(wrapped_lines))))
                
                #خالی کردن لیست تصوایر مورد نیاز برای تحلیل تصوایر برای اشکال زدایی تابع ارسال پیام
# Empty the Image List Required to Analyze the Image for Disruption of the Message Send Function
                self.Images_For_Vision_List = []

                #شناسایی پیام های ساده از Bash های ارسالی از سمت API
# Identify simple messages from Bashs sent by API
                if "```" not in response_text:
                    words = response_text.split()
                    wrapped_lines = []
                    line = ''
                    for word in words:
                        text_line = line + word + ' '  # اضافه کردن فاصله
                        linewidth = self.currentFontMixed.measure(text=text_line)
                        if linewidth < 1250:
                            line = text_line 
                        else:
                            wrapped_lines.append(line)
                            line = word + ' '  
                    if line:
                        wrapped_lines.append(line)
                    TextClipboardReady = ('\n\n'.join(wrapped_lines))
                    labeltext.configure(text=render_text(('\n\n'.join(wrapped_lines))))
                if "```" in response_text:
                    splited = response_text.split("```")
                    #اگر طول لیست بر دو بخش پذیر نباشد پس مقدار های متغیر را از لیست ریافت کرده و در تابع جایگذاری کن
# If the list length is not over two segments, then take the variable value from the list and place it in the function
                    if len(splited) % 2 != 0:
                        codeStructure = splited[len(splited)-2]
                        CodeSplited = codeStructure.split("\n")
                        ProgrammingLanguage = CodeSplited[0]
                        MainCode = codeStructure.replace(ProgrammingLanguage, "")
                        CodeCopyButton.pack( padx=20, pady=20)
                        Codeframe.pack( padx=20, pady=20)
                        labelCodeLanguage.pack( padx=20, pady=5)
                        LabelCode.pack(pady=5)
                        labelCodeLanguage.configure(text=ProgrammingLanguage)
                        LabelCode.configure(text=MainCode)
                        TextSplited = ""
                        for i in range(len(splited)):
                            if i % 2 == 0:
                                TextSplited += splited[i]
                        words = TextSplited.split()
                        wrapped_lines = []
                        line = ''
                        for word in words:
                            text_line = line + word + ' ' # اضافه کردن فاصله
                            linewidth = self.currentFontMixed.measure(text=text_line)
                            if linewidth < 1250:
                                line = text_line 
                            else:
                                #اگر طول لیست بر دو بخش پذیر نباشد پس مقدار های متغیر را از لیست ریافت کرده و در تابع جایگذاری کن
# If the list length is not over two segments, then take the variable value from the list and place it in the function
                                wrapped_lines.append(line)
                                line = word + ' '  
                        if line:
                            wrapped_lines.append(line)
                        TextClipboardReady = ('\n\n'.join(wrapped_lines))
                        labeltext.configure(text=render_text(('\n\n'.join(wrapped_lines))))
                #شناسایی Bash های داخل کد
# Identify Bash inside the code
                if response_text.startswith("```"):
                    if "```" in response_text:
                        splited = response_text.split("```")
                        del splited[0]
                        #اگر طول لیست بر دو بخش پذیر نباشد پس مقدار های متغیر را از لیست ریافت کرده و در تابع جایگذاری کن
# If the list length is not over two segments, then take the variable value from the list and place it in the function
                        if len(splited) % 2 == 0:
                            codeStructure = splited[len(splited)-2]
                            CodeSplited = codeStructure.split("\n")
                            ProgrammingLanguage = CodeSplited[0]
                            MainCode = codeStructure.replace(ProgrammingLanguage, "")
                            labelCodeLanguage.configure(text=ProgrammingLanguage)
                            LabelCode.configure(text=MainCode)
                            TextSplited = ""
                            for i in range(len(splited)):
                                if i % 2 == 0:
                                    TextSplited += splited[i]

                            words = TextSplited.split()
                            wrapped_lines = []
                            line = ''
                            for word in words:
                                text_line = line + word + ' '  #اضافه کردن فاصله
                                linewidth = self.currentFontMixed.measure(text=text_line)
                                if linewidth < 1250:
                                    line = text_line
                                else:
                                    #اگر طول لیست بر دو بخش پذیر نباشد پس مقدار های متغیر را از لیست ریافت کرده و در تابع جایگذاری کن
# If the list length is not over two segments, then take the variable value from the list and place it in the function
                                    wrapped_lines.append(line)
                                    line = word + ' '  
                            if line:
                                wrapped_lines.append(line)
                            TextClipboardReady = ('\n\n'.join(wrapped_lines))
                            labeltext.configure(text=render_text(('\n\n'.join(wrapped_lines))))
                #ساخت دکمه ایجاد صوت
# Build the button creation of audio
                SoundCreation = customtkinter.CTkButton(master=frame,text="", image=self.TTSStart,width=50,fg_color="transparent", font=(self.CurrentFont, self.CurrentFontSize), command=lambda: SoundPlayButton(TextClipboardReady))
                SoundCreation.pack(padx=2, pady=2)

                # ایجاد روم جدید روی API و اجرای دستورات مورد نیاز
# Create new Rome on API and execute the required commands
                process_content("assistant",response_text_for_conversation,self.conversations[self.current_room])
                process_content_Streaming("assistant",response_text_for_conversation,self.conversations[self.current_roomS])
                self.SendButton.configure(text="")
                self.sending = False


            else:
                #پیام در حال ارسال است
# The message is being sent.
                self.sending = True
                stream = self.client.chat.completions.create(
                    model=self.AIMODEL,
                    messages=self.conversations[self.current_roomS],
                        stream=True)
                
                response_text = ""
                TextClipboardReady = ""
                master = self.ChatFrame
                frame = customtkinter.CTkFrame(master, width=1400,fg_color="#AAD7D9", **kwargs)
                frame.pack( padx=20, pady=20)

                # یک لیبل به فریم اضافه میکند
# Adds a label to the frame

                label = customtkinter.CTkLabel(frame, text="AI",text_color="Black",font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                labeltext = customtkinter.CTkLabel(frame, text="", width=1330,text_color="Black", pady=10, justify="center",font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                CopyButton = customtkinter.CTkButton(master=frame,text="", image=self.CopyIcon,width=50,fg_color="transparent", font=(self.CurrentFont, self.CurrentFontSize), command=lambda: copy_to_clipboard(TextClipboardReady))
                CopyButton.pack(padx=2, pady=2)
                label.pack( padx=20, pady=5)
                labeltext.pack(pady=5)
                Codeframe = customtkinter.CTkFrame(master, width=0,fg_color="#E493B3", **kwargs)
                labelCodeLanguage = customtkinter.CTkLabel(Codeframe, text="",text_color="Black",font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))  
                LabelCode = customtkinter.CTkLabel(Codeframe, text="", width=1330,text_color="Black", pady=10,font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                CodeCopyButton = customtkinter.CTkButton(master=Codeframe,text="",fg_color="transparent", image=self.CopyIcon,width=50, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: copy_to_clipboard(LabelCode.cget("text")))
                
                    
                # دریافت کردن تکه کلمه ها از AI
# Receive the piece of words from AI
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        response_text += chunk.choices[0].delta.content
                        
                        if "۰" in response_text:
                            response_text = response_text.replace("۰","0")

                        if "۱" in response_text:
                            response_text = response_text.replace("۱","1")

                        if "۲" in response_text:
                            response_text = response_text.replace("۲","2")

                        if "۳" in response_text:
                            response_text = response_text.replace("۳","3")

                        if "۴" in response_text:
                            response_text = response_text.replace("۴","4")

                        if "۵" in response_text:
                            response_text = response_text.replace("۵","5")

                        if "۶" in response_text:
                            response_text = response_text.replace("۶","6")

                        if "۷" in response_text:
                            response_text = response_text.replace("۷","7")

                        if "۸" in response_text:
                            response_text = response_text.replace("۸","8")

                        if "۹" in response_text:
                            response_text = response_text.replace("۹","9")

                        if "؟" in response_text:
                            response_text = response_text.replace("؟","?")
                        if "!" in response_text:
                            response_text = response_text.replace("!","!")
                        #شرط نبودن متن
# The condition of the text is not
                        if not response_text.startswith("```"):
                            if "```" not in response_text:
                                words = response_text.split()
                                wrapped_lines = []
                                line = ''
                                for word in words:
                                    text_line = line + word + ' '  # اضافه کردن فاصله
                                    linewidth = self.currentFontMixed.measure(text=text_line)
                                    if linewidth < 1250:
                                        line = text_line  # درصورت عدم خطا ادامه بده
                                    else:
                                        # تابع طولانی بودن متن - اینتر زدن
# Function of the long text - Inter
                                        wrapped_lines.append(line)
                                        line = word + ' '  # شروع لاین جدید از کلمه آخر
                                if line:
                                    wrapped_lines.append(line)

                                TextClipboardReady = ('\n\n'.join(wrapped_lines))
                                labeltext.configure(text=render_text(('\n\n'.join(wrapped_lines))))
                            if "```" in response_text:
                                splited = response_text.split("```")
                                #اگر طول لیست بر دو بخش پذیر نباشد پس مقدار های متغیر را از لیست ریافت کرده و در تابع جایگذاری کن
# If the list length is not over two segments, then take the variable value from the list and place it in the function
                                if len(splited) % 2 != 0:
                                    codeStructure = splited[len(splited)-2]
                                    CodeSplited = codeStructure.split("\n")
                                    ProgrammingLanguage = CodeSplited[0]
                                    MainCode = codeStructure.replace(ProgrammingLanguage, "")
                                    CopyButton.pack( padx=20, pady=20)
                                    Codeframe.pack( padx=20, pady=20)
                                    labelCodeLanguage.pack( padx=20, pady=5)
                                    LabelCode.pack(pady=5)
                                    labelCodeLanguage.configure(text=ProgrammingLanguage)
                                    LabelCode.configure(text=MainCode)
                                    TextSplited = ""
                                    for i in range(len(splited)):
                                        if i % 2 == 0:
                                            TextSplited += splited[i]

                                    words = TextSplited.split()
                                    wrapped_lines = []
                                    line = ''
                                    for word in words:
                                        text_line = line + word + ' '  #اضافه کردن فاصله بین کلمات
                                        linewidth = self.currentFontMixed.measure(text=text_line)
                                        if linewidth < 1250:
                                            line = text_line  # درصورت عدم خطا ادامه دهبد
                                        else:
                                            wrapped_lines.append(line)
                                            line = word + ' ' 
                                    if line:
                                        wrapped_lines.append(line)
                                    TextClipboardReady = ('\n\n'.join(wrapped_lines))
                                    labeltext.configure(text=render_text(('\n\n'.join(wrapped_lines))))
                        #تابع شناسایی Bash ها از ورودی پیام ها جهت نوشتن بصورت کد برنامه نویسی
# Bash Identification Function from Message Input to Write in Programming Code
                        if response_text.startswith("```"):
                            if "```" in response_text:
                                splited = response_text.split("```")
                                del splited[0]
                                #اگر طول لیست بر دو بخش پذیر نباشد پس مقدار های متغیر را از لیست ریافت کرده و در تابع جایگذاری کن
# If the list length is not over two segments, then take the variable value from the list and place it in the function
                                if len(splited) % 2 == 0:
                                    codeStructure = splited[len(splited)-2]
                                    CodeSplited = codeStructure.split("\n")
                                    ProgrammingLanguage = CodeSplited[0]
                                    MainCode = codeStructure.replace(ProgrammingLanguage, "")
                                    labelCodeLanguage.configure(text=ProgrammingLanguage)
                                    LabelCode.configure(text=MainCode)
                                    TextSplited = ""
                                    for i in range(len(splited)):
                                        if i % 2 == 0:
                                            TextSplited += splited[i]
                                    #جدا کردن کلمات متغیر بر حسب فاصله از یکدیگر
# Separate variable words by distance from each other
                                    words = TextSplited.split()
                                    wrapped_lines = []
                                    line = ''
                                    for word in words:
                                        text_line = line + word + ' '  # اضافه کردن فاصله
                                        linewidth = self.currentFontMixed.measure(text=text_line)
                                        if linewidth < 1250:
                                            line = text_line  # اگر خطا وجود ندارد ادامه بده
                                        else:
                                            wrapped_lines.append(line)
                                            line = word + ' '  # کد بعدی را از آخرین کلمه شروع کن
                                    if line:
                                        wrapped_lines.append(line)
                                    TextClipboardReady = ('\n\n'.join(wrapped_lines))
                                    labeltext.configure(text=render_text(('\n\n'.join(wrapped_lines))))
                #شناسایی پیام های ساده از Bash های ارسالی از سمت API
# Identify simple messages from Bashs sent by API
                if "```" not in response_text:
                    words = response_text.split()
                    wrapped_lines = []
                    line = ''
                    for word in words:
                        text_line = line + word + ' '  # اضافه کردن فاصله
                        linewidth = self.currentFontMixed.measure(text=text_line)
                        if linewidth < 1250:
                            line = text_line 
                        else:
                            wrapped_lines.append(line)
                            line = word + ' '  
                    if line:
                        wrapped_lines.append(line)
                    TextClipboardReady = ('\n\n'.join(wrapped_lines))
                    labeltext.configure(text=render_text(('\n\n'.join(wrapped_lines))))
                if "```" in response_text:
                    splited = response_text.split("```")
                    #اگر طول لیست بر دو بخش پذیر نباشد پس مقدار های متغیر را از لیست ریافت کرده و در تابع جایگذاری کن
# If the list length is not over two segments, then take the variable value from the list and place it in the function
                    if len(splited) % 2 != 0:
                        codeStructure = splited[len(splited)-2]
                        CodeSplited = codeStructure.split("\n")
                        ProgrammingLanguage = CodeSplited[0]
                        MainCode = codeStructure.replace(ProgrammingLanguage, "")
                        CodeCopyButton.pack( padx=20, pady=20)
                        Codeframe.pack( padx=20, pady=20)
                        labelCodeLanguage.pack( padx=20, pady=5)
                        LabelCode.pack(pady=5)
                        labelCodeLanguage.configure(text=ProgrammingLanguage)
                        LabelCode.configure(text=MainCode)
                        TextSplited = ""
                        for i in range(len(splited)):
                            if i % 2 == 0:
                                TextSplited += splited[i]
                        words = TextSplited.split()
                        wrapped_lines = []
                        line = ''
                        for word in words:
                            text_line = line + word + ' ' # اضافه کردن فاصله
                            linewidth = self.currentFontMixed.measure(text=text_line)
                            if linewidth < 1250:
                                line = text_line 
                            else:
                                #اگر طول لیست بر دو بخش پذیر نباشد پس مقدار های متغیر را از لیست ریافت کرده و در تابع جایگذاری کن
# If the list length is not over two segments, then take the variable value from the list and place it in the function
                                wrapped_lines.append(line)
                                line = word + ' '  
                        if line:
                            wrapped_lines.append(line)
                        TextClipboardReady = ('\n\n'.join(wrapped_lines))
                        labeltext.configure(text=render_text(('\n\n'.join(wrapped_lines))))
                #شناسایی Bash های داخل کد
# Identify Bash inside the code
                if response_text.startswith("```"):
                    if "```" in response_text:
                        splited = response_text.split("```")
                        del splited[0]
                        #اگر طول لیست بر دو بخش پذیر نباشد پس مقدار های متغیر را از لیست ریافت کرده و در تابع جایگذاری کن
# If the list length is not over two segments, then take the variable value from the list and place it in the function
                        if len(splited) % 2 == 0:
                            codeStructure = splited[len(splited)-2]
                            CodeSplited = codeStructure.split("\n")
                            ProgrammingLanguage = CodeSplited[0]
                            MainCode = codeStructure.replace(ProgrammingLanguage, "")
                            labelCodeLanguage.configure(text=ProgrammingLanguage)
                            LabelCode.configure(text=MainCode)
                            TextSplited = ""
                            for i in range(len(splited)):
                                if i % 2 == 0:
                                    TextSplited += splited[i]

                            words = TextSplited.split()
                            wrapped_lines = []
                            line = ''
                            for word in words:
                                text_line = line + word + ' '  #اضافه کردن فاصله
                                linewidth = self.currentFontMixed.measure(text=text_line)
                                if linewidth < 1250:
                                    line = text_line
                                else:
                                    #اگر طول لیست بر دو بخش پذیر نباشد پس مقدار های متغیر را از لیست ریافت کرده و در تابع جایگذاری کن
# If the list length is not over two segments, then take the variable value from the list and place it in the function
                                    wrapped_lines.append(line)
                                    line = word + ' '  
                            if line:
                                wrapped_lines.append(line)
                            TextClipboardReady = ('\n\n'.join(wrapped_lines))
                            labeltext.configure(text=render_text(('\n\n'.join(wrapped_lines))))
                #ساخت دکمه ایجاد صوت
# Build the button creation of audio
                SoundCreation = customtkinter.CTkButton(master=frame,text="", image=self.TTSStart,width=50,fg_color="transparent", font=(self.CurrentFont, self.CurrentFontSize), command=lambda: SoundPlayButton(TextClipboardReady))
                SoundCreation.pack(padx=2, pady=2)

                # ایجاد روم جدید روی API و اجرای دستورات مورد نیاز
# Create new Rome on API and execute the required commands
                process_content("assistant",TextClipboardReady,self.conversations[self.current_room])
                process_content_Streaming("assistant",TextClipboardReady,self.conversations[self.current_roomS])
                self.SendButton.configure(text="")
                self.sending = False
            
        

        def send_message(event=None):
        #چک کردن اولین پیام ارسال شده 
# Check the first sent message
        #شناسایی روم از روی اولین پیام ارسال شده
# Roman identification from the first sent message
        #درصورت عدم وجود اولین پیام روم جدید ایجاد میکند
# In the absence of the first new Roman message
            if not self.sending:
                self.ChatBoxEnteryValue = self.ChatEntery.get()  # ارسال پیام موجود در ورودی به API
                if "۰" in self.ChatBoxEnteryValue:
                        self.ChatBoxEnteryValue = self.ChatBoxEnteryValue.replace("۰","0")

                if "۱" in self.ChatBoxEnteryValue:
                    self.ChatBoxEnteryValue = self.ChatBoxEnteryValue.replace("۱","1")

                if "۲" in self.ChatBoxEnteryValue:
                    self.ChatBoxEnteryValue = self.ChatBoxEnteryValue.replace("۲","2")

                if "۳" in self.ChatBoxEnteryValue:
                    self.ChatBoxEnteryValue = self.ChatBoxEnteryValue.replace("۳","3")

                if "۴" in self.ChatBoxEnteryValue:
                    self.ChatBoxEnteryValue = self.ChatBoxEnteryValue.replace("۴","4")

                if "۵" in self.ChatBoxEnteryValue:
                    self.ChatBoxEnteryValue = self.ChatBoxEnteryValue.replace("۵","5")

                if "۶" in self.ChatBoxEnteryValue:
                    self.ChatBoxEnteryValue = self.ChatBoxEnteryValue.replace("۶","6")

                if "۷" in self.ChatBoxEnteryValue:
                    self.ChatBoxEnteryValue = self.ChatBoxEnteryValue.replace("۷","7")

                if "۸" in self.ChatBoxEnteryValue:
                    self.ChatBoxEnteryValue = self.ChatBoxEnteryValue.replace("۸","8")

                if "۹" in self.ChatBoxEnteryValue:
                    self.ChatBoxEnteryValue = self.ChatBoxEnteryValue.replace("۹","9")

                if "؟" in self.ChatBoxEnteryValue:
                    self.ChatBoxEnteryValue = self.ChatBoxEnteryValue.replace("؟","?")
                if "!" in self.ChatBoxEnteryValue:
                    self.ChatBoxEnteryValue = self.ChatBoxEnteryValue.replace("!","!")
                if self.ChatBoxEnteryValue: #چک کردن خالی نبودن ورودی
                    self.ChatEntery.delete(0, customtkinter.END)  # پاک سازی پیام ها
                    self.SendButton.configure(text="")  # تغییر پیام ارسال پیام به دکمه ی "استاپ" جهت ایجاد تابع
                    self.sending = True  
                    #اگر نسخه کامل برنامه بود
# If the full version of the app was
                    if self.Full_Edition:
                        #در خواست کردن از هوش مصنوعی برای اینکه بفهمیم کاربر از هوش مصنوعی خواسته است که برای او عکس بسازد یا نه
# request to ai to see if the user wansts from the app to generate image for him/her
                        response = self.client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                            "role": "system",
                            "content": "You will be provided with a text from User, and your task is to choose yes if the user wants you to generate a picture and vice versa."
                            },
                            {
                            "role": "user",
                            "content": self.ChatBoxEnteryValue
                            }
                        ],
                        temperature=0.7,
                        max_tokens=64,
                        top_p=1
                        )
                        #اگر عکس ساخته بود
# If the photo was made
                        if response.choices[0].message.content == "Yes":
                            append_to_chat_log("User" ,self.ChatBoxEnteryValue)  # نمایش ورودی در لاگ ها
                            threading.Thread(target=fetch_responseIMGGENERATION).start()

                        #اگر نخواسته بود
# if it was unwanted
                        else:
                                    
                            # اضافه کردن پیام جدید ارسال شده در چت روم 
# Add new message sent to chat room
                            if len(self.Images_For_Vision_List) == 0:
                                process_content_Streaming("user",self.ChatBoxEnteryValue,self.conversations[self.current_roomS])
                            else:
                                process_content("user",self.ChatBoxEnteryValue,self.conversations[self.current_room],self.Images_For_Vision_List)

                            append_to_chat_log("User" ,self.ChatBoxEnteryValue)  # نمایش ورودی در لاگ ها
                            threading.Thread(target=fetch_response).start()
                    else:
                        process_content_Streaming("user",self.ChatBoxEnteryValue,self.conversations[self.current_roomS])
                        append_to_chat_log("User" ,self.ChatBoxEnteryValue)  # نمایش ورودی در لاگ ها
                        threading.Thread(target=fetch_response).start()

        #نمایش چت لاگ
# Chat Log Show
        def append_to_chat_log(user , text, **kwargs):
            """Appends a given text to the chat log and ensures the view is scrolled to the end."""

            master = self.ChatFrame

            if user == "User":
                # ایجاد ردیف جدید در فریم
# Create a new row in the frame
                frame = customtkinter.CTkFrame(master, fg_color="#AAD9BB", **kwargs)
                frame.pack( padx=20, pady=20, anchor="e")
                # اضافه کردن لیبل به فریم ساخته شده
# Add Label to Frame Made
                label = customtkinter.CTkLabel(frame, text=user,text_color="Black",font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                label.pack( padx=20, pady=5)
                labeltext = customtkinter.CTkLabel(frame, text=render_text(text), width=1250,text_color="Black",font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
                labeltext.pack( padx=20, pady=5) 
                  
        #ست کردن استایل
# Set style
        def ThemeChosing(choice):
            customtkinter.set_appearance_mode(choice)
        #انتخاب نسخه AI
# Select the AI ​​version
        def AImodelSelection(choice):
            if choice == "Chat GPT 3.5":
                self.AIMODEL = "gpt-3.5-turbo-0125"
            elif choice == "Chat GPT 4" and self.Full_Edition:
                self.AIMODEL = "gpt-4o"


        def Program_Begining_Language_Selection_Function(choice):
            if choice == "فارسی":
                self.Application_Language = "fa"
            elif choice == "English":
                self.Application_Language = "en"
            
        #تابع برای تغییر زبان برنامه
# Function to change the program language
        def LanguageSettingSelection(choice):
            if choice == "فارسی":
                self.Application_Language = "fa"
                self.SettingMainLabel.configure(text="تنظیمات")
                self.SettingAppereanceLabel.configure(text="ظاهر برنامه")
                self.ChatEntery.configure(placeholder_text=render_text("پیام خود را بنویسید...."))
                self.FontsComboBoxLabel.configure(text="فونت")
                self.FontsStyleComboBoxLabel.configure(text="استایل فونت")
                self.FontsSizeComboBoxLabel.configure(text="سایز فونت")
                self.LanguageSelectionForGPTHNAI.configure(values=["فارسی", "زبان های دیگر"])
                self.ThemeComboboxLabel.configure(text="تم برنامه")
                self.SettingAILabel.configure(text="هوش مصنوعی")
                self.AIMODELCOMBOBOXLABEL.configure(text="مدل زبانی")
                self.AppSetting.configure(text="تنظیمات برنامه")
                self.SettingButton.configure(text="تنظیمات")
                self.LanguageComboBoxLabel.configure(text="زبان")
                self.InfoButton.configure(text="درباره ما ")
                self.HelpButton.configure(text="سوالات  ")
                self.VideoTutorial.configure(text="  آموزش ")
                self.UpgradeAccount.configure(text="   ارتقاء  ")
                self.clearButton.configure(text="پاک کردن")
                



            elif choice == "English":
                self.Application_Language = "en"
                self.SettingMainLabel.configure(text="Setting")
                self.SettingAppereanceLabel.configure(text="App Appearance")
                self.ChatEntery.configure(placeholder_text=render_text("Write Your Message..."))
                self.FontsComboBoxLabel.configure(text="Font")
                self.FontsStyleComboBoxLabel.configure(text="Font Style")
                self.FontsSizeComboBoxLabel.configure(text="Font Size")
                self.LanguageSelectionForGPTHNAI.configure(values=["Persian", "Other Languages"])
                self.ThemeComboboxLabel.configure(text="App Theme")
                self.SettingAILabel.configure(text="Artificial Intelligent")
                self.AIMODELCOMBOBOXLABEL.configure(text="AI Model")
                self.AppSetting.configure(text="Application Setting")
                self.LanguageComboBoxLabel.configure(text="Language")
                self.SettingButton.configure(text=" Setting ")
                self.InfoButton.configure(text="    Info   ")
                self.HelpButton.configure(text="   Help   ")
                self.VideoTutorial.configure(text=" Tutorial")
                self.UpgradeAccount.configure(text="Upgrade")
                self.clearButton.configure(text="   Clear  ")

        #ایجاد و اجرای فریم ستینگ
# Creation and implementation of frames
        def Setting_Window_fa():
            Setting_Window = customtkinter.CTkToplevel(self)
            Setting_Window.title("Setting")
            Setting_Window.geometry("400x500")
            Setting_Window.resizable(False, False) # طول و عرض

            self.SettingFrame = customtkinter.CTkScrollableFrame(Setting_Window, width=400,height=430, corner_radius=0)
            self.SettingFrame.grid(row=1, column=0, sticky="nsew")

            #لیبل مورد نیاز برای فریم ستینگ
# Label Required for Frame Setting
            self.SettingMainLabel = customtkinter.CTkLabel(self.SettingFrame, text="تنظیمات", font=(self.CurrentFont, 20, self.CurrentFontBoldState))
            self.SettingMainLabel.grid(row=0, column=1, padx=5, pady=5)

            #تنظیم تم لیبل ستینگ
# Setting
            self.SettingAppereanceLabel = customtkinter.CTkLabel(self.SettingFrame, text="ظاهر برنامه", font=(self.CurrentFont, 18, self.CurrentFontBoldState))
            self.SettingAppereanceLabel.grid(row=1, column=1, padx=5, pady=5)

            #تنظیم المان و ویجت های داخل لیبل ستینگ
# Setting element and widgets inside the label
            self.FontsComboBoxLabel = customtkinter.CTkLabel(self.SettingFrame, text="فونت", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.FontsComboBoxLabel.grid(row=2, column=0, padx=5, pady=5)

            #تنظبم فونت های باکس
# Setting box fonts
            self.FontsComboBox = customtkinter.CTkOptionMenu(self.SettingFrame , values=self.Fonts,command=FontSelection)
            self.FontsComboBox.grid(row=2, column=1, padx=5, pady=5)

            #ست کردن فونت باکس های دیگر
# Setting other font boxes
            self.FontsStyleComboBoxLabel = customtkinter.CTkLabel(self.SettingFrame, text="استایل فونت", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.FontsStyleComboBoxLabel.grid(row=3, column=0, padx=5, pady=5)

            #تعریف فونت های مورد نیاز در باکس
# Define the fonts required in the box
            self.FontsStyleComboBox = customtkinter.CTkOptionMenu(self.SettingFrame , values=self.FontsStyles,
                                        command=FontStyleSelection)
            self.FontsStyleComboBox.grid(row=3, column=1, padx=5, pady=5)
            self.FontsSizeComboBoxLabel = customtkinter.CTkLabel(self.SettingFrame, text="سایز فونت", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.FontsSizeComboBoxLabel.grid(row=4, column=0, padx=5, pady=5)

            self.FontsSizeComboBox = customtkinter.CTkOptionMenu(self.SettingFrame , values=self.FontsSizes,
                                        command=FontSizeSelection)
            self.FontsSizeComboBox.grid(row=4, column=1, padx=5, pady=5)
            self.ThemeComboboxLabel = customtkinter.CTkLabel(self.SettingFrame, text="تم برنامه", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.ThemeComboboxLabel.grid(row=5, column=0, padx=5, pady=5)
            self.ThemeCombobox = customtkinter.CTkOptionMenu(self.SettingFrame , values=["dark","light","system"],
                                        command=ThemeChosing)
            self.ThemeCombobox.grid(row=5, column=1, padx=5, pady=5)

            self.SettingAILabel = customtkinter.CTkLabel(self.SettingFrame, text="هوش مصنوعی", font=(self.CurrentFont, 18, self.CurrentFontBoldState))
            self.SettingAILabel.grid(row=6, column=1, padx=5, pady=5)
            self.AIMODELCOMBOBOXLABEL = customtkinter.CTkLabel(self.SettingFrame, text="مدل زبانی", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.AIMODELCOMBOBOXLABEL.grid(row=7, column=0, padx=5, pady=5)
            self.AIMODELCOMBOBOX = customtkinter.CTkOptionMenu(self.SettingFrame , values=self.AIMODEL_List,
                                        command=AImodelSelection)
            self.AIMODELCOMBOBOX.grid(row=7, column=1, padx=5, pady=5)

            self.AppSetting = customtkinter.CTkLabel(self.SettingFrame, text="تنظیمات برنامه", font=(self.CurrentFont, 18, self.CurrentFontBoldState))
            self.AppSetting.grid(row=8, column=1, padx=5, pady=5)
            self.LanguageComboBoxLabel = customtkinter.CTkLabel(self.SettingFrame, text="تنظیمات زبان", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.LanguageComboBoxLabel.grid(row=9, column=0, padx=5, pady=5)
            self.LanguageComboBox = customtkinter.CTkOptionMenu(self.SettingFrame , values=["فارسی","English"],
                                        command=LanguageSettingSelection)
            self.LanguageComboBox.grid(row=9, column=1, padx=5, pady=5)


        def Setting_Window_en():
            Setting_Window = customtkinter.CTkToplevel(self)
            Setting_Window.title("Setting")
            Setting_Window.geometry("400x500")
            Setting_Window.resizable(False, False) # طول و عرض

            self.SettingFrame = customtkinter.CTkScrollableFrame(Setting_Window, width=400,height=430, corner_radius=0)
            self.SettingFrame.grid(row=1, column=0, sticky="nsew")

            #لیبل مورد نیاز برای فریم ستینگ
# Label Required for Frame Setting
            self.SettingMainLabel = customtkinter.CTkLabel(self.SettingFrame, text="Setting", font=(self.CurrentFont, 20, self.CurrentFontBoldState))
            self.SettingMainLabel.grid(row=0, column=1, padx=5, pady=5)

            #تنظیم تم لیبل ستینگ
# Setting
            self.SettingAppereanceLabel = customtkinter.CTkLabel(self.SettingFrame, text="App Appearance", font=(self.CurrentFont, 18, self.CurrentFontBoldState))
            self.SettingAppereanceLabel.grid(row=1, column=1, padx=5, pady=5)

            #تنظیم المان و ویجت های داخل لیبل ستینگ
# Setting element and widgets inside the label
            self.FontsComboBoxLabel = customtkinter.CTkLabel(self.SettingFrame, text="Font", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.FontsComboBoxLabel.grid(row=2, column=0, padx=5, pady=5)

            #تنظبم فونت های باکس
# Setting box fonts
            self.FontsComboBox = customtkinter.CTkOptionMenu(self.SettingFrame , values=self.Fonts,command=FontSelection)
            self.FontsComboBox.grid(row=2, column=1, padx=5, pady=5)

            #ست کردن فونت باکس های دیگر
# Setting other font boxes
            self.FontsStyleComboBoxLabel = customtkinter.CTkLabel(self.SettingFrame, text="Font Style", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.FontsStyleComboBoxLabel.grid(row=3, column=0, padx=5, pady=5)

            #تعریف فونت های مورد نیاز در باکس
# Define the fonts required in the box
            self.FontsStyleComboBox = customtkinter.CTkOptionMenu(self.SettingFrame , values=self.FontsStyles,
                                        command=FontStyleSelection)
            self.FontsStyleComboBox.grid(row=3, column=1, padx=5, pady=5)
            self.FontsSizeComboBoxLabel = customtkinter.CTkLabel(self.SettingFrame, text="Font Size", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.FontsSizeComboBoxLabel.grid(row=4, column=0, padx=5, pady=5)

            self.FontsSizeComboBox = customtkinter.CTkOptionMenu(self.SettingFrame , values=self.FontsSizes,
                                        command=FontSizeSelection)
            self.FontsSizeComboBox.grid(row=4, column=1, padx=5, pady=5)
            self.ThemeComboboxLabel = customtkinter.CTkLabel(self.SettingFrame, text="App Theme", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.ThemeComboboxLabel.grid(row=5, column=0, padx=5, pady=5)
            self.ThemeCombobox = customtkinter.CTkOptionMenu(self.SettingFrame , values=["dark","light","system"],
                                        command=ThemeChosing)
            self.ThemeCombobox.grid(row=5, column=1, padx=5, pady=5)

            self.SettingAILabel = customtkinter.CTkLabel(self.SettingFrame, text="Artificial Intelligent", font=(self.CurrentFont, 18, self.CurrentFontBoldState))
            self.SettingAILabel.grid(row=6, column=1, padx=5, pady=5)
            self.AIMODELCOMBOBOXLABEL = customtkinter.CTkLabel(self.SettingFrame, text="AI Model", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.AIMODELCOMBOBOXLABEL.grid(row=7, column=0, padx=5, pady=5)
            self.AIMODELCOMBOBOX = customtkinter.CTkOptionMenu(self.SettingFrame , values=self.AIMODEL_List,
                                        command=AImodelSelection)
            self.AIMODELCOMBOBOX.grid(row=7, column=1, padx=5, pady=5)

            self.AppSetting = customtkinter.CTkLabel(self.SettingFrame, text="Application Setting", font=(self.CurrentFont, 18, self.CurrentFontBoldState))
            self.AppSetting.grid(row=8, column=1, padx=5, pady=5)
            self.LanguageComboBoxLabel = customtkinter.CTkLabel(self.SettingFrame, text="Language", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.LanguageComboBoxLabel.grid(row=9, column=0, padx=5, pady=5)
            self.LanguageComboBox = customtkinter.CTkOptionMenu(self.SettingFrame , values=["فارسی","English"],
                                        command=LanguageSettingSelection)
            self.LanguageComboBox.grid(row=9, column=1, padx=5, pady=5)


        #تابع ایجاد پنجره درباره برنامه
# The function of creating the window about the program
        def INFO_Window_fa():
            InfoWindow = customtkinter.CTkToplevel(self, fg_color="#BED7DC")
            InfoWindow.title("App Info")
            InfoWindow.geometry("900*450")
            InfoWindow.resizable(False, False) # طول و عرض

            #ست کردن لیبل های پنجره درباره برنامه
# Setting window labels about app
            self.DEVName = customtkinter.CTkButton(InfoWindow,text_color="black",fg_color="transparent", text="توسعه دهنده و برنامه نویس: محمدرضا ایلمکچی", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.DEVName.grid(row=0,column=1, padx=5, pady=5)
            self.DevEmail = customtkinter.CTkButton(InfoWindow,text_color="black",fg_color="transparent",image=self.EmailIcon, text=render_text("E-mail: Mohammadrezailmakchi@gmail.com"), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState),command=lambda: site_open("mailto:Mohammadrezailmakchi@gmail.com"))
            self.DevEmail.grid( row=1,column=1,padx=5, pady=5)
            self.DevWebsite = customtkinter.CTkButton(InfoWindow,text_color="black",fg_color="transparent",image=self.WebIcon, text=render_text("وبسایت توسعه دهنده: moilweb.ir/mohammadreza-ilmakchi/"), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState), command=lambda: site_open("https://moilweb.ir/mohammadreza-ilmakchi/"))
            self.DevWebsite.grid( row=2,column=1,padx=5, pady=5)
            self.TeacherName = customtkinter.CTkButton(InfoWindow,text_color="black",fg_color="transparent", text="استاد راهنما: جناب آقای یوسف ولی نسب زرنقی", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.TeacherName.grid( row=3,column=1,padx=5, pady=5)
            self.TeacherEmail = customtkinter.CTkButton(InfoWindow,text_color="black",fg_color="transparent",image=self.EmailIcon, text=render_text("E-mail: YousefValinasab98@gmail.com"), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState),command=lambda: site_open("mailto:YousefValinasab98@gmail.com"))
            self.TeacherEmail.grid( row=4,column=1,padx=5, pady=5)
            self.TeacherWebsite = customtkinter.CTkButton(InfoWindow,text_color="black",fg_color="transparent",image=self.WebIcon, text=render_text("وبسایت استاد راهنما: valinasab.ir"), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState), command=lambda: site_open("valinasab.ir"))
            self.TeacherWebsite.grid( row=5,column=1,padx=5, pady=5)
            self.CopyRightText = customtkinter.CTkTextbox(InfoWindow, fg_color="transparent", text_color="black", width=500, wrap="word")
            self.CopyRightText.grid( row=6,column=1, columnspan=2 , padx=5, pady=5)
            #ایجاد متن کپی رایت
# Create Copyright Text
            self.CopyRightText.insert("0.0", 
                """
                Copyright (c) 2024 Mohammadreza Ilmakchi
                Email: Mohammadrezailmakchi@gmail.com

                All rights reserved.

                This program is the intellectual property of Mohammadreza Ilmakchi. It was developed for the Kharawzmi Festival and may not be reproduced, distributed, or used without permission.

                For inquiries regarding the use of this program, please contact Mohammadreza Ilmakchi at Mohammadrezailmakchi@gmail.com.
                """)
            self.CopyRightText.configure(state="disabled")

        
        def INFO_Window_en():
            InfoWindow = customtkinter.CTkToplevel(self, fg_color="#BED7DC")
            InfoWindow.title("App Info")
            InfoWindow.geometry("900*450")
            InfoWindow.resizable(False, False) # طول و عرض

            #ست کردن لیبل های پنجره درباره برنامه
# Setting window labels about app
            self.DEVName = customtkinter.CTkButton(InfoWindow,text_color="black",fg_color="transparent", text="Development and Programming By Mohammadreza Ilmakchi", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.DEVName.grid(row=0,column=1, padx=5, pady=5)
            self.DevEmail = customtkinter.CTkButton(InfoWindow,text_color="black",fg_color="transparent",image=self.EmailIcon, text=render_text("E-mail: Mohammadrezailmakchi@gmail.com"), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState),command=lambda: site_open("mailto:Mohammadrezailmakchi@gmail.com"))
            self.DevEmail.grid( row=1,column=1,padx=5, pady=5)
            self.DevWebsite = customtkinter.CTkButton(InfoWindow,text_color="black",fg_color="transparent",image=self.WebIcon, text=render_text("Developer Website: moilweb.ir/mohammadreza-ilmakchi/"), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState), command=lambda: site_open("https://moilweb.ir/mohammadreza-ilmakchi/"))
            self.DevWebsite.grid( row=2,column=1,padx=5, pady=5)
            self.TeacherName = customtkinter.CTkButton(InfoWindow,text_color="black",fg_color="transparent", text="Advisor : Mr.Valinasab", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.TeacherName.grid( row=3,column=1,padx=5, pady=5)
            self.TeacherEmail = customtkinter.CTkButton(InfoWindow,text_color="black",fg_color="transparent",image=self.EmailIcon, text=render_text("E-mail: YousefValinasab98@gmail.com"), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState),command=lambda: site_open("mailto:YousefValinasab98@gmail.com"))
            self.TeacherEmail.grid( row=4,column=1,padx=5, pady=5)
            self.TeacherWebsite = customtkinter.CTkButton(InfoWindow,text_color="black",fg_color="transparent",image=self.WebIcon, text=render_text("Advisor Website: valinasab.ir"), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState), command=lambda: site_open("valinasab.ir"))
            self.TeacherWebsite.grid( row=5,column=1,padx=5, pady=5)
            self.CopyRightText = customtkinter.CTkTextbox(InfoWindow, fg_color="transparent", text_color="black", width=500, wrap="word")
            self.CopyRightText.grid( row=6,column=1, columnspan=2 , padx=5, pady=5)
            #ایجاد متن کپی رایت
# Create Copyright Text
            self.CopyRightText.insert("0.0", 
                """
                Copyright (c) 2024 Mohammadreza Ilmakchi
                Email: Mohammadrezailmakchi@gmail.com

                All rights reserved.

                This program is the intellectual property of Mohammadreza Ilmakchi. It was developed for the Kharawzmi Festival and may not be reproduced, distributed, or used without permission.

                For inquiries regarding the use of this program, please contact Mohammadreza Ilmakchi at Mohammadrezailmakchi@gmail.com.
                """)
            self.CopyRightText.configure(state="disabled")

        #ساخت پنجره برای ارتقا برنامه
# Build the window to upgrade the program
        def Upgrade_Window_fa():
            Upgrade_Window = customtkinter.CTkToplevel(self,fg_color="#080808")
            Upgrade_Window.title("App Upgration")
            Upgrade_Window.geometry("851.2*116.2")
            Upgrade_Window.resizable(False, False) # طول و عرض

            #ست کردن لیبل های پنجره ارتقا برنامه
# Setting the program upgrades of the program upgrades
            self.Introduction = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text=render_text("تعدادی از قابلیت های برتر نسخه کامل برنامه عبارتند از:"), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Introduction.grid(row=0,column=1, padx=5, pady=5)
            self.Abillity = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text=render_text("نسحه کامل برنامه شامل مدل زبانی GPT-4 و قابلیت های تصویری شنیداری و گفتاری این مدل زبانی و مدل زبانی DALLE-3 برای ساخت تصویر توسط هوش مصنوعی می باشد و قابلیت های جذاب و فراوان دیگر... "), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Abillity.grid(row=1,column=1, padx=5, pady=5)
            self.Abillity1 = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text=render_text("\n مدل زبانی GPT-4 خلاق‌تر و مشارکتی‌تر از همیشه است. این مدل می‌تواند در وظایف نوشتاری خلاقانه و فنی با کاربران همکاری کند، مانند ساختن آهنگ، نوشتن فیلمنامه، یا یادگیری سبک نوشتاری کاربر را انجام دهد."), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Abillity1.grid( row=2,column=1,padx=5, pady=5)
            self.Abillity2 = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text=render_text("\nمدل زبانی GPT-4 قادر است بیش از 25,000 کلمه متن را پردازش کند، که این امکان را فراهم می‌کند تا در مواردی مانند ایجاد محتوای بلند، مکالمات طولانی و جستجو و تحلیل اسناد مورد استفاده قرار گیرد."), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Abillity2.grid( row=3,column=1,padx=5, pady=5)
            self.Abillity3 = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text=render_text("\nمدل زبانی GPT-4 با کسب نمرات در صدک‌های بالاتر نسبت به GPT-3.5 در میان آزمون‌دهندگان، عملکرد بهتری دارد."), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Abillity3.grid( row=4,column=1,padx=5, pady=5)
            self.GPT4VSGPT4 = customtkinter.CTkLabel(Upgrade_Window, text="", image=self.GPT4VSGPT3IMG)
            self.GPT4VSGPT4.grid( row=5,column=1,padx=5, pady=5)
            self.Abillity5 = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text=render_text("\nدر نسخه کامل برنامه شما می توانید با ساتفاده از مدل زبانی DALLE-3 توسط هوش مصنوعی عکس های باور نکردنی بسازید."), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Abillity5.grid( row=6,column=1,padx=5, pady=5)
            self.Abillity6 = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text=render_text("\n و بسیاری دیگر از قابلیت های جذاب و باور نکردنی برنامه"), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Abillity6.grid( row=6,column=1,padx=5, pady=5)
            self.Abillity7 = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text=render_text("\nبرای تهیه نسخه کامل برنامه به سایت زیر مراجعه کنید و سپس ثبت نام انجام دهید و یا ورود کنید و پس از دریافت کلید ویژه آن را کپی کرده و در کادر زیر وارد کنید و سپس روی دکمه ارتقا کلیک کنید."), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Abillity7.grid( row=6,column=1,padx=5, pady=5)
            
            #ارسال کاربر به وبسایت برای ثبت نام و تهیه نسخه کامل برنامه
# Send user to the website to sign up and provide the full version of the app
            self.UpgradeButtonWebsite = customtkinter.CTkButton(Upgrade_Window,text_color="white",fg_color="transparent",hover_color="#51da4c",image=self.WebIcon, text=render_text("ورود به وبسایت"), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState), command=lambda: site_open("https://khawrazmi.moilweb.ir/my_account.php"))
            self.UpgradeButtonWebsite.grid( row=7,column=1,padx=5, pady=5)

            #ورودی کلید ویژه
# Special key input
            self.EnteryUpgrade = customtkinter.CTkEntry(master=Upgrade_Window, placeholder_text=render_text("گلید ویژه را وارد کنید"),width=300 , font=(self.CurrentFont, self.CurrentFontSize))
            self.EnteryUpgrade.grid(row=8, column=1, padx=5, pady=5)
            self.EnteryUpgrade.bind("<Return>", send_message)

            self.Cheat = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text=render_text("کلید در نظر گرفته شده برای جشنواره خوارزمی : Khawrazmi (دقت کنید K با حرف بزرگ است.)"), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Cheat.grid( row=9,column=1,padx=5, pady=5)

            #ایجاد دکمه برای اینکه کاربر بتواند کد ویژه را زده و برنامه را فعال نماید
# Create button to allow the user to hit the special code and enable the application
            self.UpgradeButton = customtkinter.CTkButton(Upgrade_Window,text_color="white",fg_color="transparent",hover_color="#51da4c",image=self.UpgradeIcon, text=render_text("ارتقا"), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState), command=lambda: Upgration_fa())
            self.UpgradeButton.grid( row=10,column=1,padx=5, pady=5)
            self.EAS = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text="", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.EAS.grid( row=11,column=1,padx=5, pady=5)


        #ساخت پنجره برای ارتقا برنامه
# Build the window to upgrade the program
        def Upgrade_Window_en():
            Upgrade_Window = customtkinter.CTkToplevel(self,fg_color="#080808")
            Upgrade_Window.title("App Upgration")
            Upgrade_Window.geometry("851.2*116.2")
            Upgrade_Window.resizable(False, False) # طول و عرض

            #ست کردن لیبل های پنجره ارتقا برنامه
# Setting the program upgrades of the program upgrades
            self.Introduction = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text=render_text("Some of the top features of the full version of the program include:"), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Introduction.grid(row=0,column=1, padx=5, pady=5)
            self.Abillity = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text=render_text("The full version of the program includes the GPT-4 language model with its visual, auditory, and speech capabilities, as well as the DALLE-3 language model for AI-generated images, along with \nmany other attractive features..."), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Abillity.grid(row=1,column=1, padx=5, pady=5)
            self.Abillity1 = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text=render_text("\n The GPT-4 language model is more creative and collaborative than ever. This model can work with users on creative and technical writing tasks, such as composing songs, writing screenplays,\n or learning and adopting the user's writing style."), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Abillity1.grid( row=2,column=1,padx=5, pady=5)
            self.Abillity2 = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text=render_text("\nThe GPT-4 language model can process over 25,000 words of text, enabling it to be used for tasks such as creating long-form content, engaging in extended conversations, and searching and \nanalyzing documents."), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Abillity2.grid( row=3,column=1,padx=5, pady=5)
            self.Abillity3 = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text=render_text("\nThe GPT-4 language model performs better, scoring in higher percentiles compared to GPT-3.5 among test-takers."), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Abillity3.grid( row=4,column=1,padx=5, pady=5)
            self.GPT4VSGPT4 = customtkinter.CTkLabel(Upgrade_Window, text="", image=self.GPT4VSGPT3IMG_en)
            self.GPT4VSGPT4.grid( row=5,column=1,padx=5, pady=5)
            self.Abillity5 = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text=render_text("\nIn the full version of the program, you can create incredible images using the DALLE-3 language model powered by artificial intelligence."), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Abillity5.grid( row=6,column=1,padx=5, pady=5)
            self.Abillity6 = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text=render_text("\n and many other attractive and incredible features of the program."), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Abillity6.grid( row=6,column=1,padx=5, pady=5)
            self.Abillity7 = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text=render_text("\nTo obtain the full version of the program, visit the website below and then sign up or log in. After receiving the special key, copy it and enter it in the field below, then click the \nupgrade button."), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Abillity7.grid( row=6,column=1,padx=5, pady=5)
            
            #ارسال کاربر به وبسایت برای ثبت نام و تهیه نسخه کامل برنامه
# Send user to the website to sign up and provide the full version of the app
            self.UpgradeButtonWebsite = customtkinter.CTkButton(Upgrade_Window,text_color="white",fg_color="transparent",hover_color="#51da4c",image=self.WebIcon, text=render_text("Go to Website"), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState), command=lambda: site_open("https://khawrazmi.moilweb.ir/my_account.php"))
            self.UpgradeButtonWebsite.grid( row=7,column=1,padx=5, pady=5)

            #ورودی کلید ویژه
# Special key input
            self.EnteryUpgrade = customtkinter.CTkEntry(master=Upgrade_Window, placeholder_text=render_text("Enter The Special Key"),width=300 , font=(self.CurrentFont, self.CurrentFontSize))
            self.EnteryUpgrade.grid(row=8, column=1, padx=5, pady=5)
            self.EnteryUpgrade.bind("<Return>", send_message)

            #ایجاد دکمه برای اینکه کاربر بتواند کد ویژه را زده و برنامه را فعال نماید
# Create button to allow the user to hit the special code and enable the application
            self.UpgradeButton = customtkinter.CTkButton(Upgrade_Window,text_color="white",fg_color="transparent",hover_color="#51da4c",image=self.UpgradeIcon, text=render_text("Upgrade"), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState), command=lambda: Upgration_en())
            self.UpgradeButton.grid( row=9,column=1,padx=5, pady=5)
            self.EAS = customtkinter.CTkLabel(Upgrade_Window,text_color="white",fg_color="transparent", text="", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.EAS.grid( row=10,column=1,padx=5, pady=5)



        #ساخت یک تابع برای ایجاد پنجره برای اینکه به کار بر بگوید از نسخه کامل استفاده می کند
# Build a function to create a window to work on the full version uses the full version
        def Upgraded_Window_fa():
            Upgrade_Window = customtkinter.CTkToplevel(self,fg_color="#080808")
            Upgrade_Window.title("App Upgration")
            Upgrade_Window.geometry("1350*768")
            Upgrade_Window.resizable(False, False) # طول و عرض
            Upgrade_Window.attributes('-topmost', 1)
            Upgrade_Window.attributes('-topmost', 0)

            #ست کردن لیبل های پنجره درباره برنامه
# Setting window labels about app
            self.Introduction = customtkinter.CTkLabel(Upgrade_Window,text_color="#51da4c",fg_color="transparent", text=render_text("شما از نسخه کامل برنامه استفاده می کنید."), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Introduction.grid(row=0,column=1, padx=50, pady=50)

        def Upgraded_Window_en():
            Upgrade_Window = customtkinter.CTkToplevel(self,fg_color="#080808")
            Upgrade_Window.title("App Upgration")
            Upgrade_Window.geometry("1350*768")
            Upgrade_Window.resizable(False, False) # طول و عرض
            Upgrade_Window.attributes('-topmost', 1)
            Upgrade_Window.attributes('-topmost', 0)

            #ست کردن لیبل های پنجره درباره برنامه
# Setting window labels about app
            self.Introduction = customtkinter.CTkLabel(Upgrade_Window,text_color="#51da4c",fg_color="transparent", text=render_text("You Are Now Using The Full Edition Of The Program."), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Introduction.grid(row=0,column=1, padx=50, pady=50)


        #ساخت تابع برای اینکه کدام پنجره را برای کاربر باز کند اگر از نسخه کامل برنامه استفاده می کند یا نه
# Build a function to open the window for the user if it uses the full version of the application or not
        #در ضمن در زیر تابع هایی وجود دارند که با استفاده از اینکه برنامه از کدام زبان استفاده می کند پنجره مناسب آن زبان را باز کند
# Also, there are functions below to open the right window using which program uses the program.
        def UpgradeAccount_Function():
            if self.Full_Edition:
                if self.Application_Language == "fa":
                    Upgraded_Window_fa()
                else:
                    Upgraded_Window_en()

            else:
                if self.Application_Language == "fa":
                    Upgrade_Window_fa()
                else:
                    Upgrade_Window_en()

        def OpenSetting_Function():
            if self.Application_Language == "fa":
                    Setting_Window_fa()
            else:
                    Setting_Window_en()

        def OpenInfo_Function():
            if self.Application_Language == "fa":
                    INFO_Window_fa()
            else:
                    INFO_Window_en()

        def FAQ_Function():
            if self.Application_Language == "fa":
                WebURLOpening("\\web\\FAQ.html")
            else:
                WebURLOpening("\\web\\FAQ_en.html")

        #ایجاد تابع کشیدن و رها کردن برای قسمت تصاویر برای تحلیل
# Create a drawing function and drop for the part of the images for analysis
        def Drag_and_Drop():
            self.Images_For_Vision_List = []
            def on_drop(event):
                file_paths = str(event.data).strip('{}').split('} {')
                for file_path in file_paths:
                    self.Images_For_Vision_List.append(file_path)
                label.config(text="Files Loaded If there Are Other Files Please Drag and Drop Them \n فایل ها بارگذاری شدند اگر فابل دیگری دارید دوباره بگشید و بیاندازید")

            def process_images(image_paths):
                # ساختن پوشه Vision برای اینکه فایل های تصاویر را در ان کپی کرده و از آسیب دیدن به فایل اصلی جلو گیری شودالبته اگر ساخته نشده بود
# Build a Vision folder to copy the image files and prevent damage to the original file, if not made
                vision_folder = 'Vision'
                os.makedirs(vision_folder, exist_ok=True)

                #دریافت مسیر تصاویر و کپی کردن آنا در پوشه 
# Receive the path of images and copy Anna in the folder
                for image_path in image_paths:
                    if os.path.isfile(image_path):
                        # ایجاد یک نام جدید برای فایل بدون فاصله و یا خط تیره
# Create a new name for files without distance or dash
                        file_extension = os.path.splitext(image_path)[1]
                        new_filename = f"image_{uuid.uuid4().hex}{file_extension}"
                        
                        # ساختن مسیر مورد نظر
# Building the desired path
                        destination_path = os.path.join(vision_folder, new_filename)

                        # کپی کردن تصویر به پوشه
# Copy the image to the folder
                        shutil.copy(image_path, destination_path)



            # ساختن پنجره اصلی برنامه (کشیدن و رها کردن)
# Making the main program window (pull and drop)
            root = TkinterDnD.Tk()
            root.title("Drag and Drop Files")
            root.geometry("800x400")

            # ساختن یک لیبل که در آن به کاربر اطلاع می دهد که فایل ها را بکشد و رها کند
# Making a label in which the user informs to kill and drop files
            label = tk.Label(root, text="Drag And Drop Files Here | فایل ها را بگشید و اینجا بیاندازید", bg="lightgrey", width=100, height=20)
            label.pack()

            # تنظیم لیبل و ایجاد ایونت درگ اند دراپ یا همان کشیدن و انداختن
# Label adjustment and creation of drag and drag and dragging and throwing
            label.drop_target_register(DND_FILES)
            label.dnd_bind('<<Drop>>', on_drop)

            #شروع کردن لوپ برنامه (پنجره ی این قسمت که همان کشیدن و انداختن است)
# Starting the app's loop (the window of this part that is the same as pulling and throwing)
            root.mainloop()

            process_images(self.Images_For_Vision_List)

        #تابع برای شروع کردن برنامه
# Function to start the program
        def Program_Start():
            if self.Application_Language == "fa":
                OpenProgram_fa()
            else:
                OpenProgram_en()

        #تابع برای انتخاب زبان برنامه در همان ورودی برنامه
# Function to select the program language at the same program input
        def Program_Begining_Language_Selection():
            self.HelpWindow.destroy()
            self.HelpWindow.update()
            self.Program_Begining_Language_Selection_window = customtkinter.CTkToplevel(self)
            self.Program_Begining_Language_Selection_window.title("Language Selection")
            self.Program_Begining_Language_Selection_window.geometry("600x175")
            self.Program_Begining_Language_Selection_window.resizable(False, False) # طول و عرض
            self.Program_Begining_Language_Selection_Label = customtkinter.CTkLabel(self.Program_Begining_Language_Selection_window, text="Language | زبان", font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState))
            self.Program_Begining_Language_Selection_Label.pack(pady=10)
            self.Program_Begining_Language_Selection_ComboBox = customtkinter.CTkOptionMenu(self.Program_Begining_Language_Selection_window , values=["فارسی","English"],
                                        command=Program_Begining_Language_Selection_Function)
            self.Program_Begining_Language_Selection_ComboBox.pack(pady=10)
            self.Program_Begining_Language_Selection_SubmitButton = customtkinter.CTkButton(self.Program_Begining_Language_Selection_window,text_color="white",fg_color="transparent", text=render_text("ورود به برنامه | Enter To The Program"), font=(self.CurrentFont, self.CurrentFontSize, self.CurrentFontBoldState), command=lambda: Program_Start())
            self.Program_Begining_Language_Selection_SubmitButton.pack(pady=10)
            

        #تابع ایجاد بخش Help Me
# The Creation of the Help ME section
        def Help():
            self.HelpWindow = customtkinter.CTkToplevel(self)
            self.HelpWindow.title("")
            self.HelpWindow.geometry("1600x600")
            self.HelpWindow.resizable(False, False) # طول و عرض
            self.HelpWindow.attributes('-topmost', 1)
            #ایجاد المان های موجود در پنجره
# The creation of elements in the window
            WTGONFA = customtkinter.CTkTextbox(self.HelpWindow,fg_color="transparent",text_color="#FF8080",height=50, width=1200,font=(self.CurrentFont, 24, "bold"))
            WTGONFA.pack(pady=20)
            WTGONFA.tag_config('tag-right', justify='center')
            WTGONEN = customtkinter.CTkTextbox(self.HelpWindow,fg_color="transparent",text_color="#FF8080",height=50, width=1200,font=(self.CurrentFont, 24, "bold"))
            WTGONEN.pack(pady=20)
            WTGONEN.tag_config('tag-right', justify='center')

            #افکت تایپینگ
# Typing Effect
            typeit(WTGONFA,"end", render_text("معرفی هوش مصنوعی که به احتمال زیاد برترین و باهوش‌ ترین هوش مصنوعی در جهان است."))
            typeit(WTGONEN,"end", render_text("Introducing an AI that is undoubtedly the world's most capable and intelligent artificial intelligence."))

            #افزودن کلید ها
# Add keys
            TMWTGON = customtkinter.CTkButton(master=self.HelpWindow,fg_color="transparent",text_color="#A86464", hover_color="#C7C8CC",text="More Information | توضیحات بیشتر",width=50, font=(self.CurrentFont, 28), command=lambda: WebURLOpening("\\web\\index.html"))
            TMWTGON.pack(padx=5, pady=10)
            GTP = customtkinter.CTkButton(master=self.HelpWindow,fg_color="transparent",text_color="#804674", hover_color="#C7C8CC",text="Show Me The Program | رفتن به برنامه",width=50, font=(self.CurrentFont, 28), command=lambda: Program_Begining_Language_Selection())
            GTP.pack(padx=5, pady=10)         
        Help()
             
        # باز کردن برنامه بعد از اجرا شدن تابع های قبلی یا بطور دیگر برنامه اجرا می شود درصورتی کاربر کلید رفتن به برنامه را بزند
# Opening the program will run after running previous functions or other applications.
        def OpenProgram_fa():
            self.Program_Begining_Language_Selection_window.destroy()
            self.Program_Begining_Language_Selection_window.update()
            self.currentFontMixed = customtkinter.CTkFont(self.CurrentFont, self.CurrentFontSize)
            self.MainTabview = customtkinter.CTkTabview(master=self, width=1380, corner_radius=10 )
            self.MainTabview.grid(row=0, column=1, rowspan=3,columnspan=6, padx=5, pady=10, sticky="nsew")
            #ایجاد تب های بالای صفحه
# Create tabs on top of the screen
            self.MainChatTabview = self.MainTabview.add(render_text("Chat Section"))
            self.GPTHNAI = self.MainTabview.add(render_text("G.P.T.H.N.A.I"))
            #فریم اصلی چت
# The main chat frame
            self.ChatFrame = ChatFrame(master=self.MainChatTabview, width=1330,height=650, corner_radius=0)
            self.ChatFrame.pack(padx=5, pady=10)
            #فریم GPTHNAI
# Gpthnai frame
            self.GPTHNAIFrame = ChatFrame(master=self.GPTHNAI, width=1330,height=650, corner_radius=0)
            self.GPTHNAIFrame.pack(padx=5, pady=10)
            # GPTHNAI دکمه رکورد فارسی
# GPTHNAII Farsi Record button
            self.GPTHNAIPersianRecordingButton = customtkinter.CTkButton(master=self.GPTHNAIFrame,text="", image=self.TalkingStart,width=500,corner_radius=25, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: toggle_recording())
            self.GPTHNAIPersianRecordingButton.pack(padx=2, pady=100)
            #انتخاب فونت های مورد نیاز برای المان ها
# Select the fonts required for elements
            self.LanguageSelectionForGPTHNAI = customtkinter.CTkOptionMenu(self.GPTHNAIFrame,
                                        values=["فارسی", "زبان های دیگر"],
                                        state=self.LanguageSelectionForGPTHNAIState,
                                        font=(self.CurrentFont, 20),
                                        command=LanguageSelection)
            self.LanguageSelectionForGPTHNAI.pack( padx=5, pady=5)
            #ورودی چت و ارسال آن به سمت API
# Chat input and send it to the API
            self.ChatEntery = customtkinter.CTkEntry(master=self, placeholder_text=render_text("پیام خود را بنویسید...."),width=1130 , font=(self.CurrentFont, self.CurrentFontSize))
            self.ChatEntery.grid(row=3, column=4, padx=2, pady=2)
            self.ChatEntery.bind("<Return>", send_message)

            #دکمه جایگذاری
# Placement button
            self.PasteButton = customtkinter.CTkButton(master=self,text="", image=self.PasteIcon,width=20, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: paste_from_clipboard(self.ChatEntery))
            self.PasteButton.grid(row=3, column=3, padx=2, pady=2)

            #دکمه ارسال
# The send button
            self.SendButton = customtkinter.CTkButton(master=self,text="", image=self.SendIcon,width=20, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: send_message())
            self.SendButton.grid(row=3, column=5, padx=2, pady=2)

            #ست کردن فریم آپشن ها
# Set the options frame
            self.Options = customtkinter.CTkFrame(master=self, corner_radius=25 , width=300,fg_color="transparent",bg_color="transparent", **kwargs)
            self.Options.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

            #دکمه تنظیمات
# Settings button
            self.SettingButton = customtkinter.CTkButton(master=self.Options,text="تنظیمات", image=self.SettingIcon,width=20, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: OpenSetting_Function())
            self.SettingButton.pack( padx=2, pady=10)

            #دکمه درباره ماه
# Button on the moon
            self.InfoButton = customtkinter.CTkButton(master=self.Options,text="درباره ما ", image=self.InfoIcon,width=20, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: OpenInfo_Function())
            self.InfoButton.pack( padx=2, pady=10)

            #دکمه کمک به ما
# The help button to us
            self.HelpButton = customtkinter.CTkButton(master=self.Options,text="سوالات  ", image=self.HelpIcon,width=20, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: WebURLOpening("\\web\\FAQ.html"))
            self.HelpButton.pack( padx=2, pady=10)

            #دکمه باز کردن ویدیوی آموزشی
# Tutorial Opening button
            self.VideoTutorial = customtkinter.CTkButton(master=self.Options,text="  آموزش ", image=self.VideoTutorial,width=20, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: VideoTutorial())
            self.VideoTutorial.pack( padx=2, pady=10)

            #دکمه ی ارتقاء به چت جی پی تی کامل
# The upgrade button to the full GPT chat
            self.UpgradeAccount = customtkinter.CTkButton(master=self.Options,text="   ارتقاء  ", image=self.UpgradeIcon,width=20, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: UpgradeAccount_Function())
            self.UpgradeAccount.pack( padx=2, pady=10)

            #دکمه پاکسازی
# Cleansing button
            self.clearButton = customtkinter.CTkButton(master=self.Options,text="پاک کردن",fg_color="#D37676",hover_color="#BB6464", image=self.ClearIcon,width=20, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: ClearFrame())
            self.clearButton.pack( padx=2, pady=10)
            #ایجاد تیپ های راهنمای دکمه ها
# Create Button Guide Types
            ClearButton_Tip = CTkToolTip(self.clearButton, delay=0.25, message=render_text("پاک کردن همه چت ها"), y_offset=-20)
            HelpButton_Tip = CTkToolTip(self.HelpButton, delay=0.25, message=render_text("آموزش کار با اپلیکیشن"), y_offset=-20)
            InfoButton_Tip = CTkToolTip(self.InfoButton, delay=0.25, message=render_text("اطلاعات توسعه دهنده"), y_offset=-20)
            SettingButton_Tip = CTkToolTip(self.SettingButton, delay=0.25, message=render_text("تنظیمات برنامه"), y_offset=-20)
            SendButton_Tip = CTkToolTip(self.SendButton, delay=0.25, message=render_text("ارسال پیام"), y_offset=-20,x_offset=-80)
            PasteButton_Tip = CTkToolTip(self.PasteButton, delay=0.25, message=render_text("جایگذاری(الصاق,Paste)"), y_offset=-20)
            IMGGENERATIONBUTTON_Tip = CTkToolTip(self.IMGGENERATIONBUTTON, delay=0.25, message=render_text("فعالسازی/غیرفعالسازی حالت تصویر") , y_offset=-20)
            UpgradeAccount = CTkToolTip(self.UpgradeAccount, delay=0.25, message=render_text("وضیعت ارتقا برنامه") , y_offset=-20)

        #همان تابع قبلی اما نسخه انگلیسی
# The same function but the English version
        def OpenProgram_en():
            self.Program_Begining_Language_Selection_window.destroy()
            self.Program_Begining_Language_Selection_window.update()
            self.currentFontMixed = customtkinter.CTkFont(self.CurrentFont, self.CurrentFontSize)
            self.MainTabview = customtkinter.CTkTabview(master=self, width=1380, corner_radius=10 )
            self.MainTabview.grid(row=0, column=1, rowspan=3,columnspan=6, padx=5, pady=10, sticky="nsew")
            #ایجاد تب های بالای صفحه
# Create tabs on top of the screen
            self.MainChatTabview = self.MainTabview.add(render_text("Chat Section"))
            self.GPTHNAI = self.MainTabview.add(render_text("G.P.T.H.N.A.I"))
            #فریم اصلی چت
# The main chat frame
            self.ChatFrame = ChatFrame(master=self.MainChatTabview, width=1330,height=650, corner_radius=0)
            self.ChatFrame.pack(padx=5, pady=10)
            #فریم GPTHNAI
# Gpthnai frame
            self.GPTHNAIFrame = ChatFrame(master=self.GPTHNAI, width=1330,height=650, corner_radius=0)
            self.GPTHNAIFrame.pack(padx=5, pady=10)
            # GPTHNAI دکمه رکورد فارسی
# GPTHNAII Farsi Record button
            self.GPTHNAIPersianRecordingButton = customtkinter.CTkButton(master=self.GPTHNAIFrame,text="", image=self.TalkingStart,width=500,corner_radius=25, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: toggle_recording())
            self.GPTHNAIPersianRecordingButton.pack(padx=2, pady=100)
            #انتخاب فونت های مورد نیاز برای المان ها
# Select the fonts required for elements
            self.LanguageSelectionForGPTHNAI = customtkinter.CTkOptionMenu(self.GPTHNAIFrame,
                                        values=["Persian", "Other Languages"],
                                        state=self.LanguageSelectionForGPTHNAIState,
                                        font=(self.CurrentFont, 20),
                                        command=LanguageSelection)
            self.LanguageSelectionForGPTHNAI.pack( padx=5, pady=5)
            #ورودی چت و ارسال آن به سمت API
# Chat input and send it to the API
            self.ChatEntery = customtkinter.CTkEntry(master=self, placeholder_text=render_text("Write Your Message..."),width=1130 , font=(self.CurrentFont, self.CurrentFontSize))
            self.ChatEntery.grid(row=3, column=4, padx=2, pady=2)
            self.ChatEntery.bind("<Return>", send_message)

            #دکمه جایگذاری
# Placement button
            self.PasteButton = customtkinter.CTkButton(master=self,text="", image=self.PasteIcon,width=20, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: paste_from_clipboard(self.ChatEntery))
            self.PasteButton.grid(row=3, column=3, padx=2, pady=2)

            #دکمه ارسال
# The send button
            self.SendButton = customtkinter.CTkButton(master=self,text="", image=self.SendIcon,width=20, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: send_message())
            self.SendButton.grid(row=3, column=5, padx=2, pady=2)

            #ست کردن فریم آپشن ها
# Set the options frame
            self.Options = customtkinter.CTkFrame(master=self, corner_radius=25 , width=300,fg_color="transparent",bg_color="transparent", **kwargs)
            self.Options.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

            #دکمه تنظیمات
# Settings button
            self.SettingButton = customtkinter.CTkButton(master=self.Options,text=" Setting ", image=self.SettingIcon,width=20, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: OpenSetting_Function())
            self.SettingButton.pack( padx=2, pady=10)

            #دکمه درباره ماه
# Button on the moon
            self.InfoButton = customtkinter.CTkButton(master=self.Options,text="    Info   ", image=self.InfoIcon,width=20, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: OpenInfo_Function())
            self.InfoButton.pack( padx=2, pady=10)

            #دکمه کمک به ما
# The help button to us
            self.HelpButton = customtkinter.CTkButton(master=self.Options,text="   Help   ", image=self.HelpIcon,width=20, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: FAQ_Function())
            self.HelpButton.pack( padx=2, pady=10)

            #دکمه باز کردن ویدیوی آموزشی
# Tutorial Opening button
            self.VideoTutorial = customtkinter.CTkButton(master=self.Options,text=" Tutorial", image=self.VideoTutorial,width=20, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: VideoTutorial())
            self.VideoTutorial.pack( padx=2, pady=10)

            #دکمه ی ارتقاء به چت جی پی تی کامل
# The upgrade button to the full GPT chat
            self.UpgradeAccount = customtkinter.CTkButton(master=self.Options,text="Upgrade", image=self.UpgradeIcon,width=20, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: UpgradeAccount_Function())
            self.UpgradeAccount.pack( padx=2, pady=10)

            #دکمه پاکسازی
# Cleansing button
            self.clearButton = customtkinter.CTkButton(master=self.Options,text="   Clear  ",fg_color="#D37676",hover_color="#BB6464", image=self.ClearIcon,width=20, font=(self.CurrentFont, self.CurrentFontSize), command=lambda: ClearFrame())
            self.clearButton.pack( padx=2, pady=10)
            #ایجاد تیپ های راهنمای دکمه ها
# Create Button Guide Types
            ClearButton_Tip = CTkToolTip(self.clearButton, delay=0.25, message=render_text("Clear All Messages And ALso AI Memory"), y_offset=-20)
            HelpButton_Tip = CTkToolTip(self.HelpButton, delay=0.25, message=render_text("Learn How to Work With Application"), y_offset=-20)
            InfoButton_Tip = CTkToolTip(self.InfoButton, delay=0.25, message=render_text("Application And Developer Info"), y_offset=-20)
            SettingButton_Tip = CTkToolTip(self.SettingButton, delay=0.25, message=render_text("Application Setting"), y_offset=-20)
            SendButton_Tip = CTkToolTip(self.SendButton, delay=0.25, message=render_text("Send Message"), y_offset=-20,x_offset=-80)
            PasteButton_Tip = CTkToolTip(self.PasteButton, delay=0.25, message=render_text("Paste"), y_offset=-20)
            IMGGENERATIONBUTTON_Tip = CTkToolTip(self.IMGGENERATIONBUTTON, delay=0.25, message=render_text("Activate / Deactivate Image Generation Mode ") , y_offset=-20)
            UpgradeAccount = CTkToolTip(self.UpgradeAccount, delay=0.25, message=render_text("Program / AccountUpgration State") , y_offset=-20)


#  اجرای کد و لوپ کردن برنامه
# Run the code and loop the app
if __name__ == "__main__":
    app = App()
    app.mainloop()  
