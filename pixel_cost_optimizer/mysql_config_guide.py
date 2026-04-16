"""
MySQL Configuration Setup for Pixel Cost Optimizer
This script helps configure the database settings for phpMyAdmin MySQL connection
"""

MYSQL_SETTINGS = '''
# MySQL Configuration for phpMyAdmin
# Add this to your pixel_cost_optimizer/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'driver': 'pymysql',
        },
        'NAME': 'pixel_cost_optimizer',        # Your database name in phpMyAdmin
        'USER': 'root',                       # Usually 'root' for XAMPP
        'PASSWORD': '',                       # Usually empty for XAMPP
        'HOST': '127.0.0.1',                 # localhost
        'PORT': '3306',                       # Default MySQL port
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    }
}

# Alternatively, if you want to keep SQLite as backup:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'driver': 'pymysql',
        },
        'NAME': 'pixel_cost_optimizer',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    },
    'sqlite_backup': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''

print("🔧 MySQL Configuration for Pixel Cost Optimizer")
print("=" * 60)
print()
print("📋 SETUP STEPS:")
print()
print("1️⃣  XAMPP/phpMyAdmin Setup:")
print("   • Start XAMPP Control Panel")
print("   • Start Apache and MySQL services")
print("   • Open phpMyAdmin: http://localhost/phpmyadmin/")
print("   • Create new database: 'pixel_cost_optimizer'")
print()
print("2️⃣  Django Settings Update:")
print("   • Edit pixel_cost_optimizer/settings.py")
print("   • Replace DATABASES section with MySQL configuration")
print()
print("3️⃣  Database Migration:")
print("   • python manage.py makemigrations")
print("   • python manage.py migrate")
print()
print("4️⃣  Setup Dynamic Data:")
print("   • python manage.py setup_database")
print()
print("=" * 60)
print()
print("📄 MYSQL SETTINGS TO ADD:")
print()
print(MYSQL_SETTINGS)
print()
print("=" * 60)
print()
print("💡 NOTES:")
print("• Make sure PyMySQL is installed: pip install pymysql")
print("• Default XAMPP MySQL user: root (no password)")
print("• Database will be created automatically during migration")
print("• All pricing data will be dynamic from MySQL tables")
print()
print("🔍 VERIFY CONNECTION:")
print("• Check phpMyAdmin: http://localhost/phpmyadmin/")
print("• Look for 'pixel_cost_optimizer' database")
print("• Tables: auth_user, analyzer_defaultpricingrule, analyzer_costsetting, etc.")
print()
print("✅ After setup, your pricing will be 100% dynamic from MySQL!")