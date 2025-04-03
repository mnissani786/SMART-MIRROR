"""
This is a draft of making the weather widget expand to full screen and also creating the news widget
Current problems:
weather data needs to be organized on screen still
news display might need to be refined
buttons need better appearance

BIG ISSUE:
API data seems to be causing buttons to not work immedietly but after letting the 
program run for a bit without interacting with it the buttons work fine
"""



from API_Data import news_list
from API_Data import temp
from API_Data import clouds 
from API_Data import wind_mph 
from API_Data import humid 
from API_Data import low_temp 
from API_Data import high_temp
import customtkinter as ctk


ctk.set_appearance_mode("dark")  # Optional: Dark mode
ctk.set_default_color_theme("blue")  # Optional: Default theme
root = ctk.CTk()
root.title("Reflective Assistant")
root.geometry("500x700")

news = str(news_list)
curr_temp = str(temp) + "° Celsius"
cloudy = str(clouds) +"% \n Cloud Coverage"
wind_speed = "Wind" + str(wind_mph) + "mph"
humidity = "Humidity: \n" + str(humid) + "%"
High = "H: " + str(high_temp)
Low = "L: " + str(low_temp)


def exit_news():
    news_frame.place_forget()
    news_close.place_forget()
    main()

def weather_exit():
    weather_frame.place_forget()
    weather_close.place_forget()
    main()

def main():
    sample_text.place(x= 250, y= 350, anchor = "center")
    news_open.place(x= 250, y= 400, anchor = 'center')
    weather_open.place(x=380, y=95, anchor = 'center')


def news_screen():
    sample_text.place_forget()
    news_open.place_forget()
    weather_open.place_forget()

    news_frame.place(x= 0, y = 0)
    news_frame.insert("0.0", news)
    news_frame.configure(wrap="word")
    news_close.place(x= 75, y= 20, anchor = 'center')

def weather_screen():
    sample_text.place_forget()
    news_open.place_forget()
    weather_open.place_forget()

    weather_frame.place(x= 0, y = 0)
    weather_frame.insert("10.50", curr_temp)
    weather_frame.insert("2.1", cloudy)
    weather_frame.insert("3.2", wind_speed)
    weather_frame.insert("4.3", humidity)
    weather_frame.insert("5.4", High)
    weather_frame.insert("6.5", Low)
    weather_frame.configure(wrap="word")
    weather_close.place(x= 75, y= 300, anchor = 'center')


news_frame = ctk.CTkTextbox(master=root, width=500, height= 700, fg_color= 'black')
weather_frame = ctk.CTkTextbox(master=root, width=500, height= 700, fg_color= 'black')
sample_text = ctk.CTkLabel(root,text = "this is the main screen",font = ("Aptos (Body)", 20), text_color = "white", wraplength= 425)
news_open = ctk.CTkButton(root, text="Open News", command=news_screen)
news_close = ctk.CTkButton(root, text="Close News", command=exit_news)
weather_open = ctk.CTkButton(root, text="Weather", command=weather_screen)
weather_close = ctk.CTkButton(root, text="Exit", command=weather_exit)

    

main()
root.mainloop()