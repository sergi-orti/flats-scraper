# main-windows.py
import datetime
import time
import subprocess
import sys

SCRAPING_INTERVAL = 300  # 5 min


def main():
    while True:
        print("Ejecutando spider...")

        subprocess.run([sys.executable, "run_once.py"])

        print(f"Spider finalizado a las {datetime.datetime.now()}. Esperando {SCRAPING_INTERVAL} segundos...")
        time.sleep(SCRAPING_INTERVAL)


if __name__ == "__main__":
    main()
