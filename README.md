# Valencia Flats Scrapper

Este proyecto es un scraper para Idealista que obtiene información de pisos en Valencia y la guarda en MongoDB. También envía notificaciones a Telegram con los pisos nuevos encontrados.

## Tecnologías utilizadas

* Python 3.13
* Scrapy
* BeautifulSoup
* MongoDB
* Telegram API

## Configuración

1. Crear un entorno virtual:

```bash
python -m venv .venv
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar `config.py` con tus credenciales de MongoDB, Telegram y la URL de Idealista.

## Uso

```bash
python main.py
```

El scraper se ejecuta periódicamente según `SCRAPING_INTERVAL` y guarda los datos en MongoDB, enviando notificaciones por Telegram.
