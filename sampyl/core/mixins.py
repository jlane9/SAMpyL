# -*- coding: utf-8 -*-
"""sampyl.core.mixins

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""


from sampyl.core.shortcuts import encode_ascii
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select as SeleniumSelect
from selenium.common.exceptions import ElementNotVisibleException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

__all__ = ['ClickMixin', 'InputMixin', 'SelectMixin', 'SelectiveMixin', 'TextMixin']


class ElementMixin(object):
    """The ElementMixin Implementation

    .. note::
        This is a dummy class.
    """

    def __getattr__(self, item):
        return item

    # This function will be overridden by the base class this extends
    def blur(self):
        """Simulate moving out of focus

        :return:
        """

        if self:
            pass

    # This function will be overridden by the base class this extends
    def element(self):
        """Returns the element

        :return:
        """

        return WebElement(WebDriver(), 'html') if self.exists() else None

    # This function will be overridden by the base class this extends
    def exists(self):
        """Return True if the element exists

        :return:
        """

        if self:
            pass

    def is_disabled(self):
        """Returns True, if the element is disabled

        :return: True, if the element is disabled
        :rtype: bool
        """

        return self.__contains__('disabled')

    # This function will be overridden by the base class this extends
    def scroll_to(self):
        """Simulate scrolling to element

        :return:
        """

        if self:
            pass


class ClickMixin(ElementMixin):
    """The ClickMixin Implementation
    """

    def click(self):
        """Click element

        :return:
        """

        if self.exists():

            try:
                self.element().click()

            # If the object is not within the view try to scroll to the element
            except (ElementNotVisibleException, WebDriverException):

                # Scroll to Element
                self.scroll_to()

                try:
                    self.element().click()

                except (ElementNotVisibleException, WebDriverException):
                    pass

    def hover(self):
        """Simulate hovering over element

        :return:
        """

        return ActionChains(self.driver).move_to_element(self.element()).perform()


class InputMixin(ElementMixin):
    """The InputMixin implementation
    """

    def __str__(self):
        return self.value()

    def input(self, text, clear=True):
        """Send text to a input field

        :param str text: Text to send to the input field
        :param bool clear: True if user wants to clear the field before assigning text
        :return: True, if text is assigned
        :rtype: bool
        """

        if self.exists() and isinstance(text, basestring):

            element = self.element()

            if clear:
                element.clear()

            element.send_keys(text)

            return True

        return False

    @encode_ascii()
    def value(self):
        """Return value of input

        :return: Input value
        :rtype: str
        """

        return self.element().get_attribute('value') if self.exists() else ''


class SelectMixin(ElementMixin):
    """The SelectMixin implementation
    """

    @staticmethod
    def _to_int(value):

        if isinstance(value, int) or isinstance(value, basestring):

            if isinstance(value, basestring):
                if value.isdigit():
                    return int(value)

            return value

    def deselect_all(self):
        """Deselect all selected options

        :return: True, if all options are deselected
        :rtype: bool
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select':

                select = SeleniumSelect(element)

                try:

                    select.deselect_all()
                    return True

                except NotImplementedError:
                    pass

        return False

    def deselect_by_index(self, option):
        """Deselect option by index [i]

        :param option: Select option index
        :return: True, if option is deselected
        :rtype: bool
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select':

                option = self._to_int(option)

                if isinstance(option, int):

                    select = SeleniumSelect(element)

                    try:
                        select.deselect_by_index(option)
                        return True

                    except NoSuchElementException:
                        pass

        return False

    def deselect_by_text(self, option):
        """Deselect option by display text

        :param option: Select option
        :return: True, if option is deselected
        :rtype: bool
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select' and isinstance(option, basestring):

                select = SeleniumSelect(element)

                try:

                    select.deselect_by_visible_text(option)
                    return True

                except NoSuchElementException:
                    pass

        return False

    def deselect_by_value(self, option):
        """Deselect option by option value

        :param option: Select option value
        :return: True, if option is deselected
        :rtype: bool
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select' and isinstance(option, basestring):

                select = SeleniumSelect(element)

                try:

                    select.deselect_by_value(option)
                    return True

                except NoSuchElementException:
                    pass

        return False

    def options(self):
        """Returns all Select options

        :return: List of options
        :rtype: list
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select':

                select = SeleniumSelect(element)

                options = []

                for option in select.options:
                    options.append(option.text.encode('ascii', 'ignore'))

                return options

        return []

    def selected_first(self):
        """Select first option

        :return: First option element
        :rtype: WebElement
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select':

                select = SeleniumSelect(element)
                options = select.all_selected_options

                if len(options) > 0:
                    return options[0]

        return None

    def selected_options(self):
        """Returns a list of selected options

        :return: List of options
        :rtype: list
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select':

                select = SeleniumSelect(element)
                options = []

                for option in select.all_selected_options:
                    options.append(option.text.encode('ascii', 'ignore'))

                return options

        return []

    def select_by_index(self, option):
        """Select option at index [i]

        :param int option: Select index
        :return: True, if the option is selected
        :rtype: bool
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select':

                option = self._to_int(option)

                if isinstance(option, int):

                    select = SeleniumSelect(element)

                    try:

                        select.select_by_index(option)
                        return True

                    except NoSuchElementException:
                        pass

        return False

    def select_by_text(self, option):
        """Select option by display text

        :param str option: Select option
        :return: True, if the option is selected
        :rtype: bool
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select' and isinstance(option, basestring):

                select = SeleniumSelect(element)

                try:

                    select.select_by_visible_text(option)
                    return True

                except NoSuchElementException:
                    pass

        return False

    def select_by_value(self, option):
        """Select option by option value

        :param str option: Select option value
        :return: True, if the option is selected
        :rtype: bool
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select' and isinstance(option, basestring):

                select = SeleniumSelect(element)

                try:

                    select.select_by_value(option)
                    return True

                except NoSuchElementException:
                    pass

        return False


class SelectiveMixin(ClickMixin):
    """The SelectiveMixin implementation
    """

    def deselect(self):
        """Deselect this element

        :return:
        """

        return self.click() if self.selected() else None

    def select(self):
        """Select this element

        :return:
        """

        return self.click() if not self.selected() else None

    def selected(self):
        """Return True if element is selected

        :return: True, if the element is selected
        :rtype: bool
        """

        return self.element().is_selected() if self.exists() else False


class TextMixin(ElementMixin):
    """The TextMixin implementation
    """

    def __str__(self):
        return self.text()

    @encode_ascii(clean=True)
    def text(self):
        """Returns the text within an element

        :return: Element text
        :rtype: str
        """

        return self.element().get_attribute('textContent') if self.exists() else ''

    @encode_ascii(clean=True)
    def visible_text(self):
        """Returns the visible text within an element

        :return: Element text
        :rtype: str
        """

        return self.element().text if self.exists() else ''
