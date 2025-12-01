import logging
import re
from datetime import datetime

import scrapy
from bs4 import BeautifulSoup

from config import *
from items.items import ScrapyrealestateItem
from telegram_service import send_telegram_message
from utils import extract_bathrooms

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class IdealistaSpider(scrapy.Spider):
    name = "idealista"
    allowed_domains = ["idealista.com"]
    start_urls = [
    IDEALISTA_URL
    ]

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'es-ES,es;q=0.9,ca;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
    }

    def __init__(self, start_url, mongo_collection, telegram_token, telegram_chat_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.collection = mongo_collection
        self.TOKEN = telegram_token
        self.CHAT_ID = telegram_chat_id
        self.new_flats = []

    def parse(self, response):
        default_url = 'https://www.idealista.com'
        soup = BeautifulSoup(response.text, 'lxml')
        flats = soup.find_all("div", {"class": "item-info-container"})
        print(f"Found {len(flats)} flats")

        # Determinar tipo según URL
        flat_type = 'rent' if 'alquiler' in self.start_urls else 'buy'

        for flat in flats:
            try:
                href_tag = flat.find(class_="item-link")
                href = href_tag['href']
                flat_id = href.split('/')[2]
                title = href_tag.get_text(strip=True)
                price_tag = flat.find("span", {"class": "item-price h2-simulated"})
                price = price_tag.get_text(strip=True) if price_tag else ''

                # Revisar si ya existe en MongoDB
                if self.collection.find_one({"id": flat_id}):
                    continue

                # Inicializar variables
                m2 = rooms = floor = town = neighbour = street = number = ''

                # Extraer detalles
                details = flat.find_all("span", {"class": "item-detail"})
                for d in details:  # Los 3 primeros suelen ser: habitaciones, m², planta
                    text = d.get_text(strip=True)
                    if text.endswith('hab.'):
                        rooms = text
                    elif text.endswith('m²'):
                        m2 = text
                    elif any(x in text for x in ['Planta', 'Bajo', 'Sótano', 'Entreplanta']):
                        floor = text

                bathrooms = ""
                if bathrooms == "":
                    description = flat.find_all("p", {"class": "ellipsis"})
                    for desc in description:
                        bathrooms = extract_bathrooms(desc.get_text(strip=True))
                        if bathrooms != "":
                            break

                # Parsear dirección a town, neighbour, street, number
                parts = [p.strip() for p in title.split(',')]
                if len(parts) == 4:
                    street = parts[0].split(' en ')[-1]
                    number = parts[1]
                    neighbour = parts[2]
                    town = parts[3]
                elif len(parts) == 3:
                    street = parts[0].split(' en ')[-1]
                    neighbour = parts[1]
                    town = parts[2]
                elif len(parts) == 2:
                    neighbour = parts[0].split(' en ')[-1]
                    town = parts[1]

                # Crear item
                item = ScrapyrealestateItem(
                    id=flat_id,
                    price=price,
                    m2=m2,
                    rooms=rooms,
                    bathrooms=bathrooms,
                    floor=floor,
                    town=town,
                    neighbour=neighbour,
                    street=street,
                    number=number,
                    type=flat_type,
                    title=title,
                    href=default_url + href,
                    site='idealista',
                    post_time=datetime.now().isoformat()
                )

                # Guardar en MongoDB
                self.collection.insert_one(dict(item))
                self.new_flats.append(item)
                yield item

            except Exception as e:
                logging.warning(f"Error parseando flat: {e}")
                continue

    def closed(self, reason):
        if self.new_flats:
            for f in self.new_flats:
                # Construimos mensaje
                message = f"<b>{f.get('title','Sin título')}</b>\n"
                message += "Características:\n"
                message += f"- Precio: {f.get('price','N/A')}\n"
                message += f"- m²: {f.get('m2','N/A')}\n"
                message += f"- Altura: {f.get('floor','N/A')}\n"
                message += f"- Habitaciones: {f.get('rooms','N/A')}\n"
                message += f"- Baños: {f.get('bathrooms') or '-'}\n"
                message += f"Link: {f.get('href','N/A')}"
                # Enviar mensaje
                send_telegram_message(TELEGRAM_TOKEN, self.CHAT_ID, message)

