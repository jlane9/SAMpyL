# -*- coding: utf-8 -*-
"""sampyl.app

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

# pylint: disable=line-too-long
import keyword
import re
import warnings
from urlparse import urlparse
from sampyl.core.element import SeleniumObject
from sampyl.core.structures import TYPES as T
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException


__all__ = ['App', 'Node']

RESERVED = ('nodeName', 'nodeType', 'this')
DEFAULT_TYPE = 'text'


def is_legal_variable_name(name):
    """Determines whether the name attribute value is a valid variable name

    :param str name: Name attribute
    :return:
    """

    if isinstance(name, basestring):
        if not keyword.iskeyword(name):
            return bool(re.compile(r'^[a-zA-Z_][\w]*$').search(name))

    return False


def force_legal_variable_name(name):
    """Forces name attribute into a valid variable name

    :param str name: Name attribute
    :return:
    """

    if not is_legal_variable_name(name):

        if isinstance(name, basestring):

            re_keyword = '|'.join(['(^{}$)'.format(item) for item in keyword.kwlist])

            keyword_safe = re.sub('({})'.format(re_keyword), '_\g<1>', name)

            return re.sub('^\d|[^\w]', '_', keyword_safe)

        return '_'

    return name


class App(SeleniumObject):
    """The App implementation

    .. TODO:: Add the ability define which types are available
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

    def get(self, url):
        """Instruct Selenium to navigate to the following url

        :param str url: web url
        :return:
        """

        if isinstance(url, basestring):
            return self.driver.get(url)

        raise TypeError('Incorrect type for \'url\', url must be of type \'str\'')

    def navigate_to(self, path):
        """Instructs Selenium to navigate to a different path under the hostname

        :param str path: Path from hostname
        :return:
        """

        if isinstance(path, basestring):

            full_url = urlparse(path).path
            url_path = '/%s' % full_url if not full_url.startswith('/') else full_url

            if isinstance(path, basestring):

                scheme = self.scheme if self.scheme != '' else 'http'

                if self.hostname != '':
                    return self.get('%s://%s%s' % (scheme, self.hostname, url_path))

                raise NotImplementedError('Action cannot be completed because hostname is not set')

        raise TypeError('Incorrect type for \'path\', path must be of type \'str\'')

    def update(self, name_attr='data-qa-id', type_attr='data-qa-model'):
        """

        :param str name_attr:
        :param str type_attr:
        :return:
        """

        if isinstance(name_attr, basestring) and isinstance(type_attr, basestring):

            identifiers = [e.get_attribute(name_attr) for e in
                           self.driver.find_elements(By.XPATH, '/descendant-or-self::*[@{0}]'.format(name_attr))]

            duplicates = set([_id for _id in identifiers if identifiers.count(_id) > 1])

            if len(duplicates) > 0:

                msg = ' '.join(['UniquenessWarning: There appears to be multiple elements with the'
                                ' same identifier. Please review the following element(s):',
                                ', '.join(duplicates)])

                warnings.warn(msg)

            self.page = Node(self.driver, name_attr=name_attr, type_attr=type_attr)
            self.page.add_children(*set(identifiers))

    def wait_until_present(self, path, _by=None, timeout=30):
        """Wait until element with id is present

        :param str _by:
        :param str path:
        :param int timeout: Wait timeout in seconds
        :return:
        """

        if not _by and isinstance(path, basestring):
            _by = 'xpath'
            path = '/descendant-or-self::*[contains(@{0}, "{1}")]'.format(self._name_attr, path)

        return super(App, self).wait_until_present(_by, path, timeout=timeout)

    def wait_until_appears(self, path, _by=None, timeout=30):
        """Wait until the element appears

        :param str _by:
        :param str path:
        :param int timeout: Wait timeout in seconds
        :return: True, if the wait does not timeout
        :rtype: bool
        """

        if not _by and isinstance(path, basestring):
            _by = 'xpath'
            path = '/descendant-or-self::*[contains(@{0}, "{1}")]'.format(self._name_attr, path)

        return super(App, self).wait_until_appears(_by, path, timeout=timeout)

    def wait_until_disappears(self, path, _by=None, timeout=30):
        """Wait until the element disappears

        :param str _by:
        :param str path:
        :param int timeout: Wait timeout in seconds
        :return: True, if the wait does not timeout
        :rtype: bool
        """

        if not _by and isinstance(path, basestring):
            _by = 'xpath'
            path = '/descendant-or-self::*[contains(@{0}, "{1}")]'.format(self._name_attr, path)

        return super(App, self).wait_until_disappears(_by, path, timeout=timeout)


