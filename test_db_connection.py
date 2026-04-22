#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connections

print("=" * 60)
print("VERIFICANDO CONEXIONES A BASES DE DATOS")
print("=" * 60)

# Probar conexión "pagina_web"
try:
    print("\n[1] Intentando conectar a 'pagina_web'...")
    conn = connections["pagina_web"]
    print(f"    ENGINE: {conn.settings_dict['ENGINE']}")
    print(f"    HOST: {conn.settings_dict['HOST']}")
    print(f"    PORT: {conn.settings_dict['PORT']}")
    print(f"    NAME: {conn.settings_dict['NAME']}")
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"    ✅ Conexión exitosa: {result}")
except Exception as e:
    print(f"    ❌ Error: {str(e)}")

print("\n[2] Verificando qué driver MySQL está siendo usado...")
try:
    import MySQLdb
    print(f"    MySQLdb version: {MySQLdb.__version__}")
    print(f"    MySQLdb file: {MySQLdb.__file__}")
except ImportError as e:
    print(f"    ❌ MySQLdb no importable: {e}")

print("\n[3] Verificando PyMySQL...")
try:
    import pymysql
    print(f"    PyMySQL version: {pymysql.__version__}")
    print(f"    PyMySQL installed as MySQLdb: {hasattr(pymysql, 'install_as_MySQLdb')}")
except ImportError as e:
    print(f"    ❌ PyMySQL no importable: {e}")

print("\n[4] Intentando query simple...")
try:
    from django.db import connections
    with connections["pagina_web"].cursor() as cursor:
        sql = "SELECT COUNT(*) FROM ps_orders LIMIT 1"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(f"    ✅ Query exitosa: {result}")
except Exception as e:
    print(f"    ❌ Error: {str(e)}")

print("\n" + "=" * 60)
