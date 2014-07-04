# coding=utf-8
from django import template
import re
import arrow
register = template.Library()

def cutTitle(value, args):
    """中英文截取"""
    sub_fix = '...'
    real_len = 0
    args = str(args)
    bits = args.split(' ')

    if len(bits) == 2:
        if bits[1] == '' or bits[1] == 'none':
            sub_fix = ''
        else:
            sub_fix = '...'
    cut_len = int(bits[0])
    ret_val = ""
    for s in value:
        if real_len >= cut_len:
            ret_val = ret_val+sub_fix
            break
        if not re.match("^[\u4E00-\u9FA5]+$", s):
            if real_len + 2 <= cut_len:
                ret_val += s
                real_len += 2
        else:
            if real_len + 1 <= cut_len:
                ret_val += s
                real_len += 1
    return ret_val


def tranArrowDate(value):
    """转换几天前，几小时前，几月前等格式"""
    u = arrow.get(value)
    return u.humanize(locale='zh_CN')


register.filter('cut_title', cutTitle)
register.filter('fun', tranArrowDate)
