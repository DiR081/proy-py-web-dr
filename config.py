from decouple import config

class Config:
    SECRET_KEY = 'EsMiClav3S3cret4'

class DevelomentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/Proj_PythonWeb_Cfacil' # Gestor Usuario Contrasena Ruta NombBaseDatos
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'bk1.df.rodriguez@gmail.com'
    MAIL_PASSWORD = config('MAIL_PASSWORD') #MAIL_PASSWORD #OS

configDic = {
    'development' : DevelomentConfig,
    'default' : DevelomentConfig
}
