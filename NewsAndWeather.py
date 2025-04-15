"""
This is a draft of making the weather widget expand to full screen and also creating the news widget

Organized weather and news frames

only issue left is somewhat slow runtime
"""



from API_Data import news_list
from API_Data import temp
from API_Data import clouds 
from API_Data import wind_mph 
from API_Data import humid 
from API_Data import low_temp 
from API_Data import high_temp
from API_Data import news_pic
from PIL import Image
from API_Data import weather_symbol
import customtkinter as ctk


ctk.set_appearance_mode("dark")  # Optional: Dark mode
ctk.set_default_color_theme("blue")  # Optional: Default theme
root = ctk.CTk()
root.title("Reflective Assistant")
root.geometry("500x700")

news = str(news_list)
curr_temp = str(temp) + "° C"
cloudy = "Cloud Coverage: " + str(clouds) +"% "
wind_speed = "Wind Speed: " + str(wind_mph) + "mph"
humidity = "Humidity:" + str(humid) + "%"
High = "H: " + str(high_temp)
Low = "L: " + str(low_temp)

for i in range(3):
    root.grid_columnconfigure(i, weight=1)
for i in range(3):
    root.grid_rowconfigure(i, weight=1)
    

def exit_news():
    news_frame.grid_forget()
    #news_close.grid_forget()
    main()

def weather_exit():
    weather_frame.grid_forget()
    #weather_close.grid_forget()
    main()

def main():
    sample_text.grid(column = 1, row = 1)
    news_open.grid(column = 0, row= 0)
    weather_open.grid(column = 2, row = 0)


def news_screen():
    sample_text.grid_forget()
    news_open.grid_forget()
    weather_open.grid_forget()

    news_frame.grid(column = 0, row = 1, sticky = 'nsew')
    #news_frame.place("0.0", news)
    news_frame.grid_columnconfigure(0, weight=1)
    news_frame.grid_rowconfigure(0, weight=1)
    news_frame.grid_rowconfigure(1, weight=1)

    new_display.grid(column = 0, row = 1, padx = 20, pady = 20, sticky = 'nw')
    
    #news_frame.configure(wrap="word")
    news_close.grid(column = 0, row= 0)

def weather_screen():
    sample_text.grid_forget()
    news_open.grid_forget()
    weather_open.grid_forget()

    weather_frame.grid(column = 0, row = 0, columnspan = 3, sticky = 'nsew')

    for i in range(3):
        weather_frame.grid_columnconfigure(i, weight=1)
    for i in range(7):
        weather_frame.grid_rowconfigure(i, weight=1)
    
    
    Wsym_label.grid(column = 1, row = 0, padx = 3, pady = 3)
    tempLabel.grid(column = 1, row = 1, padx = 3, pady = 3)
    cloudLabel.grid(column = 0, row = 3, padx = 20, pady = 20, sticky = 'w', columnspan = 2)
    windLabel.grid(column = 0, row = 4, padx = 20, pady = 20, sticky = 'w', columnspan = 2)
    humidLabel.grid(column = 0, row = 5, padx = 20, pady = 20, sticky = 'w', columnspan = 2)
    HighLabel.grid(column = 2, row = 2, padx = 20, pady = 20, sticky = 'ne')
    LowLabel.grid(column = 0, row = 2, padx = 20, pady = 20, sticky = 'ne')
    weather_close.grid(column = 0, row = 0, padx = 20, pady = 20, sticky = 'ne')


news_frame = ctk.CTkScrollableFrame(master=root, width=500, height= 700, fg_color= 'black')
weather_frame = ctk.CTkFrame(master=root, width=500, height= 700, fg_color= 'black')
sample_text = ctk.CTkLabel(root,text = "this is the main screen",font = ("Aptos (Body)", 20), text_color = "white", wraplength= 425)
news_pic = ctk.CTkImage(dark_image= Image.open(news_pic), size= (80,80))
news_open = ctk.CTkButton(root, image = news_pic, text="", command=news_screen, fg_color= "transparent", width= 80, height= 80)
news_close = ctk.CTkButton(news_frame, text="Close News", command=exit_news)
weather_icon = ctk.CTkImage(dark_image= Image.open(weather_symbol), size= (80,80))
weather_open = ctk.CTkButton(root, image = weather_icon, text = "", command=weather_screen, width= 80, height= 80, fg_color= "transparent")
weather_close = ctk.CTkButton(weather_frame, text="Exit", command=weather_exit)

new_display = ctk.CTkLabel(news_frame,text = news,font = ("Aptos (Body)", 20), text_color = "white", wraplength= 450, anchor= 'w')
weather_sym = ctk.CTkImage(dark_image= Image.open(weather_symbol), size= (210,210))
Wsym_label = ctk.CTkLabel(weather_frame, image=weather_sym, text="")
tempLabel = ctk.CTkLabel(weather_frame, text = curr_temp, font = ("Times New Roman", 30), text_color = "white", fg_color= "black")
cloudLabel = ctk.CTkLabel(weather_frame, text = cloudy, font = ("Times New Roman", 25), text_color = "white", fg_color= "black")
windLabel = ctk.CTkLabel(weather_frame, text = wind_speed, font = ("Times New Roman", 25), text_color = "white", fg_color= "black")
humidLabel = ctk.CTkLabel(weather_frame, text = humidity, font = ("Times New Roman", 25), text_color = "white", fg_color= "black")
HighLabel = ctk.CTkLabel(weather_frame, text = High, font = ("Times New Roman", 25), text_color = "white", fg_color= "black")
LowLabel = ctk.CTkLabel(weather_frame, text = Low, font = ("Times New Roman", 25), text_color = "white", fg_color= "black")

  


main()
root.mainloop()