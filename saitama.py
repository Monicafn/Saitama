#Gestión de productos

import csv
import os
from datetime import datetime
from typing import List, Dict

# ==================== CLASES PRINCIPALES ====================
class Producto:
    def __init__(self, id: int, nombre: str, categoria: str, precio: float, stock: int):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    def __str__(self):
        return f"{self.id}: {self.nombre} (${self.precio:.2f}) | Stock: {self.stock}"

class Carrito:
    def __init__(self):
        self.items: List[Dict] = []  # Lista de diccionarios: {producto, cantidad}

    def agregar_producto(self, producto: Producto, cantidad: int) -> bool:
        if producto.stock >= cantidad:
            self.items.append({"producto": producto, "cantidad": cantidad})
            producto.stock -= cantidad
            print(f"✅ {cantidad}x {producto.nombre} agregado al carrito")
            return True
        else:
            print(f"❌ Stock insuficiente de {producto.nombre}")
            return False

    def calcular_total(self) -> float:
        return sum(item["producto"].precio * item["cantidad"] for item in self.items)

    def mostrar(self):
        if not self.items:
            print("\n🛒 El carrito está vacío")
            return

        print("\n=== 🛒 CARRITO ===")
        for item in self.items:
            p = item["producto"]
            print(f"- {p.nombre} x{item['cantidad']} = ${p.precio * item['cantidad']:.2f}")
        print(f"\n💵 TOTAL: ${self.calcular_total():.2f}")

# ==================== MANEJO DE ARCHIVOS ====================
class Database:
    @staticmethod
    def cargar_productos() -> List[Producto]:
        productos = []
        try:
            with open("data/productos.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)  # Saltar cabecera
                for row in reader:
                    id, nombre, categoria, precio, stock = row
                    productos.append(Producto(int(id), nombre, categoria, float(precio), int(stock)))
        except FileNotFoundError:
            print("⚠️ No se encontró el archivo de productos. Se creará uno nuevo.")
        return productos

    @staticmethod
    def guardar_productos(productos: List[Producto]):
        os.makedirs("data", exist_ok=True)
        with open("data/productos.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "nombre", "categoria", "precio", "stock"])
            for p in productos:
                writer.writerow([p.id, p.nombre, p.categoria, p.precio, p.stock])

    @staticmethod
    def registrar_venta(cliente: str, total: float, items: List[Dict]):
        os.makedirs("data", exist_ok=True)
        with open("data/ventas.csv", "a", newline="") as file:
            writer = csv.writer(file)
            for item in items:
                p = item["producto"]
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    cliente,
                    p.nombre,
                    item["cantidad"],
                    p.precio,
                    total
                ])

# ==================== SISTEMA PRINCIPAL ====================
class SaitmaPy:
    def __init__(self):
        self.productos = Database.cargar_productos()
        self.carrito = Carrito()

    def mostrar_menu(self):
        print("\n=== 🐾 SAITMA PY - VENTAS DE MASCOTAS ===")
        print("1. 📋 Ver productos")
        print("2. 🛒 Agregar al carrito")
        print("3. 🧾 Ver carrito")
        print("4. 💰 Finalizar compra")
        print("5. ❌ Salir")

    def ejecutar(self):
        print("¡Bienvenido a Saitma Py! 🐕🐈")

        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.mostrar_productos()
            elif opcion == "2":
                self.agregar_al_carrito()
            elif opcion == "3":
                self.carrito.mostrar()
            elif opcion == "4":
                self.finalizar_compra()
            elif opcion == "5":
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción no válida")

    def mostrar_productos(self):
        print("\n=== 🏷️ PRODUCTOS ===")
        for p in self.productos:
            print(p)

    def agregar_al_carrito(self):
        self.mostrar_productos()
        try:
            id_producto = int(input("\n🔹 ID del producto: "))
            cantidad = int(input("🔹 Cantidad: "))
            
            producto = next((p for p in self.productos if p.id == id_producto), None)
            if producto:
                self.carrito.agregar_producto(producto, cantidad)
            else:
                print("❌ Producto no encontrado")
        except ValueError:
            print("❌ Ingrese un número válido")

    def finalizar_compra(self):
        if not self.carrito.items:
            print("❌ El carrito está vacío")
            return

        self.carrito.mostrar()
        cliente = input("\n🔹 Nombre del cliente: ")

        confirmar = input("¿Confirmar compra? (s/n): ").lower()
        if confirmar == "s":
            total = self.carrito.calcular_total()
            Database.registrar_venta(cliente, total, self.carrito.items)
            Database.guardar_productos(self.productos)
            print(f"\n✅ Compra realizada. Total: ${total:.2f}")
            self.carrito = Carrito()  # Reiniciar carrito
        else:
            print("❌ Compra cancelada")

# ==================== EJECUCIÓN ====================
if __name__ == "__main__":
    sistema = SaitmaPy()
    sistema.ejecutar()
