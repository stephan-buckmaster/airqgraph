import os
from api import app, db
from flask_cors import CORS, cross_origin
import hashlib

from werkzeug.middleware.proxy_fix import ProxyFix

# Need for prod deployments
app.wsgi_app = ProxyFix(
  app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from flask import request, jsonify, abort

from api.queries import listAirVisualDeviceMeasurements_resolver, getAirVisualDeviceMeasurement_resolver, getLatestAirVisualDeviceMeasurement_resolver
from api.mutations import create_air_visual_device_measurement_resolver

from ariadne.explorer import ExplorerPlayground
from flask_httpauth import HTTPTokenAuth


PLAYGROUND_HTML = ExplorerPlayground(title="Air Quality Monitoring Data API").html(None)


query = ObjectType("Query")
mutation = ObjectType("Mutation")

query.set_field("listAirVisualDeviceMeasurements", listAirVisualDeviceMeasurements_resolver)
query.set_field("getAirVisualDeviceMeasurement", getAirVisualDeviceMeasurement_resolver)
query.set_field("getLatestAirVisualDeviceMeasurement", getLatestAirVisualDeviceMeasurement_resolver)

mutation.set_field("createAirVisualDeviceMeasurement", create_air_visual_device_measurement_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)
CORS(app)

tokens = {
  "secret": "token",
  "secret-token-2": "susan"
}

from functools import cache
@cache
def get_token_hashes(token_file):
  return [ line.strip() for line in open(token_file) if not '#' in line]

auth = HTTPTokenAuth(scheme='Bearer')
def verify_token(token):
  token_hash = hashlib.sha256(token.encode('utf-8')).hexdigest()
  app.logger.info(f"Look for token hash {token} -> {token_hash}")
  if token_hash in get_token_hashes(os.getenv("BEARER_AUTH_FILE")):
    return True

def bearer_token_valid():
  token_file = os.getenv("BEARER_AUTH_FILE")
  if token_file is None:
    return True
  app.logger.info(f"Check token {auth.get_auth().token}")
  return verify_token(auth.get_auth().token)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    if not bearer_token_valid():
      abort(401, "Bearer authentication failed")

    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code
