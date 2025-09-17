#!/usr/bin/env python
"""
Тест подключения к Cloudflare R2
"""

import os
import boto3
from botocore.exceptions import ClientError

def test_r2_connection():
    """Тестирует подключение к R2"""
    
    print("🧪 Тестируем подключение к Cloudflare R2...")
    
    # Получаем настройки из переменных окружения
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    endpoint_url = os.environ.get('AWS_S3_ENDPOINT_URL')
    
    print(f"📋 Настройки:")
    print(f"  - Bucket: {bucket_name}")
    print(f"  - Endpoint: {endpoint_url}")
    print(f"  - Access Key: {'*' * (len(access_key) - 4) + access_key[-4:] if access_key else 'НЕ УСТАНОВЛЕН'}")
    
    if not all([access_key, secret_key, bucket_name, endpoint_url]):
        print("❌ Не все переменные окружения установлены!")
        print("Убедитесь, что файл .env.local заполнен правильно")
        return False
    
    try:
        # Создаем клиент S3
        s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        
        # Проверяем доступ к bucket
        print("\n🔍 Проверяем доступ к bucket...")
        response = s3_client.head_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' доступен!")
        
        # Пробуем загрузить тестовый файл
        print("\n📤 Тестируем загрузку файла...")
        test_content = "Hello from Django! This is a test file for R2."
        test_key = "test/django-test.txt"
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=test_key,
            Body=test_content.encode('utf-8'),
            ContentType='text/plain',
            CacheControl='max-age=3600'
        )
        print(f"✅ Тестовый файл загружен: {test_key}")
        
        # Пробуем скачать файл
        print("\n📥 Тестируем скачивание файла...")
        response = s3_client.get_object(Bucket=bucket_name, Key=test_key)
        downloaded_content = response['Body'].read().decode('utf-8')
        
        if downloaded_content == test_content:
            print("✅ Файл успешно скачан и содержимое совпадает!")
        else:
            print("❌ Содержимое файла не совпадает!")
            return False
        
        # Удаляем тестовый файл
        print("\n🗑️ Удаляем тестовый файл...")
        s3_client.delete_object(Bucket=bucket_name, Key=test_key)
        print("✅ Тестовый файл удален")
        
        print(f"\n🎉 Все тесты прошли успешно!")
        print(f"✅ R2 bucket '{bucket_name}' готов к использованию!")
        
        return True
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        
        print(f"❌ Ошибка подключения к R2:")
        print(f"  - Код ошибки: {error_code}")
        print(f"  - Сообщение: {error_message}")
        
        if error_code == 'NoSuchBucket':
            print(f"💡 Bucket '{bucket_name}' не найден. Проверьте название bucket.")
        elif error_code == 'InvalidAccessKeyId':
            print(f"💡 Неверный Access Key. Проверьте AWS_ACCESS_KEY_ID.")
        elif error_code == 'SignatureDoesNotMatch':
            print(f"💡 Неверный Secret Key. Проверьте AWS_SECRET_ACCESS_KEY.")
        elif error_code == 'AccessDenied':
            print(f"💡 Доступ запрещен. Проверьте права API токена.")
        
        return False
        
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False

if __name__ == '__main__':
    # Загружаем переменные из .env.local
    try:
        from dotenv import load_dotenv
        load_dotenv('.env.local')
        print("📁 Переменные окружения загружены из .env.local")
    except ImportError:
        print("⚠️ python-dotenv не установлен, используем системные переменные")
    except Exception as e:
        print(f"⚠️ Не удалось загрузить .env.local: {e}")
    
    test_r2_connection()
