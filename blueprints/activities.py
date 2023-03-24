import config
import json

from flask import Blueprint, jsonify, request, g
from pydantic import BaseModel, validator, Extra, ValidationError

from utils.utils import generic_api_requests

activities = Blueprint(name="activities", import_name=__name__)


class ActivityCreationFilterInput(BaseModel, extra=Extra.forbid):
    name: str

    @validator("name")
    def validate_name(cls, value):
        if value == "":
            raise ValueError("can not be empty")
        return value



@activities.route("/", methods=["POST"], strict_slashes=False)
def create_activity():
    try:

        request_body = json.loads(
            ActivityCreationFilterInput(**request.get_json()).json()
        )

        is_success, response = generic_api_requests(
            "post", config.URL_ACTIVITIES, request_body
        )

        response_body = {
            "success": is_success,
            "data": response["json"] if is_success else {"message": str(response)},
        }

        return jsonify(response_body)

    except ValidationError as e:
        print(g.execution_id, " VALIDATION ERROR", e)

        response = {
            "success": 0,
            "data": {"message": ("RTFM {}".format(e))},
        }

        return response, 400

    except Exception as error:

        response_body = {
            "success": 0,
            "data": {"message": "Error : {}".format(error)},
        }

        return jsonify(response_body), 400