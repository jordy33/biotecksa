from sqlalchemy import func
from bio_backend.db import db
from datetime import datetime
from hashlib import sha256
import os
from sqlalchemy.orm import relation, synonym
from sqlalchemy import exc
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy import Column, Integer, Boolean, Unicode, LargeBinary, TEXT, TIMESTAMP,SmallInteger,Date, Numeric
from sqlalchemy import BigInteger
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.mysql import TINYINT

# +------------------+---------------------+------+-----+---------+----------------+
# | Field            | Type                | Null | Key | Default | Extra          |
# +------------------+---------------------+------+-----+---------+----------------+
# | id               | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
# | name             | varchar(255)        | NO   |     | NULL    |                |
# | email            | varchar(255)        | NO   | UNI | NULL    |                |
# | password         | varchar(255)        | NO   |     | NULL    |                |
# | remember_token   | varchar(100)        | YES  |     | NULL    |                |
# | created_at       | timestamp           | YES  |     | NULL    |                |
# | updated_at       | timestamp           | YES  |     | NULL    |                |
# | tipo_usuarios_id | int(10) unsigned    | YES  | MUL | NULL    |                |
# | is_admin         | tinyint(4)          | NO   |     | 0       |                |
# | idioma_id        | bigint(20) unsigned | YES  | MUL | 1       |                |
# | deleted_at       | timestamp(6)        | YES  |     | NULL    |                |
# | token_version    | int(11)             | NO   |     | NULL    |                |
# | users_id         | bigint(20) unsigned | YES  | MUL | NULL    |                |
# +------------------+---------------------+------+-----+---------+----------------+
class Users(db.Model):
    __tablename__ = 'users'
    id = Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    name = Column(Unicode(255))
    email = Column(Unicode(255))
    password = Column(Unicode(255))
    remember_token = Column(Unicode(255))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    tipo_usuarios_id = Column(INTEGER(unsigned=True))
    is_admin = Column(TINYINT)
    idioma_id = Column(INTEGER(unsigned=True))
    deleted_at = Column(TIMESTAMP)
    token_version = Column(Integer)
    users_id = Column(BIGINT(unsigned=True))

# mysql> desc users_has_cultivos;
# +-------------+---------------------+------+-----+----------------------+----------------+
# | Field       | Type                | Null | Key | Default              | Extra          |
# +-------------+---------------------+------+-----+----------------------+----------------+
# | id          | bigint(20) unsigned | NO   | PRI | NULL                 | auto_increment |
# | cultivos_id | int(10) unsigned    | NO   | MUL | NULL                 |                |
# | users_id    | bigint(20) unsigned | NO   | MUL | NULL                 |                |
# | created_at  | timestamp(6)        | NO   |     | CURRENT_TIMESTAMP(6) |                |
# | updated_at  | timestamp(6)        | NO   |     | CURRENT_TIMESTAMP(6) |                |
# | deleted_at  | timestamp(6)        | YES  |     | NULL                 |                |
# +-------------+---------------------+------+-----+----------------------+----------------+
#
class UsersHasCultivos(db.Model):
    __tablename__ = 'users_has_cultivos'
    id = Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    cultivos_id = Column(INTEGER(unsigned=True))
    users_id = Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
# mysql> desc cultivos;
# +---------------------+---------------------+------+-----+----------------------+----------------+
# | Field               | Type                | Null | Key | Default              | Extra          |
# +---------------------+---------------------+------+-----+----------------------+----------------+
# | id                  | int(10) unsigned    | NO   | PRI | NULL                 | auto_increment |
# | nombre              | varchar(100)        | YES  |     | NULL                 |                |
# | polyline            | longtext            | YES  |     | NULL                 |                |
# | fecha_inicio        | date                | NO   |     | NULL                 |                |
# | fecha_final         | date                | NO   |     | NULL                 |                |
# | clave_cultivo       | varchar(10)         | YES  | UNI | NULL                 |                |
# | predios_id          | bigint(20) unsigned | NO   | MUL | NULL                 |                |
# | tipos_cultivo_id    | int(10) unsigned    | NO   | MUL | NULL                 |                |
# | ambiente_cultivo_id | int(10) unsigned    | NO   | MUL | NULL                 |                |
# | ciclo_cultivo_id    | int(10) unsigned    | NO   | MUL | NULL                 |                |
# | created_at          | timestamp(6)        | NO   |     | CURRENT_TIMESTAMP(6) |                |
# | updated_at          | timestamp(6)        | NO   |     | CURRENT_TIMESTAMP(6) |                |
# | deleted_at          | timestamp(6)        | YES  |     | NULL                 |                |
# | creador_id          | bigint(20) unsigned | YES  | MUL | NULL                 |                |
# | zonas_horarias_id   | int(10) unsigned    | YES  | MUL | NULL                 |                |
# | hectareas           | double(15,8)        | NO   |     | 0.00000000           |                |
# +---------------------+---------------------+------+-----+----------------------+----------------+

class Cultivos(db.Model):
    __tablename__ = 'cultivos'
    id = Column(INTEGER(unsigned=True), autoincrement=True, primary_key=True)
    nombre = Column(Unicode(100))
    polyline = Column(LONGTEXT)
    fecha_inicio = Column(Date)
    fecha_final = Column(Date)
    clave_cultivo = Column(Unicode(10))
    predios_id = Column(BIGINT(unsigned=True))
    tipos_cultivo_id = Column(INTEGER(unsigned=True))
    ambiente_cultivo_id = Column(INTEGER(unsigned=True))
    ciclo_cultivo_id = Column(INTEGER(unsigned=True))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    creador_id= Column(BIGINT(unsigned=True))
    zonas_horarias_id = Column(INTEGER(unsigned=True))
    hectareas = Column(DOUBLE(15,8))

