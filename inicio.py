from modelos import Profesional

profesional = Profesional("Dr. Juan Nandez", "Pediatria", "Lunes y Viernes, 8:00-13:00")

# profesional.guardar_db()

# print(profesional)
# print(type(profesional))
# print(profesional.tabla)
# print(profesional.campos)
# print(profesional.nombre)
# print(profesional.saludar())

profesional = Profesional.obtener_profesional(3)
print(profesional)
print(type(profesional))
print((profesional.__dict__))