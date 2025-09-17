from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
from urllib.parse import urlparse

app = Flask(__name__, template_folder='templates', static_folder='static')

# 🔹 Configuración de base de datos directa
DB_CONFIG = {
    'host': 'dpg-d333e7bipnbc73dkvfvg-a',
    'database': 'piero',
    'user': 'piero_user',
    'password': 'zTU8IRNbGppbwlsZ3B9SoS22M6eW1RzN',
    'port': '5432',
    'sslmode': 'require'
}

print(f"✅ Conectando a la base de datos: {DB_CONFIG['user']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}")

def conectar_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print("❌ Error al conectar a la base de datos:", e)
        return None

def crear_persona(dni, nombre, apellido, direccion, telefono):
    conn = conectar_db()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO personas (dni, nombre, apellido, direccion, telefono) VALUES (%s, %s, %s, %s, %s)",
        (dni, nombre, apellido, direccion, telefono)
    )
    conn.commit()
    cursor.close()
    conn.close()

def obtener_registros():
    conn = conectar_db()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas ORDER BY apellido")
    registros = cursor.fetchall()
    cursor.close()
    conn.close()
    return registros

@app.route('/')
def index():
    mensaje_confirmacion = request.args.get("mensaje_confirmacion")
    return render_template('index.html', mensaje_confirmacion=mensaje_confirmacion)

@app.route('/registrar', methods=['POST'])
def registrar():
    dni = request.form['dni']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    crear_persona(dni, nombre, apellido, direccion, telefono)
    return redirect(url_for('index', mensaje_confirmacion="✅ Registro Exitoso"))

@app.route('/administrar')
def administrar():
    registros = obtener_registros()
    return render_template('administrar.html', registros=registros)

@app.route('/eliminar/<dni>')
def eliminar_registro(dni):
    conn = conectar_db()
    if not conn:
        return redirect(url_for('administrar'))
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personas WHERE dni = %s", (dni,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('administrar'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
