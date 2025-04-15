import customtkinter as ctk
from goveeTest import *

class SmartHome:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(master=parent, width=500, height=500, fg_color="black", border_width=3, border_color="white")
        self.frame.place(relx=.5, rely=.5, anchor="center", bordermode='outside')
        for i in range(9):
            self.frame.rowconfigure(i, weight=1)
        for i in range(6):
            self.frame.columnconfigure(i, weight=1)

        titleLabel = ctk.CTkLabel(self.frame, text="Govee Devices:", font=("Arial", 24), text_color="white", fg_color="black")
        closeWindow = ctk.CTkButton(self.frame, text="X", font=("Arial", 24), text_color="white", fg_color="black", width=20, command=self.close_widget)
        devicesButton = ctk.CTkButton(self.frame, text="Lamp", font=("Arial", 20), text_color="white", fg_color="black", width=20)

        powerLabel = ctk.CTkLabel(self.frame, text="Power:", font=("Arial", 24), text_color="white", fg_color="black")
        onButton = ctk.CTkButton(self.frame, text="ON", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: changeLight("devices.capabilities.on_off", "powerSwitch", 1))        
        offButton = ctk.CTkButton(self.frame, text="OFF", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: changeLight("devices.capabilities.on_off", "powerSwitch", 0))        

        brightnessLabel = ctk.CTkLabel(self.frame, text="Brightness:", font=("Arial", 24), text_color="white", fg_color="black")
        percent1Button = ctk.CTkButton(self.frame, text="1%", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: changeLight("devices.capabilities.range", "brightness", 1))
        percent25Button = ctk.CTkButton(self.frame, text="25%", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: changeLight("devices.capabilities.range", "brightness", 25))
        percent50Button = ctk.CTkButton(self.frame, text="50%", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: changeLight("devices.capabilities.range", "brightness", 50))
        percent75Button = ctk.CTkButton(self.frame, text="75%", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: changeLight("devices.capabilities.range", "brightness", 75))
        percent100Button = ctk.CTkButton(self.frame, text="100%", font=("Arial", 10), text_color="white", fg_color="black", width=20, command=lambda: changeLight("devices.capabilities.range", "brightness", 100))

        whiteTempLabel = ctk.CTkLabel(self.frame, text="White Temperature:", font=("Arial", 24), text_color="white", fg_color="black")
        coolTempButton = ctk.CTkButton(self.frame, text="Cool", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: changeLight("devices.capabilities.color_setting", "colorTemperatureK", 9000))
        pureTempButton = ctk.CTkButton(self.frame, text="Pure", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: changeLight("devices.capabilities.color_setting", "colorTemperatureK", 5500))
        warmTempButton = ctk.CTkButton(self.frame, text="Warm", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: changeLight("devices.capabilities.color_setting", "colorTemperatureK", 2000))

        colorLabel = ctk.CTkLabel(self.frame, text="Color:", font=("Arial", 24), text_color="white", fg_color="black")
        redButton = ctk.CTkButton(self.frame, text="Red", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(255, 0, 0))))
        orangeButton = ctk.CTkButton(self.frame, text="Orange", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(255, 127, 0))))
        yellowButton = ctk.CTkButton(self.frame, text="Yellow", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(255, 255, 0))))
        greenButton = ctk.CTkButton(self.frame, text="Green", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(0, 255, 0))))
        blueButton = ctk.CTkButton(self.frame, text="Blue", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(0, 0, 255))))
        purpleButton = ctk.CTkButton(self.frame, text="Purple", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(160, 0, 255))))

        titleLabel.grid(column = 0, row = 0, columnspan = 3, sticky='sw', pady = 3, padx = 13)
        closeWindow.grid(column = 5, row = 0,  pady = 3, padx = 3)
        devicesButton.grid(column = 0, row = 1, sticky='n', pady = 3, padx = 7)

        powerLabel.grid(column = 0, row = 2, columnspan = 3, sticky='sw', padx = 13)
        onButton.grid(column = 0, row = 3, sticky='n', pady = 3, padx = 3)
        offButton.grid(column = 1, row = 3, sticky='n', pady = 3, padx = 3)

        brightnessLabel.grid(column = 0, row = 4, columnspan = 3, sticky='sw', padx = 13)
        percent1Button.grid(column = 0, row = 5, sticky='n', pady = 3, padx = 3)
        percent25Button.grid(column = 1, row = 5, sticky='n', pady = 3, padx = 3)
        percent50Button.grid(column = 2, row = 5, sticky='n', pady = 3, padx = 3)
        percent75Button.grid(column = 3, row = 5, sticky='n', pady = 3, padx = 3)
        percent100Button.grid(column = 4, row = 5, sticky='n', pady = 3, padx = 3)

        whiteTempLabel.grid(column = 0, row = 6, columnspan = 3, sticky='sw', padx = 13)
        coolTempButton.grid(column = 0, row = 7, sticky='n', pady = 3, padx = 3)
        pureTempButton.grid(column = 1, row = 7, sticky='n', pady = 3, padx = 3)
        warmTempButton.grid(column = 2, row = 7, sticky='n', pady = 3, padx = 3)

        colorLabel.grid(column = 0, row = 8, columnspan = 3, sticky='sw', padx = 13)
        redButton.grid(column = 0, row = 9, sticky='n', pady = 3, padx = 3)
        orangeButton.grid(column = 1, row = 9, sticky='n', pady = 3, padx = 3)
        yellowButton.grid(column = 2, row = 9, sticky='n', pady = 3, padx = 3)
        greenButton.grid(column = 3, row = 9, sticky='n', pady = 3, padx = 3)
        blueButton.grid(column = 4, row = 9, sticky='n', pady = 3, padx = 3)
        purpleButton.grid(column = 5, row = 9, sticky='n', pady = 3, padx = 3)

    def close_widget(self):
        self.frame.place_forget()
    

def smart_home_widget():
    frame = ctk.CTkFrame(master=root, width = 500, height=500, fg_color="black", border_width=3, border_color="white")

    #This places the smart home frame and all its widgets
    frame.place(relx=.5, rely=.5, anchor="center", bordermode = 'outside')
    for i in range(9):
        frame.rowconfigure(i, weight=1)
    for i in range(6):
        frame.columnconfigure(i, weight=1)
    
    if __name__ == "__main__":
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        root = ctk.CTk()
        root.geometry("500x400")
        root.title("Smart Home Control")

        # Run the main loop
        root.mainloop()