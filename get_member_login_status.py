def get_member_login_status():
    """ 获取会员登录状态 """
    member_token = request.values.get('m_token', None)
    if member_token:
        member = rs.get('logonmember_' + member_token)
        if member:
            rs.delete('logonmember_' + member_token)
            member = json.loads(member)
            session['member'] = member
        else:
            return None
    else:
        member = session.get('member', None)

    return member