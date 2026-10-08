# Используем образ с предустановленным wkhtmltopdf
FROM madnight/docker-alpine-wkhtmltopdf as wkhtmltopdf_image

# Используем образ Python 3.11-bullseye
FROM python:3.13-bullseye

# Опция для отключения записи байт-кода Python
ENV PYTHONDONTWRITEBYTECODE=1

# # Устанавливаем зависимости, необходимые для сборки Python-пакетов и для работы с изображениями, для работы с postGis
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends bash expat gcc gdal-bin libboost-program-options1.74.0 libboost-regex1.74.0 \
        libboost-date-time1.74.0 libboost-chrono1.74.0 libboost-filesystem1.74.0 libboost-iostreams1.74.0 \
        libboost-system1.74.0 libboost-thread1.74.0 libgdal-dev libjpeg-dev liblua5.4-0 musl-dev netcat-traditional \
        python3-gdal zlib1g-dev osmctools osmium-tool && \
    rm -rf /var/lib/apt/lists/* && \
    ldconfig


#Переменные окружения для Gdal
ENV GDAL_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libgdal.so
ENV GEOS_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libgeos_c.so

# Устанавливаем зависимости Python из файла requirements.txt
ADD ./requirements.txt /opt
RUN pip install --no-cache-dir -r /opt/requirements.txt

# Копируем wkhtmltopdf из предыдущего образа в контейнер
COPY --from=wkhtmltopdf_image /bin/wkhtmltopdf /usr/bin/

# Копируем все файлы проекта в контейнер
ADD ./ /opt

# Устанавливаем рабочую директорию
WORKDIR /opt

# Создаем два тома для медиафайлов и статических файлов
VOLUME /opt/media
VOLUME /opt/staticfiles

# Открываем порт 8000
EXPOSE 8000
