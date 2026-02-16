import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style
import time

# Инициализация цветов
init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Список сервисов для проверки
URLS = [
    # Банки
    "https://www.sberbank.ru", "https://www.tbank.ru", "https://alfabank.ru",
    "https://sovcombank.ru", "https://halvacard.ru", "https://koronapay.com",
    "https://severgazbank.ru", "https://www.vtb.ru", "https://www.gazprombank.ru",
    "https://www.raiffeisen.ru", "https://mkb.ru", "https://open.ru",
    
    # Маркетплейсы
    "https://www.ozon.ru", "https://www.wildberries.ru", 
    "https://market.yandex.ru", "https://avito.ru", "https://megamarket.ru",
    
    # Экосистема и Гос
    "https://yandex.ru", "https://kinopoisk.ru", "https://vk.com", 
    "https://gosuslugi.ru", "https://nalog.gov.ru", "https://rutube.ru"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}

def check_site(url):
    domain = url.replace("https://", "").replace("www.", "")
    try:
        start_time = time.time()
        response = requests.get(url, headers=HEADERS, verify=False, timeout=5)
        elapsed = round((time.time() - start_time) * 1000)
        
        status = response.status_code
        
        if status == 200:
            return f"{Fore.GREEN}✅ {domain:<20} | OK (200) | {elapsed}ms"
        elif status in [403, 406, 451]:
            return f"{Fore.RED}⛔ {domain:<20} | BLOCKED ({status}) | Доступ запрещен сайтом"
        elif status == 503:
            return f"{Fore.YELLOW}⚠️ {domain:<20} | WAF/DDoS (503) | Вероятно капча или защита"
        else:
            return f"{Fore.YELLOW}⚠️ {domain:<20} | CODE {status}"
            
    except requests.exceptions.ConnectTimeout:
        return f"{Fore.RED}❌ {domain:<20} | TIMEOUT | IP забанен (нет коннекта)"
    except requests.exceptions.ReadTimeout:
        return f"{Fore.RED}❌ {domain:<20} | READ TIMEOUT | Соединение есть, сайт молчит"
    except Exception as e:
        return f"{Fore.RED}❓ {domain:<20} | ERROR | {str(e)[:30]}"

def main():
    print(f"{Style.BRIGHT}Проверка доступности RU-сервисов с текущего IP...")
    print("-" * 60)
    
    # Запуск в 5 потоков
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(check_site, URLS)
        
        # Сортируем результаты: сначала ошибки (красные), потом успех
        results_list = list(results)
        results_list.sort(key=lambda x: "✅" in x) 

        for res in results_list:
            print(res)
            
    print("-" * 60)
    print("Проверка завершена.")

if __name__ == "__main__":
    main()
