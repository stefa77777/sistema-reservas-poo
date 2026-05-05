from abc import ABC, abstractmethod
from datetime import datetime

# =========================
# LOGS
# =========================
def registrar_log(mensaje):
    with open("logs.txt", "a") as archivo:
        archivo.write(f"{datetime.now()} - {mensaje}\n")


# =========================
# EXCEPCIONES PERSONALIZADAS
# =========================
class ErrorSistema(Exception):
    pass

class ClienteError(ErrorSistema):
    pass

class ServicioError(ErrorSistema):
    pass

class ReservaError(ErrorSistema):
    pass


# =========================
# CLASE ABSTRACTA
# =========================
class Entidad(ABC):
    @abstractmethod
    def mostrar_info(self):
        pass


# =========================
# CLIENTE
# =========================
class Cliente(Entidad):
    def __init__(self, nombre, documento):
        if not nombre.strip():
            raise ClienteError("Nombre vacío")
        if not documento.strip():
            raise ClienteError("Documento inválido")

        self.nombre = nombre
        self.documento = documento

    def mostrar_info(self):
        return f"{self.nombre} - {self.documento}"


# =========================
# SERVICIO ABSTRACTO
# =========================
class Servicio(ABC):
    def __init__(self, nombre, precio):
        if precio <= 0:
            raise ServicioError("Precio inválido")
        self.nombre = nombre
        self.precio = precio

    @abstractmethod
    def calcular_costo(self, tiempo):
        pass


# =========================
# SERVICIOS
# =========================
class ServicioSala(Servicio):
    def calcular_costo(self, horas):
        if horas <= 0:
            raise ServicioError("Horas inválidas")
        return self.precio * horas


class ServicioEquipo(Servicio):
    def calcular_costo(self, dias):
        if dias <= 0:
            raise ServicioError("Días inválidos")
        return self.precio * dias


class ServicioAsesoria(Servicio):
    def calcular_costo(self, horas):
        if horas <= 0:
            raise ServicioError("Horas inválidas")
        return self.precio * horas * 1.15


# =========================
# RESERVA
# =========================
class Reserva:
    def __init__(self, cliente, servicio, tiempo):
        if not isinstance(cliente, Cliente):
            raise ReservaError("Cliente inválido")
        if not isinstance(servicio, Servicio):
            raise ReservaError("Servicio inválido")

        self.cliente = cliente
        self.servicio = servicio
        self.tiempo = tiempo
        self.estado = "Pendiente"

    def procesar(self):
        try:
            costo = self.servicio.calcular_costo(self.tiempo)
        except Exception as e:
            registrar_log(f"Error cálculo reserva: {e}")
            raise ReservaError("Error al calcular costo") from e
        else:
            return costo
        finally:
            print("Intento de cálculo realizado")

    def confirmar(self):
        self.estado = "Confirmada"

    def cancelar(self):
        self.estado = "Cancelada"

    def mostrar(self):
        return f"{self.cliente.mostrar_info()} | {self.servicio.nombre} | Estado: {self.estado}"


# =========================
# SISTEMA
# =========================
clientes = []
servicios = []
reservas = []


# =========================
# FUNCIONES DEL MENÚ
# =========================
def registrar_cliente():
    try:
        nombre = input("Nombre: ")
        documento = input("Documento: ")
        cliente = Cliente(nombre, documento)
        clientes.append(cliente)
        print("✅ Cliente registrado")
    except Exception as e:
        print("❌ Error:", e)
        registrar_log(str(e))


def crear_servicio():
    try:
        print("1. Sala\n2. Equipo\n3. Asesoría")
        tipo = input("Seleccione: ")
        nombre = input("Nombre del servicio: ")
        precio = float(input("Precio: "))

        if tipo == "1":
            servicio = ServicioSala(nombre, precio)
        elif tipo == "2":
            servicio = ServicioEquipo(nombre, precio)
        elif tipo == "3":
            servicio = ServicioAsesoria(nombre, precio)
        else:
            raise ServicioError("Tipo inválido")

        servicios.append(servicio)
        print("✅ Servicio creado")

    except Exception as e:
        print("❌ Error:", e)
        registrar_log(str(e))


def crear_reserva():
    try:
        if not clientes or not servicios:
            raise ReservaError("No hay clientes o servicios")

        print("\nClientes:")
        for i, c in enumerate(clientes):
            print(i, c.mostrar_info())

        c_index = int(input("Seleccione cliente: "))
        cliente = clientes[c_index]

        print("\nServicios:")
        for i, s in enumerate(servicios):
            print(i, s.nombre)

        s_index = int(input("Seleccione servicio: "))
        servicio = servicios[s_index]

        tiempo = float(input("Tiempo (horas/días): "))

        reserva = Reserva(cliente, servicio, tiempo)
        costo = reserva.procesar()
        reserva.confirmar()

        reservas.append(reserva)

        print(f"✅ Reserva creada | Costo: {costo}")

    except Exception as e:
        print("❌ Error:", e)
        registrar_log(str(e))


def ver_reservas():
    if not reservas:
        print("No hay reservas")
    for r in reservas:
        print(r.mostrar())


# =========================
# MENÚ PRINCIPAL
# =========================
def menu():
    while True:
        print("\n=== SISTEMA DE RESERVAS ===")
        print("1. Registrar cliente")
        print("2. Crear servicio")
        print("3. Crear reserva")
        print("4. Ver reservas")
        print("5. Salir")

        opcion = input("Seleccione: ")

        try:
            if opcion == "1":
                registrar_cliente()
            elif opcion == "2":
                crear_servicio()
            elif opcion == "3":
                crear_reserva()
            elif opcion == "4":
                ver_reservas()
            elif opcion == "5":
                print("Saliendo...")
                break
            else:
                raise ErrorSistema("Opción inválida")

        except Exception as e:
            print("❌ Error:", e)
            registrar_log(str(e))


# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    try:
        menu()
    except Exception as e:
        registrar_log(f"Error crítico: {e}")
    finally:
        print("Sistema cerrado correctamente")
