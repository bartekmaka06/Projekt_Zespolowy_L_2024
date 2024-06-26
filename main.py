from weather import Weather
from tkinter import Tk, Label, Button, Frame, Entry, PhotoImage, ttk
from PIL import Image, ImageTk
from datetime import datetime
import requests
from io import BytesIO
from skimage import segmentation
import numpy as np

global pogoda  # Declare the variable as global to modify it within the function
url_icon = 'https://openweathermap.org/img/wn/'
def center_window(window, width, height):
    # Pobierz szerokość i wysokość ekranu
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Oblicz położenie, aby umieścić okno na środku ekranu
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Ustaw położenie okna na środku ekranu
    window.geometry(f"{width}x{height}+{x}+{y}")

def get_and_resize_image(icon_id, width, height):
    response = requests.get(url_icon + f'{icon_id}@2x.png')
    image_data = response.content
    original_image = Image.open(BytesIO(image_data))
    resized_image = original_image.resize((width, height), Image.LANCZOS)
    return resized_image

def create_button_callback(button_nr):
    return lambda: click_day_button(button_nr)

def click_day_button(nr):
    print("Selected: "+ str(nr))
    print("Day: ", label_day_l[nr-1].cget("text"), " temp: ", str(int(pogoda.day[nr-1].temperature_avg)))

    image_weather_button = ImageTk.PhotoImage(get_and_resize_image(pogoda.day[nr-1].overall_icon, 200, 200))
    label_photo.config(image=image_weather_button)
    label_photo.image = image_weather_button  # Keep a reference to prevent image from being garbage collected

    label_day.config(text=pogoda.day[nr-1].download_date.strftime("%A"))
    label_avg_temp_day.config(text="Avg temp: " + str(int(pogoda.day[nr-1].temperature_avg)) + " °C")
    label_min_max_temp.config(text="Min: " + str(int(pogoda.day[nr-1].temperature_min)) + " °C Max: " + str(int(pogoda.day[nr-1].temperature_max)) + " °C")
    label_sunset.config(text="Sunset: " + str(pogoda.day[nr-1].sunset))
    label_sunrise.config(text="Sunrise: " + str(pogoda.day[nr-1].sunrise))
    label_weather_info.config(text=pogoda.day[nr-1].description.capitalize())
    label_pressure.config(text="Pressure: " + str(pogoda.day[nr-1].pressure) + " hPa")
    label_cloud.config(text="Cloudy: " + str(pogoda.day[nr-1].clouds) + "%")
    label_wind.config(text="Wind: " + str(pogoda.day[nr-1].wind_speed) + " m/s")
    label_air_humidity.config(text="Air humidity: " + str(pogoda.day[nr-1].humidity) + "%")

def click_search_button():
    global pogoda
    global text_date
    city = entry.get()
    print("Search: " + city)
    
    pogoda = Weather(city)

    # Update the labels and images in the GUI with the new weather data
    update_gui_with_weather_data(pogoda)

def update_gui_with_weather_data(pogoda):
    label_date.config(text="Last update: " + pogoda.day[0].download_date.strftime("%Y-%m-%d %H:%M:%S"))
    print("label_day: " + pogoda.day[0].download_date.strftime("%A"))
    label_day.config(text=pogoda.day[0].download_date.strftime("%A"))
    label_city.config(text=pogoda.city.capitalize())
    label_avg_temp_day.config(text="Avg temp: " + str(int(pogoda.day[0].temperature_avg)) + " °C")
    label_min_max_temp.config(text="Min: " + str(int(pogoda.day[0].temperature_min)) + " °C Max: " + str(int(pogoda.day[0].temperature_max)) + " °C")
    label_sunset.config(text="Sunset: " + str(pogoda.day[0].sunset))
    label_sunrise.config(text="Sunrise: " + str(pogoda.day[0].sunrise))
    label_weather_info.config(text=pogoda.day[0].description.capitalize())
    label_pressure.config(text="Pressure: " + str(pogoda.day[0].pressure) + " hPa")
    label_cloud.config(text="Cloudy: " + str(pogoda.day[0].clouds) + "%")
    label_wind.config(text="Wind: " + str(pogoda.day[0].wind_speed) + " m/s")
    label_air_humidity.config(text="Air humidity: " + str(pogoda.day[0].humidity) + "%")

    # Update the weather images
    update_weather_images(pogoda)

