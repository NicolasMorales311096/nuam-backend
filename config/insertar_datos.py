from conexion import conectar

def insertar_datos():
    con = conectar()
    cur = con.cursor()

    # Insertar usuarios
    cur.execute("""
    INSERT INTO usuarios (nombre_completo, email, password_hash, rol)
    VALUES ('Nicolás Morales', 'nico@nuam.cl', '1234', 'admin')
    """)

    cur.execute("""
    INSERT INTO usuarios (nombre_completo, email, password_hash, rol)
    VALUES ('Leah Halton', 'leah@nuam.cl', 'abcd', 'analista')
    """)

    # Insertar países
    cur.execute("INSERT INTO paises (nombre, codigo_iso) VALUES ('Chile', 'CL')")
    cur.execute("INSERT INTO paises (nombre, codigo_iso) VALUES ('Estados Unidos', 'US')")

    # Insertar monedas
    cur.execute("INSERT INTO monedas (codigo, nombre, simbolo) VALUES ('CLP', 'Peso Chileno', '$')")
    cur.execute("INSERT INTO monedas (codigo, nombre, simbolo) VALUES ('USD', 'Dólar Estadounidense', 'US$')")

    # Insertar bolsas
    cur.execute("""
    INSERT INTO bolsas (nombre, ciudad, id_pais, id_moneda_base, zona_horaria)
    VALUES ('Bolsa de Comercio de Santiago', 'Santiago', 1, 1, 'GMT-3')
    """)

    # Insertar empresas
    cur.execute("""
    INSERT INTO empresas (nombre, ticker_base, id_bolsa, sector, sitio_web)
    VALUES ('NUAM Tech', 'NUAM', 1, 'Tecnología', 'https://nuam.cl')
    """)

    # Insertar instrumentos
    cur.execute("""
    INSERT INTO instrumentos (id_empresa, tipo, ticker, id_moneda_cotizacion, activo)
    VALUES (1, 'acción', 'NUAM.CL', 1, 1)
    """)

    con.commit()
    con.close()
    print("✅ Datos de ejemplo insertados correctamente en la base NUAM.")

if __name__ == "__main__":
    insertar_datos()
