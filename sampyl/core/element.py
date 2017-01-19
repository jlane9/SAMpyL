# -*- coding: utf-8 -*-
"""sampyl.core.element

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

# pylint: disable=line-too-long
import keyword
from lxml.cssselect import CSSSelector, SelectorError
from sampyl.core.shortcuts import encode_ascii
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, TimeoutException

__all__ = ['Element']


def normalize(_by, path, *args, **kwargs):
    """Convert all paths into a xpath selector

    :param str _by: Selenium selector
    :param str path: Selector value
    :param args:
    :param kwargs:
    :return:
    """

    if args or kwargs:
        pass

    normalizers = dict([('class name', lambda x: '/descendant-or-self::*[contains(@class, "%s")]' % x),
                        ('id', lambda x: '/descendant-or-self::*[@id="%s"]' % x),
                        ('link text', lambda x: '/descendant-or-self::*[contains("input a button", name()) '
                                                'and normalize-space(text()) = "%s"]' % x),
                        ('name', lambda x: '/descendant-or-self::*[@name="%s"]' % x),
                        ('partial link text', lambda x: '/descendant-or-self::*[contains("input a button", name()) '
                                                        'and contains(normalize-space(text()), "%s")]' % x),
                        ('tag name', lambda x: '/descendant-or-self::%s' % x),
                        ('xpath', lambda x: x)])

    if _by == 'css selector':

        try:
            return By.XPATH, '/%s' % CSSSelector(str(path)).path

        except SelectorError:
            return By.XPATH, ''

    elif _by == 'element':
        if isinstance(path, Element):
            return path.search_term

    else:
        return By.XPATH, normalizers.get(_by, lambda x: '')(str(path))


def join(*args):
    """Join 'x' locator paths into a single path

    :param args: Locator path tuples (by, path)
    :return: Locator path
    :rtype: str
    """

    return By.XPATH, ''.join([normalize(*item)[1] for item in args if isinstance(item, (list, tuple))])


class SeleniumObject(object):
    """The SeleniumObject implementation
    """

    def __init__(self, web_driver, **kwargs):

        self.driver = web_driver if isinstance(web_driver, WebDriver) else None

        if not self.driver:
            raise TypeError("'web_driver' MUST be a selenium WebDriver element")

        if 'name_attr' in kwargs.keys():
            self._name_attr = kwargs['name_attr'] if isinstance(kwargs['name_attr'], basestring) else 'data-qa-id'

        else:
            self._name_attr = 'data-qa-id'

        if 'type_attr' in kwargs.keys():
            self._name_attr = kwargs['type_attr'] if isinstance(kwargs['type_attr'], basestring) else 'data-qa-model'

        else:
            self._type_attr = 'data-qa-model'

    def _wait_until(self, expected_condition, _by, path, timeout=30):
        """Wait until expected condition is fulfilled

        :param func expected_condition: Selenium expected condition
        :param str _by: Selector method
        :param str path: Selector path
        :param timeout: Wait timeout in seconds
        :return:
        """

        wait = WebDriverWait(self.driver, timeout) if isinstance(timeout, int) else WebDriverWait(self.driver, 30)

        try:

            if _by != 'element':

                wait.until(expected_condition((_by, path)))
                return True

        except TimeoutException:
            pass

        return False

    def wait_until_present(self, _by, path, timeout=30):
        """Wait until the element is available to the DOM

        :param str _by: Selector method
        :param str path: Selector path
        :param timeout: Wait timeout in seconds
        :return:
        """

        return self._wait_until(ec.presence_of_element_located, _by, path, timeout)

    def wait_until_appears(self, _by, path, timeout=30):
        """Wait until the element appears

        :param str _by: Selector method
        :param str path: Selector path
        :param int timeout: Wait timeout in seconds
        :return: True, if the wait does not timeout
        :rtype: bool
        """

        return self._wait_until(ec.visibility_of_element_located, _by, path, timeout)

    def wait_until_disappears(self, _by, path, timeout=30):
        """Wait until the element disappears

        :param str _by: Selector method
        :param str path: Selector path
        :param int timeout: Wait timeout in seconds
        :return: True, if the wait does not timeout
        :rtype: bool
        """

        return self._wait_until(ec.invisibility_of_element_located, _by, path, timeout)

    def wait_implicitly(self, s):
        """Wait a set amount of time in seconds

        :param int s: Seconds to wait
        :return:
        """

        if isinstance(s, int):
            self.driver.implicitly_wait(s)
            return True

        return False


class Element(SeleniumObject):
    """The Element implementation

    An abstract class for interacting with web elements.

    """

    def __init__(self, web_driver, _by=By.XPATH, path=None, **kwargs):
        """Basic Selenium element

        :param WebDriver web_driver: Selenium webdriver
        :param str _by: By selector
        :param str path: selection value
        :return:
        """

        super(Element, self).__init__(web_driver, **kwargs)

        # Instantiate selector
        self.search_term = normalize(_by=_by, path=path)

        # Add any additional attributes
        for extra in kwargs:
            self.__setattr__(extra, kwargs[extra])

    def __contains__(self, attribute):
        """Returns True if element contains attribute

        :param str attribute: Element attribute
        :return: True, if the element contains that attribute
        :rtype: bool
        """

        if self.exists() and isinstance(attribute, basestring):

            try:
                self.driver.find_element(join(self.search_term, ('xpath', '/self::*[boolean(@{0})]'.format(attribute))))
                return True

            except NoSuchElementException:
                pass

        return False

    @encode_ascii()
    def __getattr__(self, attribute):
        """Returns the value of an attribute

        .. note:: class and for are both reserved keywords. Prepend/post-pend '_' to reference both.

        :param str attribute: Element attribute
        :return: Returns the string value
        :rtype: str
        """

        if self.exists():

            if keyword.iskeyword(attribute.replace('_', '')):
                attribute = attribute.replace('_', '')

            else:
                attribute = attribute.replace('_', '-')

            return self.element().get_attribute(attribute)

        return ''

    @encode_ascii()
    def __repr__(self):
        """Returns HTML representation of the element

        :return: HTML representation of the element
        :rtype: str
        """

        return self.outerHTML if self.exists() else ''

    def angular_scope(self, attribute):
        """Returns an attribute from the angular scope

        :param str attribute:
        :return:
        """

        if self.exists():

            try:

                return self.driver.execute_script('return angular.element(arguments[0]).scope().'
                                                  '{}'.format(str(attribute)), self.element())

            except (TypeError, WebDriverException):
                pass

    def blur(self):
        """Simulate moving the cursor out of focus of this element.

        :return:
        """

        return self.driver.execute_script('arguments[0].blur();', self.element()) if self.is_displayed() else None

    @encode_ascii()
    def css_property(self, prop):
        """Return the value of a CSS property for the element

        .. warning:: value_of_css_property does not work with Firefox

        :param str prop: CSS Property
        :return: Value of a CSS property
        :rtype: str
        """

        return self.element().value_of_css_property(str(prop)) if self.exists() else None

    def drag(self, x_offset=0, y_offset=0):
        """Drag element x,y pixels from its center

        :param int x_offset: Pixels to move element to
        :param int y_offset: Pixels to move element to
        :return:
        """

        if self.exists() and isinstance(x_offset, int) and isinstance(y_offset, int):

            action = ActionChains(self.driver)
            action.click_and_hold(self.element()).move_by_offset(x_offset, y_offset).release().perform()
            return True

        return False

    def element(self):
        """Return the selenium webelement object

        :return: Selenium WebElement
        :rtype: WebElement
        """

        # If the search term passed through was an element
        if self.search_term[0] == 'element' and isinstance(self.search_term[1], WebElement):
            return self.search_term[1]

        # If the search term is a valid term
        elif self.search_term[0] in ('class name', 'css selector', 'id', 'link text',
                                     'name', 'partial link text', 'tag name', 'xpath'):

            try:

                # Locate element
                element = self.driver.find_elements(*self.search_term)

            except InvalidSelectorException:
                element = []

            if len(element) > 0:
                return element[0]

        return None

    def exists(self):
        """Returns True if element can be located by selenium

        :return: Returns True, if the element can be located
        :rtype: bool
        """

        return True if self.element() else False

    def focus(self):
        """Simulate element being in focus

        :return:
        """

        return self.driver.execute_script('arguments[0].focus();', self.element()) if self.is_displayed() else None

    def is_displayed(self):
        """Return True, if the element is visible

        :return: True, if element is visible
        :rtype: bool
        """

        return self.element().is_displayed() if self.exists() else False

    def parent(self):
        """Returns the Selenium element for the current element

        :return:
        """

        xpath = join(self.search_term, ('xpath', '/parent::*'))
        return Element(self.driver, xpath[0], xpath[1])

    def scroll_to(self):
        """Scroll to the location of the element

        :return:
        """

        if self.exists():

            element = self.element()

            script = "var vHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);" \
                     "var eTop = arguments[0].getBoundingClientRect().top;" \
                     "window.scrollBy(0, eTop-(vHeight/2));"

            # Scroll to Element
            self.driver.execute_script(script, element)

    @property
    @encode_ascii()
    def tag_name(self):
        """Returns element tag name

        :return: Element tag name
        :rtype: str
        """

        return self.element().tag_name if self.exists() else ''

    def wait_until_present(self, _by=None, path=None, timeout=30):
        """Wait until the element is present

        :param str _by: Selector method
        :param str path: Selector path
        :param timeout: Wait timeout in seconds
        :return: True, if the wait does not timeout
        :rtype: bool
        """

        if _by and path:
            return super(Element, self).wait_until_present(_by, path, timeout=timeout)

        else:
            return super(Element, self).wait_until_present(self.search_term[0], self.search_term[1], timeout=timeout)

    def wait_until_appears(self, _by=None, path=None, timeout=30):
        """Wait until the element appears

        :param str _by: Selector method
        :param str path: Selector path
        :param int timeout: Wait timeout in seconds
        :return: True, if the wait does not timeout
        :rtype: bool
        """

        if _by and path:
            return super(Element, self).wait_until_appears(_by, path, timeout=timeout)

        else:
            return super(Element, self).wait_until_appears(self.search_term[0], self.search_term[1], timeout=timeout)

    def wait_until_disappears(self, _by=None, path=None, timeout=30):
        """Wait until the element disappears

        :param str _by: Selector method
        :param str path: Selector path
        :param int timeout: Wait timeout in seconds
        :return: True, if the wait does not timeout
        :rtype: bool
        """

        if _by and path:
            return super(Element, self).wait_until_disappears(_by, path, timeout=timeout)

        else:
            return super(Element, self).wait_until_disappears(self.search_term[0], self.search_term[1], timeout=timeout)
