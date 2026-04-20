from app import create_app, db, bcrypt
from app.models import Usuario

app = create_app()

with app.app_context():
    password_hash = bcrypt.generate_password_hash('admin123').decode('utf-8')
    
    usuario = Usuario(
        nombre = 'Owner Principal',
        email = 'owner@restaurante.com',
        password=password_hash,
        rol = 'owner'
    )
    
    db.session.add(usuario)
    db.session.commit()
    print('Usuario creado exitosamente')
    
    