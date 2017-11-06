@official_web.route('notice_detail/', defaults = {'to': '1'})
@official_web.route('notice_detail/<to>')
@cache.cached(timeout = 300, key_prefix='%s')
def notice(**args):
    """ 获取文章 """
    try:
        fn = os.path.join(app.static_folder, 'ue_upload', 'article',
                          args['to'] + '.art')
        with open(fn, 'rb') as fp:
            tt = ''.join(list(fp.readlines())) #用生成器优化内存效率
        at = content.Article.query \
                            .filter(
                                content.Article.article_id == args['to']
                            ) \
                            .first()

        map_type = content.ContentType.get_ordered_dict_choice(10,3)
        atype = map_type.get(str(at.article_type),'全部资讯')
        #找上一篇和下一篇
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

        return render_template(
            '/official_web/notice_detail.html',
            article_id = args['to'], content = Markup(tt),
            arttypeval = atype, arttypekey = str(at.article_type),
            at = at, prev_a = prev_a, next_a = next_a,
            map_type = map_type
        )
    except:
        abort(404)
