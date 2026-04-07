# Práctica 1 - Tipología y ciclo de vida de los datos

## Integrantes del grupo
- Carlos Gómez Domínguez
- Blanca Gómez Sanz

## Descripción del proyecto
Este repositorio contiene el desarrollo de la Práctica 1 de la asignatura **Tipología y ciclo de vida de los datos**.  
El objetivo del proyecto ha sido construir un dataset sobre las provincias de España a partir de técnicas de **web scraping** aplicadas a distintas páginas y anexos de Wikipedia.

Página web utilizada como punto de partida:  
https://es.wikipedia.org/wiki/Provincia_(Espa%C3%B1a)

## Estructura del repositorio

- `README.md`: descripción general del proyecto y guía de uso.
- `requirements.txt`: librerías necesarias para ejecutar el código.
- `source/scraping_provincias.py`: script principal de web scraping. Parte de la página principal de provincias de España en Wikipedia, descubre enlaces a anexos relevantes y extrae tablas provinciales para construir un dataset bruto.
- `source/script_limpieza.ipynb`: notebook/script utilizado para limpiar, transformar y consolidar el dataset bruto.
- `dataset/datos_raw.csv`: dataset intermedio generado tras el scraping y la fusión inicial de tablas.
- `dataset/datos_finales.csv`: dataset final limpio y preparado para el análisis.

## Librerías necesarias

Las dependencias del proyecto están recogidas en el archivo `requirements.txt`.

Instalación recomendada:

```bash
pip install -r requirements.txt
```

## Cómo ejecutar el proyecto
### 1. Ejecutar el scraping

Desde la raíz del repositorio:

```bash
python source/scraping_provincias.py
```

Este script genera un archivo CSV con los datos extraídos de Wikipedia.

### 2. Ejecutar la limpieza

Abrir y ejecutar el notebook:

```bash
source/script_limpieza.ipynb
```

o adaptar su contenido a un script .py si se desea automatizar completamente el flujo.

El resultado final es el archivo:
```bash
dataset/datos_finales.csv
```

## Ejemplo replicable de uso

```bash
python source/scraping_provincias.py --output dataset/datos_raw.csv --timeout 10 --sleep 0.5
```

Después, ejecutar el notebook source/script_limpieza.ipynb para obtener el dataset final.

## Dataset publicado

DOI de Zenodo:
https://zenodo.org/records/19462356

## Vídeo explicativo

Enlace al vídeo:
[PENDIENTE DE AÑADIR]

## Licencia del dataset

El dataset resultante se publica bajo licencia CC BY-SA 4.0, en coherencia con la licencia de los contenidos de Wikipedia empleados como fuente.

## Observaciones

El scraping se ha realizado exclusivamente con fines académicos. La información procede de Wikipedia en español y ha sido consolidada a partir de varios anexos y tablas enlazadas desde la página principal de provincias de España.
