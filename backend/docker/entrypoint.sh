while ! nc -z db 5432; do
  echo "Waiting for PostgreSql to start..."
  sleep 1
done

create_log_dir() {
  root_folder="/opt/logs"
  if [ ! -d "$root_folder" ]; then
    mkdir -p "$root_folder"
    echo "Папка создана: $root_folder"
  fi

  sub_folders=("base_logger")
  for folder in "${sub_folders[@]}"; do
    folder_path="$root_folder/$folder"
    if [ ! -d "$folder_path" ]; then
      mkdir -p "$folder_path"
      echo "Подпапка создана: $folder_path"
    fi
  done
}

server() {
  create_log_dir

  echo "Migrate..."
  python ./manage.py migrate --noinput

  echo "Collect static"
  python ./manage.py collectstatic --noinput

  echo "Run server..."
  gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 8 --timeout 600 --reload
}

celery_worker() {
  create_log_dir

  echo "Starting Celery worker..."
  exec celery -A config worker -l INFO
}

celery_beat() {
  create_log_dir

  echo "Starting Celery beat with database scheduler..."
  exec celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
}

case "$1" in
  server)
    server
    ;;
  celery_worker)
    celery_worker
    ;;
  celery_beat)
    celery_beat
    ;;
  *)
    echo "Usage: $0 {server|celery_worker|celery_beat}"
    exit 1
    ;;
esac

$1
