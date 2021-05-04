import jwt

from flask import Blueprint, request, jsonify, g
from flask_request_validator import GET, Param, Enum, validate_params

from config import SECRET_KEY, ALGORITHM
from util import login_required


def create_qna_endpoints(qna_service, Session):

    qna_app = Blueprint("qna_app", __name__, url_prefix="/api/qnas")

    @qna_app.route("/qna", methods=["POST", "DELETE"])
    @login_required
    def qna():
        session = Session()
        try:
            if request.method == "POST":

                # 문의 입력을 위한 데이터를 받는다.
                qna_info = {
                    "type_id": request.json["type_id"],
                    "user_id": g.user_id["user_id"],
                    "product_id": request.json["product_id"],
                    "content": request.json["content"],
                    "is_private": request.json["is_private"],
                }

                qna_service.insert_question(qna_info, session)

                session.commit()

                return jsonify({"message": "INSERT_SUCCESS"}), 200

            # 삭제하려는 유저와 문의한 유저가 일치하는지 id 를 통해 확인
            question_info = {
                "question_id": request.args.get("question_id"),
                "user_id": g.user_id["user_id"],
            }

            row_count = qna_service.delete_question(question_info, session)

            # 유저 아이디가 매칭될 경우 row_count = 1, token의 유저 id 와 삭제하려는 유저의 id 가 다를 경우 0
            if row_count == 0:
                return jsonify({"message": "DELETE_FAILED"}), 400

            session.commit()

            return jsonify({"message": "DELETE_SUCCESS"}), 200

        except KeyError:
            return jsonify({"message": "KEY_ERROR"}), 400

        except Exception as e:
            session.rollback()
            return jsonify({"message": f"{e}"}), 500

        finally:
            session.close()

    @qna_app.route("", methods=["GET"])
    @validate_params(
        Param("limit", GET, int, default=100, required=False),
        Param("offset", GET, int, required=False),
        Param("product_id", GET, int, required=True),
    )
    def qnas(*args):
        session = Session()
        try:
            qna_info = dict()

            # pagination
            qna_info["limit"] = args[0]
            qna_info["offset"] = args[1]

            # 상품 상세페이지 상품 아이디
            qna_info["product_id"] = args[2]

            # 로그인한 유저의 문의인지 판단하기 위해 토큰을 통해 id를 가져온다.
            access_token = request.headers.get("Authorization")
            if access_token:
                payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            else:
                payload = None

            body = {
                "login_user_id": payload,
                "qna": [dict(qna) for qna in qna_service.get_qnas(qna_info, session)],
            }

            return jsonify(body), 200

        except Exception as e:
            return jsonify({"message": f"{e}"}), 500

        finally:
            session.close()

    @qna_app.route("/user", methods=["GET"])
    @login_required
    @validate_params(
        Param("limit", GET, int, default=100, required=False),
        Param("offset", GET, int, required=False),
        Param("product_id", GET, int, required=False),
        Param("is_answered", GET, int, rules=[Enum(0, 1)], required=False),
    )
    def user_qnas(*args):
        session = Session()
        try:
            qna_info = dict()

            # pagination
            qna_info["limit"] = args[0]
            qna_info["offset"] = args[1]

            # 상품 아이디 (특정 상품의 상세페이지에서 내가 쓴 문의 필터링을 위해)
            qna_info["product_id"] = args[2]

            # 유저의 아이디
            qna_info["user_id"] = g.user_id["user_id"]

            # 답변 여부
            qna_info["is_answered"] = args[3]

            body = [dict(qna) for qna in qna_service.get_qnas(qna_info, session)]

            return jsonify(body), 200

        except Exception as e:
            return jsonify({"message": f"{e}"}), 500

        finally:
            session.close()

    return qna_app
