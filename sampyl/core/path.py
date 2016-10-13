# -*- coding: utf-8 -*-
"""sampyl.core.element

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

from sampyl.core.element import Element
from lxml.cssselect import CSSSelector, SelectorError
from selenium.webdriver.common.by import By

__all__ = ['join', 'normalize']


def normalize(by, path, *args, **kwargs):
    """Convert all paths into a xpath selector

    :param str by: Selenium selector
    :param str path: Selector value
    :param args:
    :param kwargs:
    :return:
    """

    if args or kwargs:
        pass

    if by == 'class name':
        return By.XPATH, '/descendant-or-self::[contains(@class, "%s")]' % str(path)

    elif by == 'css selector':

        try:
            return By.XPATH, '/%s' % CSSSelector(str(path)).path

        except SelectorError:
            pass

    elif by == 'element':
        if isinstance(path, Element):
            return path.search_term

    elif by == 'id':
        return By.XPATH, '/descendant-or-self::[@id="%s"]' % str(path)

    elif by == 'link text':
        return By.XPATH, '/descendant-or-self::*[contains("input a button", name()) ' \
                         'and normalize-space(text()) = "%s"]' % str(path)

    elif by == 'name':
        return By.XPATH, '/descendant-or-self::*[@name="%s"]' % str(path)

    elif by == 'partial link text':
        return By.XPATH, '/descendant-or-self::*[contains("input a button", name()) ' \
                         'and contains(normalize-space(text()), "%s")]' % str(path)

    elif by == 'tag name':
        return By.XPATH, '/descendant-or-self::%s' % str(path)

    elif by == 'xpath':
        return by, path

    # All other cases return an empty statement
    return By.XPATH, ''


def join(*args):
    """Join 'x' locator paths into a single path

    :param args: Locator path tuples (by, path)
    :return: Locator path
    :rtype: str
    """

    return By.XPATH, ''.join([normalize(*item)[1] for item in args if isinstance(item, (list, tuple))])
