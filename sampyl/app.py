# -*- coding: utf-8 -*-
"""sampyl.app

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

from sampyl.core.element import SeleniumObject
# from sampyl.core.inspection import save_inspection
from sampyl.core.structures import TYPES as T
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from urlparse import urlparse
import keyword
import re
import warnings

__all__ = ['App', 'Node']

RESERVED = ('nodeName', 'nodeType', 'this')
DEFAULT_TYPE = 'text'


def is_legal_variable_name(name):

    if isinstance(name, basestring):
        if not keyword.iskeyword(name):
            return bool(re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$').search(name))

    return False


def force_legal_variable_name(name):

    if isinstance(name, basestring):

        re_keyword = '|'.join(['(^{}$)'.format(item) for item in keyword.kwlist])

        return re.sub('|'.join(['(^[0-9]?[^a-zA-Z_])', re_keyword]), '_', name)

    return '_'


class App(SeleniumObject):
    """The App implementation
    """

    scheme = ""
    hostname = ""

    def __init__(self, web_driver, url=None):

        super(App, self).__init__(web_driver)

        full_url = url if isinstance(url, basestring) else ''
        path = urlparse(full_url)
        self.page = Node(web_driver)

        if path.netloc != '':

            self.scheme = path.scheme if path.scheme != '' else 'http'
            self.hostname = path.netloc

            if self.hostname != '':
                self.get('%s://%s' % (self.scheme, self.hostname))

    @staticmethod
    def save_inspection(self, filename, name_attr='data-qa-id'):

        return

        # assert isinstance(filename, basestring)

        # with open(filename, 'w') as f:
        #    f.write(save_inspection(self.driver, self.driver.get_screenshot_as_base64(), self.update(), name_attr))

    def get(self, url):
        """Instruct Selenium to navigate to the following url

        :param str url: web url
        :return:
        """

        if isinstance(url, basestring):
            return self.driver.get(url)

        raise TypeError('Incorrect type for \'url\', url must be of type \'str\'')

    def navigate_to(self, path):
        """

        :param str path:
        :return:
        """

        if isinstance(path, basestring):

            full_url = urlparse(path).path
            url_path = '/%s' % full_url if not full_url.startswith('/') else full_url

            if isinstance(path, basestring):

                scheme = self.scheme if self.scheme != '' else 'http'

                if self.hostname != '':
                    return self.get('%s://%s%s' % (scheme, self.hostname, url_path))

                raise NotImplementedError('This action cannot be completed because hostname is not set')

        raise TypeError('Incorrect type for \'path\', path must be of type \'str\'')

    def update(self, name_attr='data-qa-id', type_attr='data-qa-model'):

        if isinstance(name_attr, basestring) and isinstance(type_attr, basestring):

            identifiers = [e.get_attribute(name_attr)
                           for e in self.driver.find_elements(By.XPATH, '/descendant-or-self::*[@%s]' % name_attr)]

            duplicates = set([_id for _id in identifiers if identifiers.count(_id) > 1])

            if len(duplicates) > 0:

                msg = ' '.join(['UniquenessWarning: There appears to be multiple elements with the same identifier. '
                                'Please review the following element(s):', ', '.join(duplicates)])
                warnings.warn(msg)

            self.page = Node(self.driver, name_attr=name_attr, type_attr=type_attr)
            self.page.add_children(*set(identifiers))

    def wait_until_present(self, _id, timeout=30):
        """Wait until element with id is present

        :param str _id: Element id to wait for
        :param int timeout: Wait timeout in seconds
        :return:
        """

        search = '/descendant-or-self::*[contains(@data-qa-id, "{0}")]'

        wait = WebDriverWait(self.driver, timeout) if isinstance(timeout, int) else WebDriverWait(self.driver, 30)

        try:

            wait.until(ec.presence_of_element_located((By.XPATH, search.format(str(_id)))))
            return True

        except TimeoutException:
            pass

        return False

    def wait_until_appears(self, _id, timeout=30):
        """Wait until the element appears

        :param str _id: Element id to wait for
        :param int timeout: Wait timeout in seconds
        :return: True, if the wait does not timeout
        :rtype: bool
        """

        search = '/descendant-or-self::*[contains(@data-qa-id, "{0}")]'

        wait = WebDriverWait(self.driver, timeout) if isinstance(timeout, int) else WebDriverWait(self.driver, 30)

        try:

            wait.until(ec.visibility_of_element_located((By.XPATH, search.format(str(_id)))))
            return True

        except TimeoutException:
            pass

        return False

    def wait_until_disappears(self, _id, timeout=30):
        """Wait until the element disappears

        :param str _id: Element id to wait for
        :param int timeout: Wait timeout in seconds
        :return: True, if the wait does not timeout
        :rtype: bool
        """

        search = '/descendant-or-self::*[contains(@data-qa-id, "{0}")]'

        wait = WebDriverWait(self.driver, timeout) if isinstance(timeout, int) else WebDriverWait(self.driver, 30)

        try:

            wait.until(ec.invisibility_of_element_located((By.XPATH, search.format(str(_id)))))
            return True

        except TimeoutException:
            pass

        return False


class Node(SeleniumObject):
    """The SAMpyL Node implementation
    """

    __PATH = '/descendant-or-self::*[@{0}="{1}"]'

    def __init__(self, web_driver, identifier=None, root=None, **kwargs):

        super(Node, self).__init__(web_driver, **kwargs)
        self._children = {}

        # Sanitize arguments
        identifier = identifier if isinstance(identifier, basestring) else ''
        root = root if isinstance(root, basestring) else ''

        # Get the first attribute from the identifier
        cur = identifier.split('.', 1)

        # Assign identifier
        if cur[0] != '':

            if root != '':
                self._identifier = '.'.join((root, cur[0]))

            else:
                self._identifier = cur[0]

        else:
            self._identifier = ''

        # The identifier has "leftover" attributes, recursively create child nodes
        if len(cur) > 1:

            child = cur[1].split('.', 1)[0]

            if child != '':
                self.__setitem__(child, Node(web_driver=web_driver, identifier=cur[1], root=self._identifier))

    def __getattr__(self, item):

        if item in self.keys():
            return self.__getitem__(item)

        else:

            element = self.this

            if hasattr(element, item):

                attr = element.__getattribute__(item)

                # SDA method
                if hasattr(attr, '__call__'):

                    def indirect_call_to_this(*args, **kwargs):

                        return attr(*args, **kwargs)

                    return indirect_call_to_this

                # SDA property
                else:
                    return attr

            else:
                raise AttributeError('%s' % str(item))

    def __getitem__(self, item):

        if isinstance(item, (basestring, int)):

            if str(item) in self.keys():

                return self._children[str(item)]

            raise KeyError('%s' % str(item))

        raise TypeError("%s is not valid, use <type 'str'>" % type(item))

    def __setitem__(self, key, value):

        if key not in RESERVED:

            if isinstance(value, Node):

                self._children[str(key)] = value
                return

            raise TypeError("value %s is not valid, use value <type 'Node'>" % type(value))

        raise KeyError('%s is a reserved keyword' % str(key))

    def keys(self):
        """Returns a list of this node's children

        :return: List of Node's children
        :rtype: list
        """

        return self._children.keys()

    def add_child(self, child):
        """Create child node from this node

        :param str child: Child element identifier
        :return:
        """

        child = child if isinstance(child, basestring) else ''

        cur = child.split('.', 1)

        if cur[0] != '':

            # If this Node has not been created
            if cur[0] not in self.keys():

                self.__setitem__(cur[0], Node(web_driver=self.driver, identifier=child, root=self._identifier))

            # If the Node already exists
            elif len(cur) > 1:

                try:
                    self._children[cur[0]].add_child(cur[1])

                except KeyError:
                    raise KeyError('Id %s contains a reserved word.' % child)

    def add_children(self, *args):
        """Creates child nodes from this node

        :param str args: Child elements' identifiers
        :return:
        """

        for arg in args:
            self.add_child(arg)

    @property
    def element(self):
        """Returns the Selenium WebElement for this nodes

        :return: Selenium WebElement
        """

        if self._identifier != '':

            elements = self.driver.find_elements(By.XPATH, self.xpath())

            if len(elements) > 0:
                return elements[0]

    @property
    def this(self):
        """Returns the sda structure for this node

        :return: SDA structure
        """

        if self._identifier != '':
            return T.get(self.type(), T[DEFAULT_TYPE])(self.driver, by=By.XPATH, path=self.xpath())

    def xpath(self):
        """Returns the XPATH selector for this node

        :return: XPATH selector
        :rtype: str
        """

        if self._identifier != '':
            return self.__PATH.format(self._name_attr, self._identifier)

        return ''

    def type(self):
        """Return a node's type

        :return: Node type
        :rtype: str
        """

        _type = self.element.get_attribute(self._type_attr) if self.element is not None else 'div'

        return _type.lower() if _type is not None else DEFAULT_TYPE

    def json(self):
        """Return json representation of Node and it's nested children

        :return: JSON
        :rtype: dict
        """

        json = {'nodeName': self._identifier, 'nodeType': self.type()} if self._identifier != '' else {}

        for child in self.keys():
            json[child] = self.__getitem__(child).json()

        return json
