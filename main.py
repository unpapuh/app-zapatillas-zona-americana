import flet as ft
import json
import os

ARCHIVO = "inventario.json"

def cargar_inventario():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def guardar_inventario(inventario):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)

def main(page: ft.Page):
    page.title = "Zona Americana"
    page.window_width = 900
    page.window_height = 700
    page.bgcolor = "#FAF3F3"
    page.scroll = ft.ScrollMode.AUTO

    inventario = cargar_inventario()

    def vista_inicio():
        boton_coleccion = ft.ElevatedButton(
            "Explorar Colección",
            bgcolor="#111",
            color="white",
            on_click=lambda e: page.go("/coleccion")
        )

        boton_buscar = ft.ElevatedButton(
            "🔎 Buscar por Talle",
            bgcolor="#111",
            color="white",
            on_click=lambda e: page.go("/buscar")
        )

        return ft.View(
            route="/",
            controls=[
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                    controls=[
                        ft.Text("ZONA AMERICANA", size=40, weight=ft.FontWeight.BOLD),
                        ft.Row([boton_coleccion, boton_buscar], alignment=ft.MainAxisAlignment.CENTER),
                    ]
                )
            ]
        )

    def vista_coleccion():
        marca = ft.TextField(label="Marca", width=150)
        modelo = ft.TextField(label="Modelo", width=150)
        talle = ft.TextField(label="Talle", width=80)

        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Marca")),
                ft.DataColumn(ft.Text("Modelo")),
                ft.DataColumn(ft.Text("Talle")),
                ft.DataColumn(ft.Text("Eliminar")),
            ],
            rows=[]
        )

        def actualizar_tabla():
            tabla.rows.clear()
            for index, item in enumerate(inventario):
                eliminar_btn = ft.IconButton(
                    ft.Icons.DELETE,
                    icon_color="red",
                    tooltip="Eliminar",
                    on_click=lambda e, i=index: eliminar_zapatilla(i)
                )
                tabla.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(item["marca"])),
                            ft.DataCell(ft.Text(item["modelo"])),
                            ft.DataCell(ft.Text(item["talle"])),
                            ft.DataCell(eliminar_btn)
                        ]
                    )
                )
            page.update()

        def agregar_zapatilla(e):
            if not marca.value or not modelo.value or not talle.value:
                page.snack_bar = ft.SnackBar(ft.Text("Completa todos los campos."), open=True)
                page.update()
                return

            inventario.append({
                "marca": marca.value,
                "modelo": modelo.value,
                "talle": talle.value
            })
            guardar_inventario(inventario)
            actualizar_tabla()

            marca.value = modelo.value = talle.value = ""
            page.update()

        def eliminar_zapatilla(i):
            inventario.pop(i)
            guardar_inventario(inventario)
            actualizar_tabla()

        boton_agregar = ft.ElevatedButton("Agregar Zapatilla", on_click=agregar_zapatilla)
        boton_volver = ft.ElevatedButton("⬅ Volver", on_click=lambda e: page.go("/"))

        actualizar_tabla()

        return ft.View(
            route="/coleccion",
            controls=[
                ft.Text("Colección de Zapatillas", size=26, weight=ft.FontWeight.BOLD),
                ft.Row([marca, modelo, talle, boton_agregar], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(),
                tabla,
                ft.Container(boton_volver, alignment=ft.alignment.center)
            ]
        )

    def vista_busqueda():
        input_talle = ft.TextField(label="Buscar por talle", width=200)
        resultados = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

        def buscar_zapatillas(e):
            resultados.controls.clear()
            inventario_actualizado = cargar_inventario()
            talle_buscado = input_talle.value.strip()
            if not talle_buscado:
                resultados.controls.append(ft.Text("Ingresa un talle.", color="red"))
            else:
                filtradas = [z for z in inventario_actualizado if z["talle"] == talle_buscado]
                if filtradas:
                    for z in filtradas:
                        resultados.controls.append(
                            ft.Container(
                                bgcolor="#eee",
                                padding=10,
                                border_radius=8,
                                content=ft.Column([
                                    ft.Text(f"{z['marca']} - {z['modelo']}", size=18, weight="bold"),
                                    ft.Text(f"Talle: {z['talle']}")
                                ])
                            )
                        )
                else:
                    resultados.controls.append(ft.Text("No se encontraron zapatillas para ese talle."))

            page.update()

        boton_buscar = ft.ElevatedButton("Buscar", on_click=buscar_zapatillas)
        boton_volver = ft.ElevatedButton("⬅ Volver", on_click=lambda e: page.go("/"))

        return ft.View(
            route="/buscar",
            controls=[
                ft.Text("🔎 Buscar Zapatillas por Talle", size=24, weight="bold"),
                ft.Row([input_talle, boton_buscar], alignment=ft.MainAxisAlignment.CENTER),
                resultados,
                ft.Container(boton_volver, alignment=ft.alignment.center)
            ]
        )

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(vista_inicio())
        elif page.route == "/coleccion":
            page.views.append(vista_coleccion())
        elif page.route == "/buscar":
            page.views.append(vista_busqueda())
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)


