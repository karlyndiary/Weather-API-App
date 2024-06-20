from tkinter import Tk, Canvas, Entry, Label, Button, PhotoImage
from geopy.geocoders import Photon
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
from PIL import Image, ImageTk

window = Tk()
window.title("Weather App")
window.geometry("414x600")
window.configure(bg="#FFFFFF")

##appicon
app_icon = PhotoImage(file="images/weather.png")
window.iconphoto(False, app_icon)

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def getWeather():
    city = textfield.get()

    geolocator = Photon(user_agent="geoapiExercises")
    location = geolocator.geocode(city)
    obj = TimezoneFinder()

    result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
    timezone.config(text=result)
    long_lat.config(text=f"{round(location.latitude, 4)}°N,{round(location.longitude)}°E")

    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    clock.config(text=current_time)

    # weather
    api = f"https://api.openweathermap.org/data/2.5/forecast?lat={location.latitude}&lon={location.longitude}&appid=your_api_key_here"
    json_data = requests.get(api).json()

    # temperature
    temp_kelvin = json_data['list'][0]['main']['temp']
    feels_like_kelvin = json_data['list'][0]['main']['feels_like']
    humidity = json_data['list'][0]['main']['humidity']
    wind = json_data['list'][0]['wind']['speed']
    description = json_data['list'][0]['weather'][0]['description']

    temp_celsius = kelvin_to_celsius(temp_kelvin)
    feels_like_celsius = kelvin_to_celsius(feels_like_kelvin)

    t.config(text=f"{temp_celsius:.2f} °C")
    f.config(text=f"{feels_like_celsius:.2f} °C")
    h.config(text=f"{humidity}%")
    w.config(text=f"{wind} m/s")
    d.config(text=description)

    # firstcell
    firstdayimage = json_data['list'][0]['weather'][0]['icon']

    original_image = Image.open(f"icons/{firstdayimage}@2x.png")
    new_width, new_height = 120, 120  # Resize as needed
    resized_image = original_image.resize((new_width, new_height))
    photo1 = ImageTk.PhotoImage(resized_image)

    firstimage.config(image=photo1)
    firstimage.image = photo1

    # days
    first = datetime.now()
    day1.config(text=first.strftime("%A"))

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=600,
    width=414,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
main_background = PhotoImage(file="images/background.png")
background = canvas.create_image(207.0, 301.0, image=main_background)

main_temp = PhotoImage(file="images/main.png")
m_temp = canvas.create_image(207.0, 282.0, image=main_temp)

temp_details = PhotoImage(file="images/temp_details.png")
t_details = canvas.create_image(207.0, 479.0, image=temp_details)

search_bar = PhotoImage(file="images/search_bar.png")
search = canvas.create_image(206.0, 105.0, image=search_bar)

humidity_image = PhotoImage(file="images/humidity.png")
humidity_icon = canvas.create_image(83.6796875, 469.0, image=humidity_image)

wind_speed_image = PhotoImage(file="images/wind_speed.png")
wind_speed_icon = canvas.create_image(206.041015625, 469.0, image=wind_speed_image)

bold_font = ("Louis George Café", 10, "bold")
big_bold_font = ("Louis George Café", 15, "bold")
extra_bold_font = ("Louis George Café", 24, "bold")

feels_like_image = PhotoImage(file="images/feels_like.png")
feels_like_icon = canvas.create_image(328.400390625, 469.0, image=feels_like_image)

button_image_1 = PhotoImage(file="images/search_button.png")
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=getWeather,
    relief="flat"
)
button_1.place(
    x=345.0,
    y=94.759765625,
    width=22.079999923706055,
    height=22.079999923706055
)

search_bar_sun_image = PhotoImage(file="images/search_bar_sun_icon.png")
search_bar_sun_icon = canvas.create_image(55.080078125, 105.6796875, image=search_bar_sun_image)

textfield = Entry(window, justify='left', font=bold_font, bg="#F0F0F0", bd=0, border=0, fg="#000716", highlightthickness=0)
textfield.place(x=72.0, y=96.0, width=263.0, height=18.0)
textfield.focus()

# location
timezone = Label(window, font=big_bold_font, fg="white", bg="#87C5DC")
timezone.place(x=220, y=225)

# lat/long
long_lat = Label(window, font=bold_font, fg="white", bg="#59AFCF")
long_lat.place(x=295, y=13)

# clock (here we will place time)
clock = Label(window, font=bold_font, fg="white", bg="#5DB0D0")
clock.place(x=25, y=13)

# day
day1 = Label(window, font=bold_font, bg="#59AFCF", fg="#ffffff")
day1.place(x=89, y=13)

# temp, humidity, pressure, wind, description
t = Label(window, font=extra_bold_font, fg="white", bg="#87C5DC")
t.place(x=210, y=260)
d = Label(window, font=bold_font, fg="white", bg="#87C5DC")
d.place(x=230, y=310)

h = Label(window, font=bold_font, fg="white", bg="#A0B5D7")
h.place(x=70, y=488)
w = Label(window, font=bold_font, fg="white", bg="#A0B5D7")
w.place(x=180, y=488)
f = Label(window, font=bold_font, fg="white", bg="#A0B5D7")
f.place(x=305, y=488)

# weather centre image
firstimage = Label(window, bg="#87C5DC")
firstimage.place(x=70, y=225)

window.resizable(False, False)
window.mainloop()
