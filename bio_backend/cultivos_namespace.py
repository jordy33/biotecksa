from flask_restx import Namespace, Resource, fields
from bio_backend import config
from bio_backend.models import UsersHasCultivos,Cultivos,CultivosHasBioDevices,BioDevices,SensoresLog,TipoBioDispositivos
from bio_backend.db import db
from flask import abort
from datetime import datetime, timedelta

import requests
import json
import arrow

cultivos_namespace = Namespace('Cultivos', description='Cultivos information')
cultivos_parser = cultivos_namespace.parser()
cultivos_parser.add_argument('users_id', type=int, required=True, help='104',default=104)
cultivos_parser.add_argument('pageNumber', type=int, required=True, help='1',default=1)
cultivos_parser.add_argument('pageSize', type=int, required=True,default=20 )

last_log_pivot_info = {
    'bio_dispositivos_id': fields.Integer,
    'sensores_id': fields.Integer,
}
last_log_pivot_model = cultivos_namespace.model('LastLogPivot', last_log_pivot_info)
last_log_info = {
    'value_datetime': fields.String,
    'pivot': fields.Nested(last_log_pivot_model),
}
last_log_model = cultivos_namespace.model('LastLog', last_log_info)
pivot_info = {
    'cultivos_id': fields.Integer,
    'bio_dispositivos_id': fields.Integer,
}
pivot_model = cultivos_namespace.model('DevicesPivot', pivot_info)
devices_type_info = {
    'id': fields.Integer,
    'nombre': fields.String,
    'modulos': fields.Integer
}
device_type_model = cultivos_namespace.model('DevicesType', devices_type_info)
devices_info = {
    'nombre': fields.String,
    'clave': fields.String,
    'tipo_biodispositivos_id': fields.Integer,
    'pivot': fields.Nested(pivot_model),
    'last_log': fields.List(fields.Nested(last_log_model)),
    'device_type':fields.Nested(device_type_model)
}
devices_model = cultivos_namespace.model('CultivosDevices', devices_info)
cultivos_info = {
    'nombre': fields.String,
    'ciclo_cultivo_id': fields.Integer,
    'ambiente_cultivo_id': fields.Integer,
    'fecha_inicio': fields.String,
    'fecha_final': fields.String,
    'clave_cultivo': fields.String,
    'creador_id': fields.Integer,
    'id': fields.Integer,
    'predios_id': fields.Integer,
    'tipos_cultivo_id': fields.Integer,
    'devices': fields.List(fields.Nested(devices_model)),
}
cultivos_model = cultivos_namespace.model('Cultivos', cultivos_info)
meta_info = {
    'page': fields.Integer,
    'pages':fields.Integer,
    'total_count':fields.Integer,
    'prev':fields.Integer,
    'next_pag': fields.Integer
}
meta_model = cultivos_namespace.model('MetaModel', meta_info)
datacultivos_list = {
    'data':fields.List(fields.Nested(cultivos_model)),
     'meta':fields.Nested(meta_model)
}

cultivos_model = cultivos_namespace.model('CultivosList', datacultivos_list)

@cultivos_namespace.route('')
class cultivos(Resource):

    @cultivos_namespace.doc('')
    @cultivos_namespace.expect(cultivos_parser)
    @cultivos_namespace.marshal_with(cultivos_model, as_list=False)
    @cultivos_namespace.response(200, 'Success')
    @cultivos_namespace.response(404, 'Not found')
    def get(self):
        """
        Regresa la lista de Cultivos
        """

        kw = cultivos_parser.parse_args()
        userhascultivos = db.session.query(UsersHasCultivos).filter_by(users_id=kw['users_id']).paginate(page=kw["pageNumber"],per_page=kw["pageSize"])
        if not any(userhascultivos.items):
            abort(404)
        print("page:",userhascultivos.page)
        meta = {
            "page": userhascultivos.page,
            "pages": userhascultivos.pages,
            "total_count": userhascultivos.total,
            "prev": userhascultivos.prev_num,
            "next_pag": userhascultivos.next_num,
        }

        cultivos_rows = []
        for uhc in userhascultivos.items:
            cultivos = db.session.query(Cultivos).filter_by(id=uhc.cultivos_id).all()
            for each_cultivo in cultivos:
                bio_dev_rows=[]
                cultivos_has_bio_devices=db.session.query(CultivosHasBioDevices).filter_by(cultivos_id=each_cultivo.id).all()
                for each_bio_device_in_cultivos in cultivos_has_bio_devices:
                    bio_devices = db.session.query(BioDevices).filter_by(
                        id=each_bio_device_in_cultivos.bio_dispositivos_id).first()
                    if bio_devices is not None:
                        created_at=""
                        sensores_log_id=0
                        last_log_4sensor = db.session.query(SensoresLog).order_by(SensoresLog.id.desc()).first()
                        if last_log_4sensor is not None:
                            created_at=last_log_4sensor.created_at
                            sensores_log_id=last_log_4sensor.sensores_id
                        bio_type_name=""
                        bio_type_mod=0
                        bio_dev_type = db.session.query(TipoBioDispositivos).filter_by(id=bio_devices.tipo_biodispositivos_id).first()
                        if bio_dev_type is not None:
                            bio_type_name=bio_dev_type.tipo
                            bio_type_mod=bio_dev_type.modulos
                        bio_dev_rows.append({
                            "nombre": bio_devices.nombre,
                            "clave": bio_devices.clave,
                            "id": bio_devices.id,
                            "tipo_biodispositivos_id": bio_devices.tipo_biodispositivos_id,
                            "pivot":{ 'cultivos_id': each_cultivo.id,'bio_dispositivos_id': bio_devices.id},
                            "last_log":[{"value_datetime": created_at,"pivot": {"bio_dispositivos_id": each_bio_device_in_cultivos.bio_dispositivos_id,"sensores_id": sensores_log_id }}],
                            "device_type":{"id":4,"nombre":bio_type_name,"modulos":bio_type_mod}
                        })
                cultivos_rows.append({
                    'nombre': each_cultivo.nombre,
                    'ciclo_cultivo_id': each_cultivo.ciclo_cultivo_id,
                    'ambiente_cultivo_id': each_cultivo.ambiente_cultivo_id,
                    'fecha_inicio': each_cultivo.fecha_inicio,
                    'fecha_final': each_cultivo.fecha_final,
                    'clave_cultivo': each_cultivo.clave_cultivo,
                    'creador_id': each_cultivo.creador_id,
                    'id': each_cultivo.id,
                    'predios_id': each_cultivo.predios_id,
                    'tipos_cultivo_id': each_cultivo.tipos_cultivo_id,
                    'devices':bio_dev_rows,
                })
        return {'data':cultivos_rows,'meta':meta}