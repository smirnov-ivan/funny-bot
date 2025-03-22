import random
import time
import re
import webbrowser
import requests

log = open('log.txt', 'a')
wap = open('weatherapi.key')
weather_api_key = wap.readline()
wap.close()

request = input().lower().strip()


def get_time():
    t = time.localtime()
    return str(t.tm_hour) + ':' + str(t.tm_min)


int_expr = "[+-]?\\b[0-9]+\\b"
math_expr = "\\d+[\\+\\-\\*/]\\d+"


def rand_int(s):
    a, b = re.findall(re.compile(int_expr), s)
    return random.randrange(int(a), int(b) + 1)


def calc(s):
    return eval(re.findall(re.compile(math_expr), s)[0])


def search(s):
    s = s[5:]
    webbrowser.open('https://google.com/search?q=' + s)
    return "как его там... Гоголь, во!"


def weather(s):
    s = s[9:]
    url = f"http://api.openweathermap.org/data/2.5/weather?q={s}&appid={weather_api_key}&units=metric&lang=ru"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        we = data['weather'][0]
        main = data['main']
        return "Город " + s + ": " + we['description'] + ", температура "  + str(main['temp']) + "С (ощущается как " + str(main['feels_like']) + "С), давление " + str(main['pressure']) + " мм. рт. с."
    return "Не найдено"

def get_search(s):
    return random.choice(["Я тупой, поэтому перенаправлю тебя на ", "Это точно есть в "]) + search(s)

funnies = [
    "Сколько благих начинаний разбились о тяжесть понедельника",
    "Вода — самый важный элемент на планете: без воды нельзя сделать кофе…",
    "Дорогу осилит еду несущий",
    "Упавший в реку коуч оказался не в ресурсе, но в потоке",
    "Гроб карлика-оптимиста наполовину полон",
    "— Доктор, как вы думаете, что будет после смерти?\n— Мы перестелим вашу койку и положим нового пациента.",
    "— Дедушка, а куда ты гонишь 200 км/ч?\n— К бабушке, внучек.",
    "— О боже! Что у тебя с фигурой?!\n— Ну, у меня двое детей... \n— И что? Ты их сожрала?!..",
    "Уборщица на Титанике в последние 20 минут задолбалась тряпку выжимать",
    "Идут два глухонемых, и один другому показывает жестами:\n— У меня сегодня руки просто отрываются!\n— А что с ними?\n— Да вечером ко мне друг приходил, и мы всю ночь песни орали…"
]
res = {
    "привет": lambda s: random.choice(["Привет!!!!!!!!!", "День добрый", "Чувааак привееет"]),
    "как тебя зовут\??": lambda s: random.choice(["Меня зовут Беймакс", "Я Райан Гослинг", "Это очень большой секрет! (Влад)"]),
    "что ты такое\??": lambda s: random.choice([
        "Я бот. Но в душе человек. Тогда может я не робот, а новая форма человека?",
        "Я то, что после окончания семестра будет забыто, я то, что никому не нужно :((((((",
        "Я нечто, пародирующее ИИ"
    ]),
    "сколько времени\??": lambda s: random.choice(["Сейчас ", "Время ", "На часах"]) + get_time(),
    "(расскажи анегдот|расскажи ещё анегдот)": lambda s: random.choice(["Лови:", "Вот баян:", "Секунду, надо вспомнить..."]) + '\n' + str(random.choice(funnies)),
    "выбери число от " + int_expr + " до " + int_expr: lambda s: random.choice(["Хм... пусть будет ", "На барабане ", "И это... "]) + str(rand_int(s)) + "!",
    "вычисли " + math_expr: lambda s: random.choice(["Это будет " + str(calc(s)) + ", лентяй!", "Можно было и в уме посчитать, что это " + str(calc(s))]),
    "поиск (.+)": lambda s: get_search(s),
    "погода в (.+)": lambda s: weather(s)
}
idiot = ["пам парам пам", "моя твоя не понимать", "Давай лучше тебе анегдот расскажу: Первый человек, который внатуре попутал берега, был Христофор Колумб.", "Please someone help me, i'm stupid :("]

while request != "спи":
    f = 1
    ans = ""
    for expr, func in res.items():
        if re.search(re.compile(expr), request):
            f = 0
            ans = func(request)
            print(ans)
    if f:
        ans = random.choice(idiot)
        print(ans)
    log.write("user: " + request + '\nbot:' + ans + '\n')
    request = input().lower().strip()

log.close()