class Node(SeleniumObject):
    """The SAMpyL Node implementation
    """

    __PATH = '/descendant-or-self::*[@{0}="{1}"]'
    DELIMITER = '.'

    def __init__(self, web_driver, identifier=None, root=None, **kwargs):

        super(Node, self).__init__(web_driver, **kwargs)
        self._children = {}

        # Sanitize arguments
        identifier = identifier if isinstance(identifier, basestring) else ''
        root = root if isinstance(root, basestring) else ''

        # Get the first attribute from the identifier
        cur = identifier.split(self.DELIMITER, 1)

        # Assign identifier
        if cur[0] != '':

            if root != '':
                self._identifier = self.DELIMITER.join((root, cur[0]))

            else:
                self._identifier = cur[0]

        else:
            self._identifier = ''

        # The identifier has "leftover" attributes, recursively create child nodes
        if len(cur) > 1:

            child = cur[1].split(self.DELIMITER, 1)[0]

            if child != '':
                self.__setitem__(child, Node(web_driver=web_driver,
                                             identifier=cur[1], root=self._identifier))

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
                        """

                        :param args:
                        :param kwargs:
                        :return:
                        """

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
                setattr(self, force_legal_variable_name(key), value)
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

        cur = child.split(self.DELIMITER, 1)

        if cur[0] != '':

            # If this Node has not been created
            if cur[0] not in self.keys():

                self.__setitem__(cur[0], Node(web_driver=self.driver,
                                              identifier=child, root=self._identifier))

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

        try:
            element = self.driver.find_element_by_xpath(self.xpath())

        except NoSuchElementException:
            element = None

        _type = element.get_attribute(self._type_attr) if element else None

        if _type:
            return _type.lower()

        else:
            return DEFAULT_TYPE

    def json(self):
        """Return json representation of Node and it's nested children

        :return: JSON
        :rtype: dict
        """

        json = {'nodeName': self._identifier, 'nodeType': self.type()} \
            if self._identifier != '' else {}

        for child in self.keys():
            json[child] = self.__getitem__(child).json()

        return json

    def wait_until_present(self, _by=None, path=None, timeout=30):
        """Wait until the element is available to the DOM

        :param str _by: Selector method
        :param str path: Selector path
        :param timeout: Wait timeout in seconds
        :return:
        """

        if _by and path:
            self._wait_until(ec.presence_of_element_located, _by, path, timeout)

        else:
            return self._wait_until(ec.presence_of_element_located, 'xpath', self.xpath(), timeout)

    def wait_until_appears(self, _by=None, path=None, timeout=30):
        """Wait until the element appears

        :param str _by: Selector method
        :param str path: Selector path
        :param int timeout: Wait timeout in seconds
        :return: True, if the wait does not timeout
        :rtype: bool
        """

        if _by and path:
            return self._wait_until(ec.visibility_of_element_located, _by, path, timeout)

        else:
            return self._wait_until(ec.visibility_of_element_located, 'xpath', self.xpath(), timeout)

    def wait_until_disappears(self, _by=None, path=None, timeout=30):
        """Wait until the element disappears

        :param str _by: Selector method
        :param str path: Selector path
        :param int timeout: Wait timeout in seconds
        :return: True, if the wait does not timeout
        :rtype: bool
        """
        if _by and path:
            return self._wait_until(ec.invisibility_of_element_located, _by, path, timeout)

        else:
            return self._wait_until(ec.invisibility_of_element_located, 'xpath', self.xpath(), timeout)