def update_weather_images(pogoda):
    image_weather_update = ImageTk.PhotoImage(get_and_resize_image(pogoda.day[0].overall_icon, 200, 200))
    label_photo.config(image=image_weather_update)
    label_photo.image = image_weather_update  # Keep a reference to prevent image from being garbage collected

    # Update the daily weather images
    for i in range(0,5):
        image_day_widget_update = ImageTk.PhotoImage(get_and_resize_image(pogoda.day[i].overall_icon, 60, 60))
        label_photo_day_l[i].config(image=image_day_widget_update)
        label_photo_day_l[i].image = image_day_widget_update  # Keep a reference to prevent image from being garbage collected
        label_day_l[i].config(text=pogoda.day[i].download_date.strftime("%A"))
        label_avg_temp_day_l[i].config(text=str(int(pogoda.day[i].temperature_avg)))

root = Tk()
root.title('Weather App')
window_width = 700
window_height = 570
root.geometry(f"{window_width}x{window_height}")
center_window(root, window_width, window_height)
#styles
style = ttk.Style()
style.theme_use('clam')
style.configure('Search.TButton',
                foreground='black',
                background='lightgray',
                activebackground='darkgray',
                activeforeground='lightgray',
                borderwidth=0,
                font=('Helvetica', 10), width=8, relief="raised")

style.configure('Select.TButton',
                foreground='black',
                background='lightgray',
                activebackground='darkgray',
                activeforeground='lightgray',
                borderwidth=0,
                font=('Helvetica', 10), width=12, relief="raised")

# Set the background color
bg_color = "white"  # Light blue

# Apply the background color to the root window
root.configure(bg=bg_color)

pogoda = Weather("Łódź")

frame_search = Frame(root, bg=bg_color)

current_date = pogoda.day[0].download_date
formatted_datetime_str = current_date.strftime("%Y-%m-%d %H:%M:%S")
text_date = "Last update: " + formatted_datetime_str
label_date = Label(frame_search, text=text_date, font=("Helvetica", 8), bg=bg_color)
label_date.pack()
entry = Entry(frame_search, width=25, font=("Helvetica", 12))
entry.pack(side="left")
click_button = ttk.Button(frame_search, text="Search", style='Search.TButton', command=click_search_button)
click_button.pack(side="left", padx=3)
frame_search.pack()

frame_forecast = Frame(root, bg=bg_color)
frame_space = Frame(frame_forecast, height=20, bg=bg_color)  # Możesz dostosować wysokość według potrzeb
frame_space.pack()
label_city = Label(frame_forecast, text="Łódź", font=("Helvetica", 20, "bold"), bg=bg_color)
label_city.pack()
label_day = Label(frame_forecast, text=current_date.strftime("%A"), font=("Helvetica", 15), bg=bg_color)
label_day.pack()
frame_forecast.pack()

frame_center = Frame(root, bg=bg_color)

#info po lewej
frame_info_left = Frame(frame_center, bg=bg_color, width=180)
label_avg_temp_day = Label(frame_info_left, text="Avg temp: " + str(int(pogoda.day[0].temperature_avg)) + " °C", font=("Helvetica", 10), bg=bg_color)
label_avg_temp_day.pack()
label_min_max_temp = Label(frame_info_left, text="Min: " + str(int(pogoda.day[0].temperature_min)) + " °C Max: " + str(int(pogoda.day[0].temperature_max)) + " °C", font=("Helvetica", 10), bg=bg_color)
label_min_max_temp.pack()
label_sunrise = Label(frame_info_left, text="Sunrise: " + str(pogoda.day[0].sunrise), font=("Helvetica", 10), bg=bg_color)
label_sunrise.pack()
label_sunset = Label(frame_info_left, text="Sunset: " + str(pogoda.day[0].sunset), font=("Helvetica", 10), bg=bg_color)
label_sunset.pack()
frame_info_left.pack(side="left")

