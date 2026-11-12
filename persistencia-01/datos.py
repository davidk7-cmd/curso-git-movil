import json
from datetime import date
from pathlib import Path

RUTA = Path(__file__).resolve().parent / 'asistencias.json'


def validar(registro):
    campos = {'id', 'estudiante', 'fecha', 'presente'}
    if not isinstance(registro, dict) or set(registro) != campos:
        raise ValueError('Se requieren los cuatro campos del modelo.')
    if type(registro['id']) is not int or registro['id'] < 1:
        raise ValueError('El ID debe ser un entero positivo.')

    nombre = registro['estudiante']
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError('El estudiante debe tener un nombre ficticio.')

    fecha = registro['fecha']
    if not isinstance(fecha, str):
        raise ValueError('La fecha debe ser texto AAAA-MM-DD.')
    try:
        if date.fromisoformat(fecha).isoformat() != fecha:
            raise ValueError()
    except ValueError:
        raise ValueError('La fecha debe ser real y usar AAAA-MM-DD.')

    if type(registro['presente']) is not bool:
        raise ValueError('Presente debe ser un booleano.')


def validar_lista(registros):
    if not isinstance(registros, list):
        raise ValueError('El archivo debe contener una lista.')

    ids, pares = set(), set()
    for registro in registros:
        validar(registro)
        par = (
            registro['estudiante'].strip().casefold(),
            registro['fecha']
        )
        if registro['id'] in ids or par in pares:
            raise ValueError('ID o estudiante y fecha duplicados.')
        ids.add(registro['id'])
        pares.add(par)


class AsistenciaDAO:
    def __init__(self, ruta=RUTA):
        self.ruta = Path(ruta)

    def listar(self):
        try:
            texto = self.ruta.read_text(encoding='utf-8')
        except FileNotFoundError:
            return []

        try:
            registros = json.loads(texto)
        except json.JSONDecodeError as error:
            raise ValueError(
                'JSON dañado. Se conserva el archivo.'
            ) from error

        validar_lista(registros)
        return registros

    def guardar(self, nuevo):
        registros = self.listar()
        registros.append(nuevo)
        validar_lista(registros)
        texto = json.dumps(registros, ensure_ascii=False, indent=2)
        temporal = self.ruta.with_suffix('.tmp')
        temporal.write_text(texto, encoding='utf-8')
        temporal.replace(self.ruta)