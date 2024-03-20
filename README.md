# bigbox_scraper

Scraper para bajar y comparar todas las experiencias de una Bigbox específica. Por ejemplo, la [Bigbox "Bonjour"](https://www.bigbox.com.ar/regalos/gastronomia/bonjour/).

Se conservan únicamente las experiencias en CABA. Ver [`bigbox/spiders/experiences.py`](bigbox/spiders/experiences.py).

## Requisitos

[Poetry](https://python-poetry.org/docs/)

## Instalar

```
poetry shell
poetry install
```

## Ejemplo: Bajar la Bigbox `bonjour` a CSV

El argumento `box` se puede obtener del link a la Bigbox, por ejemplo `bonjour`: https://www.bigbox.com.ar/regalos/gastronomia/bonjour/

```
poetry shell
scrapy crawl experiences -a box=bonjour -o bonjour.csv
```

[Google Sheet con los resultados obtenidos el 2024-03-20](https://docs.google.com/spreadsheets/d/1uSboNKOnd4nIY_ojjC8pOzDACnznUPyNMyk4Uiyj71o/edit?usp=sharing)
