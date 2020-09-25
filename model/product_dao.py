from sqlalchemy import text

class ProductDao:
    def get_menu(self, session):
        """ 카테고리 데이터 전달
        
        args:
            session: 데이터베이스 session 객체

        returns :
            200: 메뉴 리스트

        Authors:
            고지원

        History:
            2020-09-21 (고지원): 초기 생성
            2020-09-24 (고지원): 하나씩 존재했던 3개의 카테고리 정보를 가져오는 메소드를 JOIN 을 통해 한 번에 전달하도록 수정
        """
        row = session.execute(("""
            SELECT
                m_cat.id AS m_id, 
                m_cat.main_category_name,
                f_cat.id AS f_id,
                f_cat.first_category_name,
                f_cat.main_category_id,
                s_cat.id AS s_id,
                s_cat.second_category_name,
                s_cat.first_category_id
            FROM main_categories AS m_cat 
            LEFT OUTER JOIN first_categories AS f_cat ON m_cat.id = f_cat.main_category_id
            LEFT OUTER JOIN second_categories AS s_cat ON f_cat.id = s_cat.first_category_id
        """))
        return row

    def get_seller(self, seller_id, session):
        """ 셀러 정보 전달

        args:
            seller_id: 셀러를 판단하기 위한 아이디
            session: 데이터베이스 session 객체

        returns :
            200: 셀러 정보

        Authors:
            고지원

        History:
            2020-09-21 (고지원): 초기 생성
        """
        row = session.execute(("""
            SELECT 
                seller_id, 
                korean_name,
                site_url
            FROM seller_info s_info
            INNER JOIN sellers s
            WHERE s_info.seller_id = :seller_id
        """), {'seller_id' : seller_id}).fetchone()
        return row

    def get_sellers(self, q, session):
        row = session.execute(("""
            SELECT
                COUNT(*) AS count,
                s.id, 
                s_info.korean_name, 
                s_info.image_url
                s.info.site_url
            FROM seller_info AS s_info
            INNER JOIN sellers AS s
            WHERE s_info.korean_name LIKE :name 
            AND s.is_deleted = 0
            LIMIT 1
        """), {'name' : q}).fetchall()
        return row

    def get_products(self, filter_dict, session):
        """ 상품 리스트 표출
        쿼리 파라미터에 따른 필터링된 상품 리스트를 전달한다.

        args:
            filter_dict: 필터링을 위한 딕셔너리
            session: 데이터베이스 session 객체

        returns :
            200: 필터링된 상품 리스트

        Authors:
            고지원

        History:
            2020-09-21 (고지원): 초기 생성
            2020-09-23 (고지원): 가장 최근 이력 데이터만 나오도록 수정
            
        filter_query = """
            SELECT 
                p.id, 
                p_info.main_img, 
                p_info.name, 
                p_info.price, 
                p_info.sales_amount, 
                p_info.discount_rate, 
                p_info.discount_price, 
                p_info.seller_id,
                s_info.korean_name
            FROM products AS p
            INNER JOIN product_info AS p_info ON p.id = p_info.product_id
            INNER JOIN sellers AS s ON p_info.seller_id = s.id
            INNER JOIN seller_info AS s_info ON s_info.seller_id = s.id
            WHERE (p_info.product_id, p_info.created_at) IN (SELECT p_info.product_id, MAX(p_info.created_at) FROM product_info AS p_info GROUP BY p_info.product_id) 
            AND p.is_deleted = 0 
            AND p_info.is_displayed = 1
        """

        # first 카테고리
        if filter_dict.get('first_category_id', None):
            filter_query += " AND first_category_id = :first_category_id"

        # second 카테고리
        if filter_dict.get('second_category_id', None):
            filter_query += " AND second_category_id = :second_category_id"

        # 세일
        if filter_dict.get('is_promotion', None):
            filter_query += " AND p_info.is_promotion = :is_promotion"

        # 판매량, 최신순
        if filter_dict.get('select', None):
            filter_query += " ORDER BY p.created_at DESC"
        else:
            filter_query += " ORDER BY p_info.sales_amount DESC"

        # 페이징 시작
        if filter_dict.get('offset', None):
            filter_query += " OFFSET :offset"

        # 페이징 마지막
        if filter_dict.get('limit', None):
            filter_query += " LIMIT :limit"

        row = session.execute(text(filter_query), filter_dict)

        return row

    def get_product(self, product_id, session):
        """ 상품 상세 데이터 전달

        args:
            product_id: 해당하는 상품의 아이디
            session: 데이터베이스 session 객체

        returns :
            200: 상품 상세 정보

        Authors:
            고지원

        History:
            2020-09-23 (고지원): 초기 생성
        """
        product_info = session.execute(("""
            SELECT 
                p.id AS p_id, 
                p_info.id AS p_info_id, 
                p_info.name, 
                p_info.price, 
                p_info.sales_amount, 
                p_info.discount_rate, 
                p_info.discount_price,
                p_info.seller_id
            FROM products AS p 
            INNER JOIN product_info AS p_info
            WHERE p_info.product_id = :product_id
            ORDER BY p_info.created_at DESC 
            LIMIT 1
        """), {'product_id' : product_id}).fetchone()

        # 컬러
        colors = session.execute(("""
            SELECT 
                id, 
                color_name
            FROM colors 
            WHERE product_info_id = :product_info_id
        """), {'product_info_id' : product_info.p_info_id})

        # 사이즈
        sizes = session.execute(("""
            SELECT 
                id, 
                size_name
            FROM sizes
            WHERE product_info_id = :product_info_id
        """), {'product_info_id' : product_info.p_info_id})

        # 이미지
        images = session.execute(("""
            SELECT 
                id, 
                URL
            FROM product_images
            WHERE product_info_id = :product_info_id
            ORDER BY ordering 
        """), {'product_info_id' : product_info.p_info_id})

        product_info = dict(product_info)

        color_list = [{
            "id": color.id, "color": color.color_name
        } for color in colors]
        product_info['colors'] = color_list

        size_list = [{
            "id": size.id, "size": size.size_name
        } for size in sizes]
        product_info['sizes'] = size_list

        image_list = [{
            "id": image.id, "image_url": image.URL
        } for image in images]
        product_info['images'] = image_list

        return product_info