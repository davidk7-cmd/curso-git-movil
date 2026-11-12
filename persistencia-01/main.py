from datos import AsistenciaDAO, RUTA


def main():
    dao = AsistenciaDAO()
    print('Archivo de datos:', RUTA)

    while True:
        print('\n1 Guardar  2 Listar  0 Salir')
        opcion = input('Opción: ').strip()

        try:
            if opcion == '1':
                identificador = int(input('ID entero positivo: '))
                estudiante = input('Estudiante ficticio: ').strip()
                fecha = input('Fecha AAAA-MM-DD: ').strip()
                respuesta = input('¿Presente? s/n: ').strip().lower()

                if respuesta not in ('s', 'n'):
                    raise ValueError('Responde s o n.')

                nuevo = {
                    'id': identificador,
                    'estudiante': estudiante,
                    'fecha': fecha,
                    'presente': respuesta == 's'
                }

                dao.guardar(nuevo)
                print('Guardado confirmado.')

            elif opcion == '2':
                registros = dao.listar()
                for r in registros:
                    estado = 'Presente' if r['presente'] else 'Ausente'
                    print(r['id'], r['estudiante'], r['fecha'], estado)
                print('Total:', len(registros))

            elif opcion == '0':
                break

            else:
                print('Opción no válida.')

        except (ValueError, OSError, UnicodeError) as error:
            print('No se completó la operación:', error)


if __name__ == '__main__':
    main()