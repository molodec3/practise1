import pytest

from main import process_reg_exp


def test_basic():
    assert process_reg_exp(reg_exp='ab+c.aba.*.bac.+.+*', letter='a') == 2  # ((a + b)c + a(ba)*(b + ac))*
    assert process_reg_exp(reg_exp='acb..bab.c.*.ab.ba.+.+*a.', letter='c') == 0  # (acb + b(abc)*(ab + ba))*a


def test_inf_letter_count():
    assert process_reg_exp(reg_exp='a*', letter='a') == float('inf')  # a*


def test_error_for_one_arg():
    assert process_reg_exp(reg_exp='*', letter='a') == 'ERROR'


def test_error_for_two_args():
    assert process_reg_exp(reg_exp='a+', letter='a') == 'ERROR'


def test_final_error():
    assert process_reg_exp(reg_exp='ab+bc+', letter='a') == 'ERROR'


def test_with_epsilon():
    assert process_reg_exp(reg_exp='a1b+.a.', letter='a') == 2  # a(1 + b)


def test_extra():
    assert process_reg_exp(reg_exp='aab.*.a.a.a.', letter='a') == 4  # a(ab)*aaa
    assert process_reg_exp(reg_exp='aaab..a+.b.b.b.', letter='a') == 3  # a(aab + a)bbbb


def test_with_one_letter():
    assert process_reg_exp(reg_exp='aa.a+', letter='a') == 2  # aa + a
    assert process_reg_exp(reg_exp='aa.a+*', letter='a') == float('inf')  # (aa + a)*
