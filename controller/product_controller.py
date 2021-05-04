from flask import jsonify, Blueprint
from flask_request_validator import GET, Param, Enum, validate_params


def create_product_endpoints(product_service, Session):

    product_app = Blueprint("product_app", __name__, url_prefix="/api/products")

    @product_app.route("/category", methods=["GET"])
    def product_category():
        session = Session()
        try:
            # 메뉴 데이터
            categories = product_service.get_menu(None, session)

            # 각 카테고리를 저장하기 위한 리스트
            second_category, first_category, main_category = [], [], []

            # JOIN 을 하며 생기는 중복을 제거하기 위해서 중복 체크 후 리스트에 저장
            for category in categories:

                # 1. (메인 카테고리의 id, 이름) 이 main_category 에 없을 경우 append
                if (category.m_id, category.main_category_name) not in main_category:
                    main_category.append((category.m_id, category.main_category_name))

                # 2. (1차 카테고리의 id, 이름, 이에 해당하는 메인 카테고리의 id) 가 first_category 에 없을 경우 append
                if (
                    category.f_id,
                    category.first_category_name,
                    category.main_category_id,
                ) not in first_category:
                    first_category.append(
                        (category.f_id, category.first_category_name, category.main_category_id)
                    )

                # 3. (2차 카테고리의 id, 이름, 이에 해당하는 1차 카테고리의 id) 가 second_category 에 없을 경우 append
                second_category.append(
                    (category.s_id, category.second_category_name, category.first_category_id)
                )

            # 카테고리의 계층 구조를 전달하기 위한 JSON 형식
            body = [
                {
                    # 메인 카테고리의 id 와 이름
                    "id": m_menu[0],
                    m_menu[1]: [
                        {
                            # 1차 카테고리의 id 와 이름
                            "id": f_menu[0],
                            f_menu[1]: [
                                {
                                    # 2차 카테고리의 id 와 이름
                                    "id": s_menu[0],
                                    "name": s_menu[1],
                                }
                                for s_menu in second_category
                                if s_menu[2] == f_menu[0]
                            ],
                        }
                        for f_menu in first_category
                        if f_menu[2] == m_menu[0]
                    ],
                }
                for m_menu in main_category
            ]

            return jsonify(body), 200

        except Exception as e:
            return jsonify({"message": f"{e}"}), 500

        finally:
            session.close()

    @product_app.route("", methods=["GET"])
    @validate_params(
        Param("limit", GET, int, default=100, required=False),
        Param("offset", GET, int, required=False),
        Param("main_category_id", GET, int, rules=[Enum(4, 5, 6)], required=False),
        Param("first_category_id", GET, int, required=False),
        Param("second_category_id", GET, int, required=False),
        Param("is_promotion", GET, int, rules=[Enum(0, 1)], required=False),
        Param("select", GET, int, rules=[Enum(0, 1)], required=False),
        Param("q", GET, str, required=False),
        Param("all_items", GET, int, rules=[Enum(1)], required=False),
    )
    def products(*args):
        session = Session()
        try:
            # args[2]: 메인 카테고리의 pk, args[8]: 전체 상품을 보여줄 지 판단하는 파라미터, args[3]: 1차 카테고리의 pk, args[4]: 2차 카테고리의 pk
            if args[2] == 5 or args[2] == 6 and not args[8] and not args[3] and not args[4]:

                # 특정 메인 카테고리 아이디 (5: 브랜드, 6: 뷰티) 파라미터만 들어올 경우 베스트 상품, 추천 상품 데이터 등을 전달
                body = {
                    "best_items": [],
                    "brand_items": [],
                    "recommended_items": [],
                    "category_items": [],
                }

                # 1. 파라미터로 들어온 카테고리의 id (args[2]) 에 따라 특정 셀러를 지정하고 상품 5개만 가져오기 위해 선언,
                # 2. 특정 1차 카테고리 아이디로 필터링된 상품 리스트를 가져오기 위해 선언
                if args[2] == 5:
                    f_cat_list = (12, 13, 14, 15, 16, 17, 18)
                    seller_id = 30

                else:
                    f_cat_list = (23, 24, 25, 26, 27, 28)
                    seller_id = 359

                for f_cat_id in f_cat_list:
                    # 1. 첫 번째 카테고리 상품 5개 씩 보여주기 위한 필터
                    f_category_filter = {"first_category_id": f_cat_id, "limit": 5}

                    # 2. 카테고리의 id, name 과 함께 상품 리스트를 반환한다.
                    category_products = {
                        "category_id": f_cat_id,
                        "category_name": product_service.get_menu(f_cat_id, session)[
                            0
                        ].first_category_name,
                        "product": product_service.get_products(f_category_filter, session),
                    }

                    body["category_items"].append(category_products)

                # Best 상품 필터 - 해당하는 메인 카테고리의 상품 중 판매량 순 10개만 가져오기 위해 선언
                best_prod_filter = {
                    "main_category_id": args[2],
                    "limit": 10,
                }
                best_products = product_service.get_products(best_prod_filter, session)

                # 추천 상품 필터 - 할인율 기준
                recommended_prod_filter = {
                    "main_category_id": args[2],
                    "limit": 30,
                    "discount_rate": 1,
                }
                recommended_products = product_service.get_products(
                    recommended_prod_filter, session
                )

                # 특정 셀러 상품 리스트 필터
                seller_filter = {"main_category_id": args[2], "seller_id": seller_id}
                brand_products = product_service.get_products(seller_filter, session)

                body["best_items"] = best_products
                body["brand_items"] = brand_products
                body["recommended_items"] = recommended_products

                return body

            # 필터링을 위한 딕셔너리
            filter_dict = dict()

            # pagination
            filter_dict["limit"] = args[0]
            filter_dict["offset"] = args[1]

            # 카테고리
            filter_dict["main_category_id"] = args[2]
            filter_dict["first_category_id"] = args[3]
            filter_dict["second_category_id"] = args[4]

            # 세일
            filter_dict["is_promotion"] = args[5]

            # 판매량순, 최신순
            filter_dict["select"] = args[6]

            # 검색 필터
            filter_dict["q"] = args[7]

            # 메인 카테고리의 모든 상품 필터
            filter_dict["all_items"] = args[8]

            body = dict()

            # 상품 데이터
            body["products"] = product_service.get_products(filter_dict, session)

            # 검색어가 들어올 경우 전달하는 셀러 정보
            if filter_dict["q"]:

                # 필터링된 셀러 리스트를 가져오기 위한 필터
                seller_info = dict()
                seller_info["name"] = filter_dict["q"]
                seller_info["limit"] = 100

                # 검색된 셀러 리스트 정의
                sellers = dict()

                # 검색어에 해당하는 셀러의 리스트
                seller_list = [
                    dict(seller) for seller in product_service.get_sellers(seller_info, session)
                ]

                # 셀러 검색 결과 개수
                sellers["count"] = len(seller_list)

                # 셀러 데이터
                sellers["seller_list"] = seller_list

                body["sellers"] = sellers

            return jsonify(body), 200

        except Exception as e:
            return jsonify({"message": f"{e}"}), 500

        finally:
            session.close()

    @product_app.route("/product/<int:product_id>", methods=["GET"])
    def product(product_id):
        session = Session()
        try:
            # 상품 데이터
            body = dict(product_service.get_product(product_id, session))

            return jsonify(body), 200

        except Exception as e:
            return jsonify({"message": f"{e}"}), 500

        finally:
            session.close()

    @product_app.route("/seller", methods=["GET"])
    @validate_params(
        Param("limit", GET, int, default=100, required=False),
        Param("offset", GET, int, required=False),
        Param("main_category_id", GET, int, rules=[Enum(4, 5, 6)], required=False),
        Param("select", GET, int, rules=[Enum(0, 1)], default=1, required=False),
    )
    def sellers(*args):
        session = Session()
        try:
            # 필터링을 위한 딕셔너리
            seller_dict = dict()
            seller_dict["limit"] = args[0]
            seller_dict["offset"] = args[1]
            seller_dict["main_category_id"] = args[2]
            seller_dict["select"] = args[3]

            # 셀러 데이터
            body = [dict(seller) for seller in product_service.get_sellers(seller_dict, session)]

            return jsonify(body), 200

        except Exception as e:
            return jsonify({"message": f"{e}"}), 500

        finally:
            session.close()

    return product_app
