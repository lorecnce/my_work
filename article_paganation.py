# coding: utf-8
import json
import decimal
from apps.website.models import member as m_models, product, order as o_models
from flask import request, jsonify, session, redirect
import flask_sqlalchemy

from apps import app, rs, db
from apps.api import api, front
from apps.admin.models import feedback
from apps.utils import common_utils, views_utils, result_helper, member_utils, \
    pagination_utils, assignment_helper, order_utils
from apps.website.models import member as m_models, card, product, activity as a_models
from apps.official_web.forms import member_center as m_forms

MEMBER_REF_STATUS_RECEIVABLE = 20
MEMBER_REF_STATUS_RECEIVED = 30
MEMBER_PER_PAGE = 5
from flask import render_template, redirect, request, abort
from apps import app, rs, cache
from apps.official_web import official_web
from apps.website.models import content
import os
from flask import jsonify
from apps.utils import views_utils
from flask import Markup


@api.route('/notice_detail/', defaults={'to': '1'})
@api.route('/notice_detail/<to>')
# @cache.cached(timeout=0, key_prefix='%s')
def notice(**args):
    """ 获取文章 """
    page = request.args.get('pages', 1)
    try:
        fn = os.path.join(app.static_folder, 'ue_upload', 'article',
                          args['to'] + '.art')
        with open(fn, 'rb') as fp:
            tt = ''.join(list(fp.readlines()))  # 用生成器优化内存效率

        if 'keywords' in tt:
            total_page = len(tt.split('keywords'))  # 总页数

            if page > total_page or page < 0:
                return jsonify({'status': -1, 'msg': 'page不为负,或则超出总页啦!'})

            tt = tt.split('keywords')[page - 1]

            if page == 1:
                has_prev = 0
                has_next = 1
            elif page == total_page:
                has_next = 0
                has_prev = 1
            else:
                has_prev = 1
                has_next = 1
        else:
            has_prev = 0
            has_next = 0
            total_page = 1

        at = content.Article.query \
            .filter(
            content.Article.article_id == args['to']
        ) \
            .first()

        map_type = content.ContentType.get_ordered_dict_choice(10, 3)
        atype = map_type.get(str(at.article_type), '全部资讯')
        # 找上一篇和下一篇
        prev_a = content.Article \
            .query \
            .filter(
            content.Article.article_id == at.find_prev_id()
        ) \
            .first()
        next_a = content.Article \
            .query \
            .filter(
            content.Article.article_id == at.find_next_id()
        ) \
            .first()

        # return render_template(
        #     '/official_web/notice_detail.html',
        #     article_id=args['to'], content=Markup(tt),
        #     arttypeval=atype, arttypekey=str(at.article_type),
        #     at=at, prev_a=prev_a, next_a=next_a,
        #     map_type=map_type,
        #     have_prev=has_prev,  # 返回1 或则0
        #     have_next=has_next,  # 返回1 或则0
        #     page=page,  # 页码
        #     total_page=total_page  # 总页

        return jsonify(json.loads(json.dumps({'article_id': args['to'], 'content': Markup(tt), \
                                              'arttypeval': atype, 'arttypekey': str(at.article_type), \
                                              'at': at, 'prev_a': prev_a, 'next_a': next_a, \
                                              'map_type': map_type, \
                                              'has_prev': has_prev, \
                                              'has_next': has_next, \
                                              'total_page': total_page}, cls=common_utils.serializable_them,
                                             ensure_ascii=True)))
    except:
        abort(404)

