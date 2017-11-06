@api.route('/login/get_member_info', methods = ['POST'])
@views_utils.internal_api
def get_member_info(**args):
    """ 获取会员信息 """
    mn = request.form.get('member_name', None)

    if not mn:
        return json.dumps({'status': -1, 'msg': '非法请求'})

    member = m_models.Member \
                     .query \
                     .with_entities(
                         m_models.Member.member_name,
                         m_models.Member.password,
                         m_models.Member.member_pay_flag
                     ) \
                     .filter(
                         m_models.Member.member_name == mn
                     ) \
                     .first()

    if not member:
        return json.dumps({'status': -2, 'msg': u'用户名不存在！'})

    return json.dumps(
        {'status': 0, 'member_name': member.member_name,
         'password': member.password,
         'pay_times': member.member_pay_flag}
    )
