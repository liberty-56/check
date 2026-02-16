from curl_cffi import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style
import time

# Инициализация цветов
init(autoreset=True)

# Список сервисов
URLS = [
    # Банки
    "https://www.sberbank.ru", "https://www.tbank.ru", "https://alfabank.ru",
    "https://sovcombank.ru", "https://halvacard.ru", "https://koronapay.com",
    "https://severgazbank.ru", "https://www.vtb.ru", "https://www.gazprombank.ru",
    "https://www.raiffeisen.ru", "https://mkb.ru", "https://open.ru",
    
    # Маркетплейсы (самые капризные)
    "https://www.ozon.ru", "https://www.wildberries.ru", 
    "https://market.yandex.ru", "https://avito.ru", "https://megamarket.ru",
    
    # Экосистема и Гос
    "https://yandex.ru", "https://kinopoisk.ru", "https://vk.com", 
    "https://gosuslugi.ru", "https://nalog.gov.ru", "https://rutube.ru"
]

# Заголовки как у настоящего браузера
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}

def check_site(url):
    domain = url.replace("https://", "").replace("www.", "")
    try:
        start_time = time.time()
        
        # impersonate="chrome110" заставляет сервер думать, что это реальный Chrome
        response = requests.get(
            url, 
            headers=HEADERS, 
            impersonate="chrome110", 
            timeout=10,
            verify=False # Игнорируем ошибки SSL (актуально для гос. сайтов)
        )
        
        elapsed = round((time.time() - start_time) * 1000)
        status = response.status_code
        
        # 498 и 403 часто бывают ложными для ботов, но с impersonate должно пройти
        if status == 200:
            return f"{Fore.GREEN}✅ {domain:<20} | OK (200) | {elapsed}ms"
        elif status in [403, 406, 451, 498]:
            return f"{Fore.RED}⛔ {domain:<20} | BLOCKED ({status}) | Доступ запрещен"
        elif status == 503:
             # Часто бывает на Озоне, если он просит капчу, но соединение есть
            return f"{Fore.YELLOW}⚠️ {domain:<20} | WAF/CAPTCHA (503) | Сайт видит, но просит капчу"
        else:
            return f"{Fore.YELLOW}⚠️ {domain:<20} | CODE {status}"
            
    except Exception as e:
        error_msg = str(e)
        if "Timeout" in error_msg:
             return f"{Fore.RED}❌ {domain:<20} | TIMEOUT | IP забанен или нет маршрута"
        else:
             return f"{Fore.RED}❓ {domain:<20} | ERROR | {error_msg[:30]}"

def main():
    print(f"{Style.BRIGHT}Проверка RU-сервисов (Режим эмуляции Chrome)...")
    print("-" * 65)
    
    # Озон не любит многопоточность с одного IP, снижаем до 3
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(check_site, URLS)
        
        results_list = list(results)
        results_list.sort(key=lambda x: "✅" in x) 

        for res in results_list:
            print(res)
            
    print("-" * 65)

if __name__ == "__main__":
    main()