# mysql> desc cultivos_has_biodispositivos ;
# +---------------------+---------------------+------+-----+----------------------+----------------+
# | Field               | Type                | Null | Key | Default              | Extra          |
# +---------------------+---------------------+------+-----+----------------------+----------------+
# | id                  | bigint(20) unsigned | NO   | PRI | NULL                 | auto_increment |
# | cultivos_id         | int(10) unsigned    | NO   | MUL | NULL                 |                |
# | bio_dispositivos_id | bigint(20) unsigned | NO   | MUL | NULL                 |                |
# | created_at          | timestamp(6)        | NO   |     | CURRENT_TIMESTAMP(6) |                |
# | updated_at          | timestamp(6)        | NO   |     | CURRENT_TIMESTAMP(6) |                |
# | deleted_at          | timestamp(6)        | YES  |     | NULL                 |                |
# +---------------------+---------------------+------+-----+----------------------+----------------+

class CultivosHasBioDevices(db.Model):
    __tablename__ = 'cultivos_has_biodispositivos'
    id = Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    cultivos_id = Column(INTEGER(unsigned=True))
    bio_dispositivos_id = Column(BIGINT(unsigned=True))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)

# mysql> desc  bio_dispositivos;
# +-------------------------+---------------------+------+-----+---------+----------------+
# | Field                   | Type                | Null | Key | Default | Extra          |
# +-------------------------+---------------------+------+-----+---------+----------------+
# | id                      | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
# | nombre                  | varchar(250)        | YES  |     | NULL    |                |
# | identificador           | varchar(20)         | NO   |     | NULL    |                |
# | tipo_biodispositivos_id | int(10) unsigned    | NO   | MUL | NULL    |                |
# | bio_dispositivos_id     | bigint(20) unsigned | YES  | MUL | NULL    |                |
# | dispositivos_sms_id     | bigint(20) unsigned | YES  | MUL | NULL    |                |
# | notas                   | text                | YES  |     | NULL    |                |
# | created_at              | timestamp           | YES  |     | NULL    |                |
# | updated_at              | timestamp           | YES  |     | NULL    |                |
# | deleted_at              | timestamp           | YES  |     | NULL    |                |
# | position                | longtext            | YES  |     | NULL    |                |
# | clave                   | varchar(10)         | YES  | UNI | NULL    |                |
# | propietario_id          | bigint(20) unsigned | YES  | MUL | NULL    |                |
# | activo                  | tinyint(4)          | NO   |     | 0       |                |
# | recarga_saldo           | date                | YES  |     | NULL    |                |
# +-------------------------+---------------------+------+-----+---------+----------------+
# 15 rows in set (0.07 sec)

class BioDevices(db.Model):
    __tablename__ = 'bio_dispositivos'
    id = Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    nombre = Column(Unicode(250))
    identificador = Column(Unicode(20))
    tipo_biodispositivos_id = Column(INTEGER(unsigned=True))
    bio_dispositivos_id = Column(BIGINT(unsigned=True))
    dispositivos_sms_id = Column(BIGINT(unsigned=True))
    notas= Column(TEXT())
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    position = Column(LONGTEXT())
    clave = Column(Unicode(10))
    propietario_id = Column(INTEGER(unsigned=True))
    activo = Column(TINYINT())
    recarga_saldo = Column(Date())

# mysql> desc sensores_log;
# +-------------+---------------------+------+-----+---------+----------------+
# | Field       | Type                | Null | Key | Default | Extra          |
# +-------------+---------------------+------+-----+---------+----------------+
# | id          | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
# | valor       | varchar(250)        | YES  |     | NULL    |                |
# | valor_crudo | varchar(250)        | YES  |     | NULL    |                |
# | sensores_id | bigint(20) unsigned | NO   | MUL | NULL    |                |
# | created_at  | timestamp           | YES  |     | NULL    |                |
# | updated_at  | timestamp           | YES  |     | NULL    |                |
# | deleted_at  | timestamp           | YES  |     | NULL    |                |
# +-------------+---------------------+------+-----+---------+----------------+
# 7 rows in set (0.07 sec)

class SensoresLog(db.Model):
    __tablename__ = 'sensores_log'
    id = Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    valor = Column(Unicode(250))
    valor_crudo = Column(Unicode(20))
    sensores_id = Column(BIGINT(unsigned=True))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)

#
# mysql> desc tipo_biodispositivos;
# +-------------+------------------+------+-----+---------+----------------+
# | Field       | Type             | Null | Key | Default | Extra          |
# +-------------+------------------+------+-----+---------+----------------+
# | id          | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
# | tipo        | varchar(250)     | NO   |     | NULL    |                |
# | descripcion | text             | NO   |     | NULL    |                |
# | created_at  | timestamp        | YES  |     | NULL    |                |
# | updated_at  | timestamp        | YES  |     | NULL    |                |
# | deleted_at  | timestamp        | YES  |     | NULL    |                |
# | modulos     | tinyint(4)       | NO   |     | 0       |                |
# +-------------+------------------+------+-----+---------+----------------+
# 7 rows in set (0.06 sec)

class TipoBioDispositivos(db.Model):
    __tablename__ = 'tipo_biodispositivos'
    id = Column(INTEGER(unsigned=True), autoincrement=True, primary_key=True)
    tipo = Column(Unicode(250))
    descripcion = Column(TEXT())
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    modulos = Column(TINYINT())
