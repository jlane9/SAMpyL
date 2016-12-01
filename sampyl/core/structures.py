# -*- coding: utf-8 -*-
"""sampyl.core.structures

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

import inspect
import sys
from selenium.webdriver.common.by import By
from sampyl.core.element import Element, join
from sampyl.core.mixins import *

__all__ = ['Button', 'Div', 'Form', 'Image', 'InputCheckbox', 'InputRadio', 'InputText', 'Link', 'MultiSelect',
           'Select', 'Text']


class Button(Element, ClickMixin, TextMixin):
    """The Button implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <button id="someClassId" class="someClass" on-click="javascript.function" >Click Me</button>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <button data-qa-id="some-identifier" id="someClassId" class="someClass" on-click="javascript.function">
                Click Me
            </button>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//button[@data-qa-id="some-identifier"]")
            b = structures.Button(driver, *locator)

            # Example usage
            b.click()
    """

    pass


class Div(Element):
    """The Div implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <div id="someClassId" class="someClass">
                ...
            </div>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <div data-qa-id="some-identifier" id="someClassId" class="someClass">
                ...
            </div>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//button[@data-qa-id="some-identifier"]")
            d = structures.Button(driver, *locator)

    """

    pass


class Form(Element):

    FIELD_TYPES = ('button', 'input', 'select')

    def fields(self):

        xpath = '/descendant-or-self::*[{0}]'.format(' or '.join(['contains(@data-qa-model, "{0}")'.format(_type)
                                                                  for _type in self.FIELD_TYPES]))

        elements = self.driver.find_elements(*join(self.search_term, (By.XPATH, xpath)))

        return [element.get_attribute('data-qa-id') for element in elements]


class Image(Element):
    """The Image implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <img id="someClassId" class="someClass" />


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <img data-qa-id="some-identifier" id="someClassId" class="someClass" />


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//img[@data-qa-id="some-identifier"]")
            i = structures.Image(driver, *locator)

            # Returns tag attribute 'src'
            i.source()
    """

    def source(self):
        """Returns image source URL

        :return: Image source URL
        :rtype: str
        """

        return self.src


class InputCheckbox(Element, SelectiveMixin):
    """The InputCheckbox implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <input id="someClassId" type="checkbox" class="someClass">


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <input data-qa-id="some-identifier" id="someClassId" type="checkbox" class="someClass">


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//input[@data-qa-id="some-identifier"]")
            c = structures.InputCheckbox(driver, *locator)

            # Example usage
            c.select()
    """

    def label(self):
        """Returns the label for the input item

        :return: Returns Text object for label
        :rtype: Text
        """

        if self.exists():
            return Text(self.driver, By.XPATH, '//label[@for="{0}"]'.format(str(self.id))).visible_text() \
                if len(self.id) > 0 else ''


class InputRadio(InputCheckbox, SelectiveMixin):
    """The InputRadio implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <input id="someClassId" type="radio" class="someClass">


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <input data-qa-id="some-identifier" id="someClassId" type="radio" class="someClass">


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            r = structures.InputRadio(driver, "//input[@data-qa-id="some-identifier"]")

            # Input Radio inherits from InputCheckbox
            r.select()
    """

    pass


class InputText(Element, InputMixin, ClickMixin):
    """The InputText implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <input id="someClassId" type="text" class="someClass">


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <input data-qa-id="some-identifier" id="someClassId" type="text" class="someClass">


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//input[@data-qa-id="some-identifier"]")
            t = structures.InputText(driver, *locator)

            # Example usage
            t.input('Hello World')
    """

    def label(self):
        """Returns the label for the input item

        :return: Text object for label
        :rtype: Text
        """

        if self.exists():
            return Text(self.driver, By.XPATH, '//label[@for="{0}"]'.format(str(self.id))).visible_text() \
                if len(self.id) > 0 else ''


class Link(Button, ClickMixin, TextMixin):
    """The Link implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <a id="someClassId" class="someClass" href="/some/link/path">Click Me</a>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <a data-qa-id="some-identifier" id="someClassId" class="someClass" href="/some/link/path">Click Me</a>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//a[@data-qa-id="some-identifier"]")
            l = structures.Link(driver, *locator)

            # Inherits from Button
            l.click()
    """

    pass


class MultiSelect(Element):

    @property
    def _container(self):
        return Div(self.driver, *join(self.search_term,
                                      (By.XPATH, '/descendant-or-self::div[contains(@class, "checkboxLayer")]')))

    @property
    def _toggle(self):
        return Button(self.driver, *join(self.search_term,
                                         (By.XPATH, '/descendant-or-self::button[contains(@ng-click, "toggle")]')))

    @property
    def _select_all(self):
        return Button(self.driver, *join(self.search_term,
                                         (By.XPATH, '/descendant-or-self::button[contains(@ng-click, "all")]')))

    @property
    def _select_none(self):
        return Button(self.driver, *join(self.search_term,
                                         (By.XPATH, '/descendant-or-self::button[contains(@ng-click, "none")]')))

    @property
    def _reset(self):
        return Button(self.driver, *join(self.search_term,
                                         (By.XPATH, '/descendant-or-self::button[contains(@ng-click, "reset")]')))

    @property
    def _search(self):
        return InputText(self.driver, *join(self.search_term,
                                            (By.XPATH, '/descendant-or-self::input[contains(@ng-click, "filter")]')))

    @property
    def _clear(self):
        return Button(self.driver, *join(self.search_term,
                                         (By.XPATH, '/descendant-or-self::button[contains(@ng-click, "clear")]')))

    def _get_index(self, idx):

        if isinstance(idx, int) or isinstance(idx, basestring):

            # Convert string to integer
            if isinstance(idx, str):

                if idx.isdigit():
                    idx = int(idx)

                else:
                    raise TypeError('Error: Index must be of type int')

            if idx in range(1, len(self.options())):
                return Button(self.driver, *join(self.search_term,
                                                 (By.XPATH, '/descendant-or-self::div[contains(@ng-repeat, '
                                                            '"filteredModel")][{}]'.format(idx))))

    def _get_text(self, text):

        if isinstance(text, basestring):

            return Button(self.driver, *join(self.search_term,
                                             (By.XPATH, '/descendant-or-self::label[contains(., "{}")]/ancestor::div'
                                                        '[contains(@ng-repeat, "filteredModel")]'.format(text))))

    def expand(self):

        if not self._container.is_displayed():
            self._toggle.click()

    def collapse(self):

        if self._container.is_displayed():
            self._toggle.click()

    def select_all(self):

        self._select_all.click()

    def select_none(self):

        self._select_none.click()

    def reset(self):

        self._reset.click()

    def search(self, value, clear=True):

        self._search.input(value, clear)

    def clear_search(self):

        self._clear.click()

    def select_by_index(self, index):

        self.expand()

        option = self._get_index(index)

        if option:
            if 'selected' not in option.cls:
                option.click()

    def select_by_text(self, text):

        self.expand()

        option = self._get_text(text)

        if option.exists():
            option.click()

    def deselect_by_index(self, index):

        self.expand()

        option = self._get_index(index)

        if option:
            if 'selected' in option.cls:
                option.click()

    def deselect_by_text(self, text):

        self.expand()

        option = self._get_text(text)

        if option.exists():
            option.click()

    def options(self):

        search_term = join(self.search_term,  (By.XPATH, '/descendant-or-self::div[contains(@ng-repeat, '
                                                         '"filteredModel")]//label'))

        return [element.get_attribute('textContent').encode('ascii', 'ignore')
                for element in self.driver.find_elements(*search_term)]

    def selected_options(self):

        search_term = join(self.search_term,  (By.XPATH, '/descendant-or-self::div[contains(@ng-repeat, '
                                                         '"filteredModel") and contains(@class, "selected")]//label'))

        return [element.get_attribute('textContent').encode('ascii', 'ignore')
                for element in self.driver.find_elements(*search_term)]


class Select(Element, SelectMixin):
    """The Select implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <select id="someClassId" class="someClass">
                <option value="1">Value 1</option>
                <option value="2">Value 2</option>
                <option value="3">Value 3</option>
                <option value="4">Value 4</option>
            </select>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <select data-qa-id="some-identifier" id="someClassId" class="someClass">
                <option value="1">Value 1</option>
                <option value="2">Value 2</option>
                <option value="3">Value 3</option>
                <option value="4">Value 4</option>
            </select>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//input[@data-qa-id="some-identifier"]")
            s = structures.Select(driver, *locator)

            # Example usage. Returns ['Value 1', 'Value 2', 'Value 3', 'Value 4']
            s.options()
    """

    pass


class Text(Element, TextMixin, ClickMixin):
    """The Text implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <p id="someClassId" class="someClass">
                ...
            </p>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <p data-qa-id="some-identifier" id="someClassId" class="someClass">
                ...
            </p>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//p[@data-qa-id="some-identifier"]")
            d = structures.Text(driver, *locator)

            # Prints text inside text elements
            print d
    """

    pass


MEMBERS = inspect.getmembers(sys.modules[__name__], predicate=lambda o: inspect.isclass(o) and issubclass(o, Element))
TYPES = {_type[0].lower(): _type[1] for _type in MEMBERS}