# obraz pogody
image_weather = ImageTk.PhotoImage(get_and_resize_image(pogoda.day[0].overall_icon,200,200), width=200, height=200)
label_photo = Label(frame_center, image=image_weather, bg=bg_color)
label_photo.pack(side="left")

#info po prawej
frame_info_right = Frame(frame_center, bg=bg_color, width=180)
label_pressure = Label(frame_info_right, text="Pressure: " + str(pogoda.day[0].pressure) + " hPa", font=("Helvetica", 10), bg=bg_color)
label_pressure.pack()
label_cloud = Label(frame_info_right, text="Cloudy: " + str(pogoda.day[0].clouds) + "%", font=("Helvetica", 10), bg=bg_color)
label_cloud.pack()
label_wind = Label(frame_info_right, text="Wind: " + str(pogoda.day[0].wind_speed) + " m/s", font=("Helvetica", 10), bg=bg_color)
label_wind.pack()
label_air_humidity = Label(frame_info_right, text="Air humidity: " + str(pogoda.day[0].humidity) + "%", font=("Helvetica", 10), bg=bg_color)
label_air_humidity.pack()
frame_info_right.pack(side="left")

frame_center.pack()


label_weather_info = Label(root, text=pogoda.day[0].description.capitalize(), font=("Helvetica", 15), bg=bg_color)
label_weather_info.pack()
frame_space = Frame(root, height=30, bg=bg_color)  # Możesz dostosować wysokość według potrzeb
frame_space.pack()
#dolny panel dni do wyboru
frame_center2 = Frame(root, bg=bg_color)

frame_day_l = []
label_day_l = []
image_day_l = []
label_photo_day_l = []
label_avg_temp_day_l = []
button_day_l = []

for i in range (1,6):
    frame_day = Frame(frame_center2, bg=bg_color, bd=0, relief="groove")
    frame_day_l.append(frame_day)
    if i<5:
        right_border_frame = Frame(frame_day, bg="lightgrey", width=1)
        right_border_frame.pack(side="right", fill="y", padx=5)
    print("day name: " + pogoda.day[i-1].download_date.strftime("%A"))
    label_day_widget = Label(frame_day, text=pogoda.day[i-1].download_date.strftime("%A"), font=("Helvetica", 10), bg=bg_color)
    label_day_widget.pack()
    label_day_l.append(label_day_widget)

    image_day_widget = ImageTk.PhotoImage(get_and_resize_image(pogoda.day[i-1].overall_icon,60,60), width=60, height=60)
    image_day_l.append(image_day_widget)
    label_photo_day = Label(frame_day, image=image_day_widget, bg=bg_color)
    label_photo_day.pack()
    label_photo_day_l.append(label_photo_day)

    label_avg_temp_day_widget = Label(frame_day, text=str(int(pogoda.day[i-1].temperature_avg)), font=("Helvetica", 10), bg=bg_color)
    label_avg_temp_day_widget.pack()
    label_avg_temp_day_l.append(label_avg_temp_day_widget)

    button_day = ttk.Button(frame_day, text="Select", style='Select.TButton', command=create_button_callback(i))
    button_day.pack()
    button_day_l.append(button_day)
    
    frame_day.pack(side="left")
   


frame_center2.pack()

root.mainloop()


#print(pogoda.status)
# jeśli jest internet i udało się pobrać pogodę najnowszą: "ok_online" - zmienne są tworzone w oparciu o dane online i aktualizowany jest zestaw dni w pliku
# jeśli nie ma internetu/nie udało się pobrać danych ale jest plik: "ok_offline" - zmienne są tworzone w oparciu o plik z dniami pkl
# jeśli nie ma internetu/nie udało się pobrać danych i nie ma pliku: "nok" - nie powstają zmienne - wyrzucic blad i nie pobierac zmiennych!

#odswiezenie pogody, zwraca to samo co wyzej
#pogoda.get_weather()