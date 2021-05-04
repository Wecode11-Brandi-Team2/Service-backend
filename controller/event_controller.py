from sqlalchemy import exc
from flask import jsonify, Blueprint
from flask_request_validator import GET, Param, validate_params


def create_event_endpoints(event_service, Session):
    # Blueprint 설정
    event_app = Blueprint("event_app", __name__, url_prefix="/api/events")

    @event_app.route("", methods=["GET"])
    @validate_params(
        Param("is_displayed", GET, int, required=False),
        Param("limit", GET, int, required=False, default=30),
        Param("offset", GET, int, required=False),
    )
    def select_event_list(*args):
        session = Session()
        try:
            event_info = {"is_displayed": args[0], "limit": args[1], "offset": args[2]}

            get_event_list = event_service.select_event_list(event_info, session)

            if not get_event_list:
                return jsonify({"message": "EMPTY_DATA"}), 400
            return jsonify({"data": get_event_list}), 200

        except exc.InvalidRequestError:
            return jsonify({"message": "INVALID_URL"}), 400

        except exc.ProgrammingError:
            return jsonify({"message": "ERROR_IN_SQL_SYNTAX"}), 500

        except Exception as e:
            return jsonify({"message": f"{e}"}), 500

        finally:
            session.close()

    @event_app.route("/detail", methods=["GET"])
    @validate_params(Param("id", GET, int, required=False))
    def select_event_detail(*args):
        session = Session()
        try:
            event_info = {"id": args[0]}

            get_event_detail, get_event_button = event_service.select_event_detail(
                event_info, session
            )

            if not get_event_detail:
                return jsonify({"event_detail": "EMPTY_DATA"}), 400
            if not get_event_button:
                return jsonify({"event_button": 0, "event_detail": get_event_detail}), 200

            return (
                jsonify({"event_detail": get_event_detail, "event_button": get_event_button}),
                200,
            )

        except exc.InvalidRequestError:
            return jsonify({"message": "INVALID_URL"}), 400

        except exc.ProgrammingError:
            return jsonify({"message": "ERROR_IN_SQL_SYNTAX"}), 500

        except Exception as e:
            return jsonify({"message": f"{e}"}), 500

        finally:
            session.close()

    @event_app.route("/products", methods=["GET"])
    @validate_params(
        Param("id", GET, int, required=True),
        Param("button_id", GET, int, required=True),
        Param("limit", GET, int, required=False, default=30),
        Param("offset", GET, int, required=False),
    )
    def select_event_products(*args):
        session = Session()
        try:
            event_info = {"id": args[0], "button_id": args[1], "limit": args[2], "offset": args[3]}

            get_event_products = event_service.select_event_products(event_info, session)

            if not get_event_products:
                return jsonify({"message": "EMPTY_DATA"}), 400
            return jsonify({"event_product": get_event_products}), 200

        except exc.InvalidRequestError:
            return jsonify({"message": "INVALID_URL"}), 400

        except exc.ProgrammingError:
            return jsonify({"message": "ERROR_IN_SQL_SYNTAX"}), 500

        except Exception as e:
            return jsonify({"message": f"{e}"}), 500

        finally:
            session.close()

    return event_app
