#!/bin/bash
# Скрипт для экспорта данных с локального сервера

echo "=== EXPORTING LOCAL SITE DATA ==="

# Активируем виртуальное окружение
source venv/bin/activate

# Переходим в директорию проекта
cd mysite

# Экспортируем данные
echo "Exporting pages, categories, videos, and sites..."
python manage.py export_site_data --settings=mysite.settings.dev

echo "=== EXPORT COMPLETE ==="
echo "Data exported to: exported_data/"
echo "Files created:"
echo "- exported_data/pages.json"
echo "- exported_data/categories.json" 
echo "- exported_data/videos.json"
echo "- exported_data/sites.json"
echo "- exported_data/all_site_data.json"
echo ""
echo "Now commit and push these files to GitHub:"
echo "git add exported_data/"
echo "git commit -m 'Export local site data'"
echo "git push"
