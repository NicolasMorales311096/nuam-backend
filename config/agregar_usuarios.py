from conexion import conectar

def agregar_usuarios():
    con = conectar()
    cur = con.cursor()

    usuarios = [
        ("Nicolás Morales", "nicolas@nuam.cl", "admin123", "admin"),
        ("Alejandro Pérez", "alejandro@nuam.cl", "ale123", "analista"),
        ("Julián Concha", "julian@nuam.cl", "julian321", "usuario"),
        ("Brayan Zuñiga", "brayan@nuam.cl", "brayan123", "usuario")
    ]

    for nombre, email, password, rol in usuarios:
        cur.execute("""
        INSERT INTO usuarios (nombre_completo, email, password_hash, rol)
        VALUES (?, ?, ?, ?)
        """, (nombre, email, password, rol))
        print(f"✅ Usuario agregado: {nombre}")

    con.commit()
    con.close()
    print(" Todos los usuarios fueron agregados correctamente.")

if __name__ == "__main__":
    agregar_usuarios()
