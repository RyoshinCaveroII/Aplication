import pandas as pd
from models import db, Book
from app import app  # Importamos la instancia de Flask desde app.py

# Leer el archivo CSV
csv_file = 'plantilla_libros.csv'
data = pd.read_csv(csv_file)

# Verifica que las columnas coincidan con tu modelo Book
print(data.head())  # Revisa la estructura de los datos

# Importar los datos a la base de datos
with app.app_context():
    db.create_all()  # Crea las tablas si no existen
    for _, row in data.iterrows():
        book = Book(
            id=row['ID'],  
            title=row['Título'],
            author=row['Autor'],
            genre=row['Género'],
            year=row['Año de Publicación'],
            rating=row['Calificación Promedio'],
            pages=row['Número de Páginas'],
            price=row['Precio (USD)']
        )
        db.session.add(book)
    db.session.commit()  # Guarda los cambios en la base de datos
    print("Books imported successfully!")
