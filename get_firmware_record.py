@api.route('/lianjibao/')
def get_firmware_record(**args):
    """ 获取联机宝固件信息 """
    q = f_models.Firmware.query

    ft = request.args.get('firmware_type', None)
    q = filter_helper.choice_helper(f_models.Firmware.firmware_type, q, ft)

    q = q.order_by(f_models.Firmware.add_time.desc())

    data = q.first()

    if not data:
        return json.dumps({'status': -1, 'msg': '没有固件记录！'});

    data = dict(common_utils.orm_to_dict(data, ['add_time']), status = 0)

    return json.dumps(data)