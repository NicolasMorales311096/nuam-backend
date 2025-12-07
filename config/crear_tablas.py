from conexion import conectar

def crear_tablas():
    con = conectar()
    cur = con.cursor()

    # Tabla: Usuarios
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_completo TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        rol TEXT DEFAULT 'usuario',
        fecha_registro TEXT,
        estado TEXT DEFAULT 'activo'
    )
    """)

    # Tabla: Paises
    cur.execute("""
    CREATE TABLE IF NOT EXISTS paises (
        id_pais INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        codigo_iso TEXT UNIQUE NOT NULL
    )
    """)

    # Tabla: Monedas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS monedas (
        id_moneda INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE NOT NULL,
        nombre TEXT NOT NULL,
        simbolo TEXT
    )
    """)

    # Tabla: Bolsas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bolsas (
        id_bolsa INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        ciudad TEXT,
        id_pais INTEGER,
        id_moneda_base INTEGER,
        zona_horaria TEXT,
        FOREIGN KEY (id_pais) REFERENCES paises (id_pais),
        FOREIGN KEY (id_moneda_base) REFERENCES monedas (id_moneda)
    )
    """)

    # Tabla: Empresas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS empresas (
        id_empresa INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        ticker_base TEXT,
        id_bolsa INTEGER,
        sector TEXT,
        sitio_web TEXT,
        FOREIGN KEY (id_bolsa) REFERENCES bolsas (id_bolsa)
    )
    """)

    # Tabla: Instrumentos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS instrumentos (
        id_instrumento INTEGER PRIMARY KEY AUTOINCREMENT,
        id_empresa INTEGER,
        tipo TEXT,
        ticker TEXT UNIQUE,
        id_moneda_cotizacion INTEGER,
        activo INTEGER DEFAULT 1,
        FOREIGN KEY (id_empresa) REFERENCES empresas (id_empresa),
        FOREIGN KEY (id_moneda_cotizacion) REFERENCES monedas (id_moneda)
    )
    """)

    # Tabla: Precios Históricos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS precios_historicos (
        id_precio INTEGER PRIMARY KEY AUTOINCREMENT,
        id_instrumento INTEGER,
        fecha_hora TEXT,
        precio_apertura REAL,
        precio_cierre REAL,
        precio_max REAL,
        precio_min REAL,
        volumen REAL,
        FOREIGN KEY (id_instrumento) REFERENCES instrumentos (id_instrumento)
    )
    """)

    # Tabla: Tipos de Cambio
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tipos_cambio (
        id_tipo_cambio INTEGER PRIMARY KEY AUTOINCREMENT,
        id_moneda_origen INTEGER,
        id_moneda_destino INTEGER,
        fecha TEXT,
        tasa REAL,
        UNIQUE (id_moneda_origen, id_moneda_destino, fecha),
        FOREIGN KEY (id_moneda_origen) REFERENCES monedas (id_moneda),
        FOREIGN KEY (id_moneda_destino) REFERENCES monedas (id_moneda)
    )
    """)

    # Tabla: Operaciones Simuladas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS operaciones_simuladas (
        id_operacion INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER,
        id_instrumento INTEGER,
        tipo_operacion TEXT,
        cantidad REAL,
        precio_unitario REAL,
        id_moneda_operacion INTEGER,
        fecha_hora TEXT,
        estado TEXT,
        FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario),
        FOREIGN KEY (id_instrumento) REFERENCES instrumentos (id_instrumento),
        FOREIGN KEY (id_moneda_operacion) REFERENCES monedas (id_moneda)
    )
    """)

    # Tabla: Favoritos (M:N)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS favoritos (
        id_usuario INTEGER,
        id_instrumento INTEGER,
        fecha_agregado TEXT,
        PRIMARY KEY (id_usuario, id_instrumento),
        FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario),
        FOREIGN KEY (id_instrumento) REFERENCES instrumentos (id_instrumento)
    )
    """)

    con.commit()
    con.close()
    print(" Todas las tablas de NUAM fueron creadas correctamente.")

if __name__ == "__main__":
    crear_tablas()
