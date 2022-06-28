from flask_restx import Namespace, Resource, fields
from bio_backend import config
from bio_backend.models import Users
from bio_backend.db import db
from flask import abort
from datetime import datetime, timedelta

import requests
import json
import arrow

users_namespace = Namespace('Users', description='Users information')


def authentication_header_parser(value):
    data = validate_token_header(value, config.PUBLIC_KEY)
    if data is None:
        abort(401)
    return data


# Input and output formats for Elisa
users_parser = users_namespace.parser()
users_parser.add_argument('pageNumber', type=int, required=True, help='1',default=1)
users_parser.add_argument('pageSize', type=int, required=True,default=20 )

users_info = {
    'name': fields.String,
    'email': fields.String,
    'password': fields.String,
    'remember_token': fields.String,
    'created_at': fields.String,
    'updated_at': fields.String,
    'tipo_usuarios_id': fields.Integer,
    'is_admin': fields.Integer,
    'idioma_id': fields.Integer,
    'deleted_at': fields.String,
    'token_version':fields.String,
    'users_id':fields.Integer,
}
users_model = users_namespace.model('User', users_info)
meta_info = {
    'page': fields.Integer,
    'pages':fields.Integer,
    'total_count':fields.Integer,
    'prev':fields.Integer,
    'next_pag': fields.Integer
}
meta_model = users_namespace.model('Model', meta_info)
trackers_list = {
    'users':fields.List(fields.Nested(users_model)),
    'meta':fields.Nested(meta_model)
}

users_model = users_namespace.model('UsersList', trackers_list)

@users_namespace.route('')
class users(Resource):

    @users_namespace.doc('users')
    @users_namespace.expect(users_parser)
    @users_namespace.marshal_with(users_model, as_list=False)
    @users_namespace.response(200, 'Success')
    @users_namespace.response(404, 'Not authorized')
    def get(self):
        """
        Return the list of trackers in the appID of the token given
        """

        kw = users_parser.parse_args()
        print("pagenumber:",kw["pageNumber"])
        #usr = authentication_header_parser(auth['Authorization'])
        rows = []
# .filter_by(application_id=usr['application_id'],internal_id=usr['internal_id'])
        users = db.session.query(Users).paginate(page=kw["pageNumber"],per_page=kw["pageSize"])
        meta = {
            "page": users.page,
            "pages": users.pages,
            "total_count": users.total,
            "prev": users.prev_num,
            "next_pag": users.next_num,
        }
        for user in users.items:
            rows.append({
                'name': user.name,
                'email': user.email,
                'password ': user.password,
                'remember_token': user.remember_token,
                'created_at':user.created_at,
                'updated_at': user.updated_at,
                'tipo_usuarios_id': user.tipo_usuarios_id,
                'is_admin': user.is_admin,
                'idioma_id': user.idioma_id,
                'deleted_at': user.deleted_at,
                'token_version': user.token_version,
                'users_id': user.users_id,
            })
        return {'users':rows,'meta':meta}