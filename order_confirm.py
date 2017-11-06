# coding: utf-8
@api.route('/member/order_confirm', methods = ['GET','POST'])
@views_utils.member_utils
def order_confirm(**args):
    """ 订单收货确认 """
    oid = request.form.get('order_id')
    if not oid:
        return jsonify({"status":-1,"msg":"没有找到该订单号!"})

    order = o_models.Order.query.get(oid)
    if order.member_id != args['member']['member_id']:
       order.order_status != o_models.OrderStatus.ORDER_WAIT_RECV:

       return jsonify({"status":-2,"msg":"没有对应的会员名,或则没有等待确认的订单,所以查找失败!"})

    order_utils.order_complete(order, 2)
    db.session.commit()
    member_utils.update_member(args['member']['member_id']),

    return jsonify({"status":0,"msg":"恭喜你，订单已完成！即将转到订单列表！"})



有3种可能
1：jsonify{"status":-1,"msg":"没有找到该订单号!"}
2：jsonify{"status":-2,"msg":"没有对应的会员名,或则没有等待确认的订单,所以查找失败!"}
3：jsonify{"status":0,"msg":"恭喜你，订单已完成！即将转到订单列表！"}
