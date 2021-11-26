from flask import jsonify


def custom_rest_response(**kwargs):
    result = {}
    if "data" in kwargs.keys():
        result.update({"success": True, "data": kwargs["data"]})
    else:
        result = {
            "success": False,
            "error": {
                "type": kwargs.get("error_type", "ValidationError"),
                "status": kwargs["status_code"],
                "detail": kwargs["error_msg"],
            },
        }
    return result, kwargs.get("status_code", 200)


def custom_jsonify(**kwargs):
    result = {}
    if "data" in kwargs.keys():
        result.update({"success": True, "data": kwargs["data"]})
    else:
        result = {
            "success": False,
            "error": {
                "type": kwargs.get("error_type", "ValidationError"),
                "status": kwargs["status_code"],
                "detail": kwargs["error_msg"],
            },
        }
    return jsonify(result), kwargs.get("status_code", 200)
