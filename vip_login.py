@official_web.route('login/member_login', methods = ["GET", "POST"])
def member_login():
    """ 会员登录 """
    member = views_utils.get_member_login_status()
    if member:
        return views_utils.operate_success({
            'link': '/member',
            'msg': '您已登录，即将跳转到会员中心',
            'timeout': 3
        })

    form = m_forms.LoginForm(request.form)
    if request.method == "POST":
       if not form.validate():
           return views_utils.operate_success({
               'link': '/login/member_login',
               'msg': '请正确输入用户名和密码！',
               'timeout': 3
           })

       if rs.sismember('register_member', form.member_name.data):
           mnm = member_utils.gene_member_name_md5(form.member_name.data)
           mem_key = rs.keys('register_member:' + mnm + '*')
           if mem_key:
               mem_dict = json.loads(rs.get(mem_key[0]))
           else:
               return views_utils.operate_success({
                   'link': '/register/email_register',
                   'msg': '数据同步出错，请重新注册！',
                   'timeout': 3
               })

           session['register'] = {
               'email': mem_dict['email']
           }

           return views_utils.operate_success({
               'link': '/register/email_register_validate',
               'msg': '您尚未绑定邮箱，请去邮箱中绑定',
               'timeout': 3
           })

       is_client = request.form.get('is_client', None)
       mn = form.member_name.data.strip()
       member = m_models.Member.query \
                               .filter(or_(
                                   m_models.Member.member_name == mn,
                                   m_models.Member.email == mn
                                   # m_models.Member.mobile == mn
                               )) \
                               .first()
       if not member:
           return views_utils.operate_success({
               'link': '/login/member_login',
               'msg': '会员不存在，请重试',
               'timeout': 3
           })

       if len(member.password) == 20:
           pwd = m_models.Member.get_member_password(form.password.data)
       else:
           # get compact password
           pwd = m_models.Member.get_member_password(form.password.data,
                                                     True)

       if pwd == member.password:
           # request from web, record session
           mem = common_utils.orm_to_dict(member)

           if not is_client:
               session['member'] = mem

               return views_utils.operate_success({
                   'link': '/member',
                   'msg': '登录成功,即将进入会员中心',
                   'timeout': 3
               })

           # request from client return token string
           else:
               sid = str(uuid4()).replace('-', '')[5:15] + \
                     member.member_id[10:32]
               rs.set('logonmember_' + sid,
                      json.dumps(mem),
                      ex = app.config['LOGOUT_WITHOUT_OPERATE'])

               return json.dumps({'status': 0, 'token': sid})
       else:
           return views_utils.operate_success({
               'link': '/login/member_login',
               'msg': '密码错误！请重试！',
               'timeout': 3
           })

    abort(404)