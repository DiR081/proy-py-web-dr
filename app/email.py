# Importamos capacidad de enviar mensaje a travez de la las funciones de "message"
from flask_mail import Message
# Importamos capacidad de usar las APP del proyecto
from flask import current_app, render_template
# Importamos herramientas paara envio asincrona del correo
from threading import Thread
# Importar la funcion envio correos
from . import mail, app

# Funcion Envia correo de forma asincrona
def envia_correo_asincrono(message):
    with app.app_context ():
        # Envio el correo
        mail.send(message)


def mail_bienvenida(user):
    # Se crea el Titulo, de y para
    message = Message('Bienvenido al Curso de Python de Código Fácilito.',
                        sender=current_app.config['MAIL_USERNAME'],
                        recipients=[user.email])
    # Confiruro el cuerpo del correo
    message.html = render_template('email/correobienvenida.html', user=user)
    # cargo el mensaje a enviar
    thread = Thread(target=envia_correo_asincrono, args=[message])
    thread.start()
