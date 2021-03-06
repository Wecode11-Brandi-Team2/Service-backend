import simplejson

from flask import request, Blueprint, jsonify, g
from flask_request_validator import Param, JSON, validate_params

from util import login_required


def create_order_endpoints(order_service, Session):
    # Blueprint 설정
    order_app = Blueprint("order_app", __name__, url_prefix="/api/order")

    @order_app.route("", methods=["POST"], endpoint="insert_order")
    @login_required
    @validate_params(
        Param("total_payment", JSON, int, required=True),
        Param("shipping_memo", JSON, str, required=True),
        Param("orderer_name", JSON, str, required=True),
        Param("orderer_phone", JSON, str, required=True),
        Param("orderer_email", JSON, str, required=True),
        Param("receiver_name", JSON, str, required=True),
        Param("receiver_phone", JSON, str, required=True),
        Param("receiver_address", JSON, str, required=True),
        Param("product_id", JSON, int, required=True),
        Param("price", JSON, int, required=True),
        Param("option_color", JSON, str, required=True),
        Param("option_size", JSON, str, required=True),
        Param("units", JSON, int, required=True),
    )
    def insert_orders(*args, **kwargs):
        session = Session()
        try:
            order_info = request.json
            user_id = g.user_id
            order_service.insert_orders(order_info, user_id, session)

            session.commit()
            return jsonify({"message": "SUCCESS"}), 200

        except Exception as e:
            session.rollback()
            return jsonify({"message": f"{e}"}), 500

        finally:
            session.close()

    @order_app.route("/item", methods=["GET"], endpoint="select_order_item_info")
    @login_required
    def select_order_item_info():
        session = Session()
        try:
            user_id = g.user_id
            get_order_item_info = order_service.select_order_item(user_id, session)

            if not get_order_item_info:
                return jsonify({"message": "EMPTY_DATA"}), 400
            return jsonify({"data": get_order_item_info}), 200

        except Exception as e:
            session.rollback()
            return jsonify({"message": f"{e}"}), 500

        finally:
            session.close()

    @order_app.route("/cancel", methods=["POST"], endpoint="insert_cancel_reason")
    @login_required
    def insert_cancel_reason():
        session = Session()
        try:
            cancel_info = request.json
            user_id = g.user_id
            order_service.insert_cancel_reason(cancel_info, user_id, session)

            session.commit()
            return jsonify({"message": "SUCCESS"}), 200

        except Exception as e:
            session.rollback()
            return jsonify({"message": f"{e}"}), 500

        finally:
            session.close()

    @order_app.route("/refund", methods=["POST"], endpoint="insert_refund_reason")
    @login_required
    def insert_refund_reason():
        session = Session()
        try:
            refund_info = request.json
            user_id = g.user_id
            order_service.insert_refund_reason(refund_info, user_id, session)

            session.commit()
            return jsonify({"message": "SUCCESS"}), 200

        except Exception as e:
            session.rollback()
            return jsonify({"message": f"{e}"}), 500

        finally:
            session.close()

    @order_app.route("/refundCancel", methods=["POST"], endpoint="insert_refund_cancel")
    @login_required
    def insert_refund_cancel():
        session = Session()
        try:
            refund_cancel_info = request.json
            user_id = g.user_id
            order_service.insert_refund_cancel(refund_cancel_info, user_id, session)

            session.commit()
            return jsonify({"message": "SUCCESS"}), 200

        except Exception as e:
            session.rollback()
            return jsonify({"message": f"{e}"}), 500

        finally:
            session.close()

    return order_app
