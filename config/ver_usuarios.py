from conexion import conectar

def ver_usuarios():
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT id_usuario, nombre_completo, email, rol FROM usuarios")
    usuarios = cur.fetchall()

    print("\n LISTA DE USUARIOS REGISTRADOS EN NUAM\n")
    print("{:<5} {:<25} {:<25} {:<10}".format("ID", "Nombre", "Email", "Rol"))
    print("-" * 70)

    for u in usuarios:
        print("{:<5} {:<25} {:<25} {:<10}".format(u[0], u[1], u[2], u[3]))

    con.close()

if __name__ == "__main__":
    ver_usuarios()
