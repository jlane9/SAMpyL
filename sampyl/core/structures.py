# -*- coding: utf-8 -*-
"""sampyl.core.structures

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

# pylint: disable=line-too-long
import inspect
import sys
import warnings
from selenium.webdriver.common.by import By
from sampyl.core.element import Element, join
from sampyl.core.mixins import ClickMixin, InputMixin, SelectMixin, SelectiveMixin, TextMixin

__all__ = ['Button', 'Div', 'Image', 'InputCheckbox', 'InputRadio', 'InputText', 'Link',
           'MultiSelect', 'Select', 'Text']


class Button(Element, ClickMixin, TextMixin):
    """The Button implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <button id="someClassId" class="someClass"
            on-click="javascript.function()">Click Me</button>


        If the user wants to make the code above recognizable to the testing framework, they
        would add the attribute "data-qa-id" with a unique value as well as "data-qa-model"
        with a type.

        .. code-block:: html

            <button data-qa-id="some.identifier" data-qa-model="button" id="someClassId"
            class="someClass" on-click="javascript.function()">
                Click Me
            </button>


        An example on how to interact with the element:

        .. code-block:: python

            from selenium.webdriver import Chrome
            from sampyl import App

            wd = webdriver.Chrome('/path/to/chromedriver')
            app = App(wd, "http://someurl.com/path")

            # Example usage
            app.page.some.identifier.click()

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


        If the user wants to make the code above recognizable to the testing framework, they
        would add the attribute "data-qa-id" with a unique value as well as "data-qa-model"
        with a type.

        .. code-block:: html

            <div data-qa-id="some.identifier" data-qa-model="div" id="someClassId"
            class="someClass">
                ...
            </div>


        An example on how to interact with the element:

        .. code-block:: python

            from selenium.webdriver import Chrome
            from sampyl import App

            wd = webdriver.Chrome('/path/to/chromedriver')
            app = App(wd, "http://someurl.com/path")

            # Returns True
            app.page.some.identifier.is_displayed()

    """

    pass


class Dropdown(Element, ClickMixin, TextMixin):
    """The Dropdown implementation

    .. note:: This structure is specifically for a Bootstrap dropdown

    **Example Use:**

    .. code-block:: html

            <div class="dropdown">
                <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">Dropdown Example
                <span class="caret"></span></button>
                <ul class="dropdown-menu">
                    <li><a href="#">HTML</a></li>
                    ...
                </ul>
            </div>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value as well as "data-qa-model" with a type.

        .. code-block:: html

            <div class="dropdown" data-qa-id="some.identifier" data-qa-model="dropdown">
                <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">Dropdown Example
                <span class="caret"></span></button>
                <ul class="dropdown-menu">
                    <li><a href="#">HTML</a></li>
                    ...
                </ul>
            </div>


        An example on how to interact with the element:

        .. code-block:: python

            from selenium.webdriver import Chrome
            from sampyl import App

            wd = webdriver.Chrome('/path/to/chromedriver')
            app = App(wd, "http://someurl.com/path")

            # Opens the dropdown
            app.page.some.identifier.expand()

    """

    _toggle_xpath = (By.XPATH, '/descendant-or-self::*[(contains(@class, "dropdown-toggle") or '
                               '@ng-mouseover or @ng-click)]')

    @property
    def _container(self):
        """Dropdown container

        :return:
        """

        xpath = '/following-sibling::*[(contains(@class, "dropdown-menu") or contains(@class, "tree") or @ng-show) ' \
                'and (self::div or self::ul)]'
        child = '/descendant-or-self::*[(contains(@class, "dropdown-menu") or contains(@class, "tree") or @ng-show) ' \
                'and (self::div or self::ul)]'

        xpath_term = join(self.search_term, self._toggle, (By.XPATH, xpath))
        child_term = join(self.search_term, self._toggle, (By.XPATH, child))

        return Div(self.driver, By.XPATH, '|'.join([xpath_term[1], child_term[1]]))

    @property
    def _toggle(self):
        """Show/hide toggle button

        :return:
        """

        return Button(self.driver, *join(self.search_term, self._toggle_xpath))

    def expand(self, hover=False):
        """Show dropdown

        :return:
        """

        if not self._container.is_displayed():

            if hover:
                self._toggle.hover()
            else:
                self._toggle.click()

            return self._container.wait_until_appears()

    def collapse(self, hover=False):
        """Hide dropdown

        :return:
        """

        if self._container.is_displayed():

            if hover:
                self._toggle.hover()
            else:
                self._toggle.click()

            return self._container.wait_until_disappears()


class BadgeDropdown(Dropdown):
    """Badge dropdown to capture hover event
    
    """

    def show(self):
        """Show dropdown on mousein of badge
        
        :return: 
        """

        return self.expand(True)

    def hide(self):
        """Hide dropdown on mouseout of badge
        
        :return: 
        """

        return self.collapse(True)


class Form(Element):

    def _get_field(self, field_name):

        if not isinstance(field_name, basestring):
            raise TypeError

        xpath = '/descendant-or-self::*[((self::input and @type="text") or ' \
                'self::textarea or self::select) and @name="{}"]'
        elements = self.driver.find_elements(*join(self.search_term, (By.XPATH, xpath.format(field_name))))

        if elements:
            return elements[0]

    def get_field(self, field_name):

        field = self._get_field(field_name)

        if field:

            input_xpath = '/descendant-or-self::*[((self::input and @type="text") or self::textarea) and @name="{}"]'
            select_xpath = '/descendant-or-self::*[self::select and @name="{}"]'

            if field.tag_name == u'input' or field.tag_name == u'textarea':
                return InputText(self.driver, *join(self.search_term, (By.XPATH, input_xpath.format(field_name))))

            elif field.tag_name == u'select':
                return Select(self.driver, *join(self.search_term, (By.XPATH, select_xpath.format(field_name))))

            else:
                warnings.warn('{} type not currently supported within form'.format(str(field.tag_name)))


class Image(Element):
    """The Image implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <img id="someClassId" class="someClass" />


        If the user wants to make the code above recognizable to the testing framework, they
        would add the attribute "data-qa-id" with a unique value as well as "data-qa-model"
        with a type.

        .. code-block:: html

            <img data-qa-id="some.identifier" data-qa-model="image" id="someClassId"
            class="someClass" src="http://someSource.net/image.png" />


        An example on how to interact with the element:

        .. code-block:: python

            from selenium.webdriver import Chrome
            from sampyl import App

            wd = webdriver.Chrome('/path/to/chromedriver')
            app = App(wd, "http://someurl.com/path")

            # Returns "http://someSource.net/image.png"
            app.page.some.identifier.source()

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


        If the user wants to make the code above recognizable to the testing framework, they
        would add the attribute "data-qa-id" with a unique value as well as "data-qa-model"
        with a type.

        .. code-block:: html

            <input data-qa-id="some.identifier" data-qa-model="inputcheckbox"
            id="someClassId" type="checkbox" class="someClass">


        An example on how to interact with the element:

        .. code-block:: python

            from selenium.webdriver import Chrome
            from sampyl import App

            wd = webdriver.Chrome('/path/to/chromedriver')
            app = App(wd, "http://someurl.com/path")

            app.page.some.identifier.select()

    """

    @property
    def label(self):
        """Returns the label for the input item

        :return: Returns Text object for label
        :rtype: Text
        """

        if self.exists():
            return Text(self.driver, By.XPATH,
                        '/descendant-or-self::label[@for="{0}"]'.format(str(self.id))).visible_text() \
                if len(self.id) > 0 else ''


class InputRadio(InputCheckbox, SelectiveMixin):
    """The InputRadio implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <input id="someClassId" type="radio" class="someClass">


        If the user wants to make the code above recognizable to the testing framework, they
        would add the attribute "data-qa-id" with a unique value as well as "data-qa-model"
        with a type.

        .. code-block:: html

            <input data-qa-id="some.identifier" data-qa-model="inputradio" id="someClassId"
            type="radio" class="someClass">


        An example on how to interact with the element:

        .. code-block:: python

            from selenium.webdriver import Chrome
            from sampyl import App

            wd = webdriver.Chrome('/path/to/chromedriver')
            app = App(wd, "http://someurl.com/path")

            app.page.some.identifier.select()

    """

    pass


class InputText(Element, InputMixin, ClickMixin):
    """The InputText implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <input id="someClassId" type="text" class="someClass">


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value as well as "data-qa-model" with a type.

        .. code-block:: html

            <input data-qa-id="some.identifier" data-qa-model="inputtext" id="someClassId" type="text"
            class="someClass">


        An example on how to interact with the element:

        .. code-block:: python

            from selenium.webdriver import Chrome
            from sampyl import App

            wd = webdriver.Chrome('/path/to/chromedriver')
            app = App(wd, "http://someurl.com/path")

            app.page.some.identifier.input('Hello World')

    """

    @property
    def label(self):
        """Returns the label for the input item

        :return: Text object for label
        :rtype: Text
        """

        if self.exists():
            return Text(self.driver, By.XPATH,
                        '/descendant-or-self::label[@for="{0}"]'.format(str(self.id))).visible_text() \
                if len(self.id) > 0 else ''


class Link(Element, ClickMixin, TextMixin):
    """The Link implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <a id="someClassId" class="someClass" href="/some/link/path">Click Me</a>


        If the user wants to make the code above recognizable to the testing framework, they
        would add the attribute "data-qa-id" with a unique value as well as "data-qa-model"
        with a type.

        .. code-block:: html

            <a data-qa-id="some.identifier" id="someClassId" class="someClass"
            href="/some/link/path">Click Me</a>


        An example on how to interact with the element:

        .. code-block:: python

            from selenium.webdriver import Chrome
            from sampyl import App

            wd = webdriver.Chrome('/path/to/chromedriver')
            app = App(wd, "http://someurl.com/path")

            app.page.some.identifier.click()

    """

    pass


class MultiSelect(Element):
    """The MultiSelect implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <div id="someClassId" class="someClass" isteven-multi-select input-model="some.model"
            output-model="format.model" helper-elements="filter all none">
                ...
            </div>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value as well as "data-qa-model" with a type.

        .. code-block:: html

            <div data-qa-id="some.identifier" data-qa-model="multiselect" id="someClassId" class="someClass"
            isteven-multi-select input-model="some.model" output-model="format.model" helper-elements="filter all none">
                ...
            </div>


        An example on how to interact with the element:

        .. code-block:: python

            from selenium.webdriver import Chrome
            from sampyl import App

            wd = webdriver.Chrome('/path/to/chromedriver')
            app = App(wd, "http://someurl.com/path")

            # Opens the iSteven dropdown
            app.page.some.identifier.expand()

    """

    @property
    def _container(self):
        """iSteven dropdown container

        :return:
        """

        xpath = '/descendant-or-self::div[contains(@class, "checkboxLayer")]'

        return Div(self.driver, *join(self.search_term, (By.XPATH, xpath)))

    @property
    def _toggle(self):
        """Show/hide button

        :return:
        """

        xpath = '/descendant-or-self::button[contains(@ng-click, "toggle")]'

        return Button(self.driver, *join(self.search_term, (By.XPATH, xpath)))

    @property
    def _select_all(self):
        """Select all button

        :return:
        """

        xpath = '/descendant-or-self::button[contains(@ng-click, "all")]'

        return Button(self.driver, *join(self.search_term, (By.XPATH, xpath)))

    @property
    def _select_none(self):
        """Select none button

        :return:
        """

        xpath = '/descendant-or-self::button[contains(@ng-click, "none")]'

        return Button(self.driver, *join(self.search_term, (By.XPATH, xpath)))

    @property
    def _reset(self):
        """Reset button

        :return:
        """

        xpath = '/descendant-or-self::button[contains(@ng-click, "reset")]'

        return Button(self.driver, *join(self.search_term, (By.XPATH, xpath)))

    @property
    def _filter(self):
        """Search field

        :return:
        """

        xpath = '/descendant-or-self::input[contains(@ng-click, "filter")]'

        return InputText(self.driver, *join(self.search_term, (By.XPATH, xpath)))

    @property
    def _clear(self):
        """Clear search button

        :return:
        """

        xpath = '/descendant-or-self::button[contains(@ng-click, "clear")]'

        return Button(self.driver, *join(self.search_term, (By.XPATH, xpath)))

    def _get_index(self, idx):
        """Return item at index 'i'

        :param str idx: Index
        :return:
        """

        if isinstance(idx, int) or isinstance(idx, basestring):

            # Convert string to integer
            if isinstance(idx, str):

                if idx.isdigit():
                    idx = int(idx)

                else:
                    raise TypeError('Error: Index must be of type int')

            if idx in range(0, len(self.options())):
                return Button(self.driver, *join(self.search_term,
                                                 (By.XPATH, '/descendant-or-self::div[contains(@ng-repeat, '
                                                            '"filteredModel")][{}]'.format(idx))))

    def _get_text(self, text):
        """Return selection that contains text criteria

        :param str text: Text criteria
        :return:
        """

        if isinstance(text, basestring):

            return Button(self.driver, *join(self.search_term,
                                             (By.XPATH, '/descendant-or-self::label[contains(., "{}")]/ancestor::div'
                                                        '[contains(@ng-repeat, "filteredModel")]'.format(text))))

    def expand(self):
        """Show iSteven dropdown

        :return:
        """

        if not self._container.is_displayed():
            self._toggle.click()
            self._container.wait_until_appears()

    def collapse(self):
        """Hide iSteven dropdown

        :return:
        """

        if self._container.is_displayed():
            self._toggle.click()
            self._container.wait_until_disappears()

    def select_all(self):
        """Select all possible selections

        :return:
        """

        self.expand()
        self._select_all.click()

    def select_none(self):
        """Deselect all selections

        :return:
        """

        self.expand()
        self._select_none.click()

    def reset(self):
        """Reset selection to default state

        :return:
        """

        self.expand()
        self._reset.click()

    def search(self, value, clear=True):
        """Filter selections to those matching search criteria

        :param str value: Search criteria
        :param bool clear: Clear previous search criteria
        :return:
        """

        self.expand()
        self._filter.input(value, clear)

    def clear_search(self):
        """Click clear search button

        :return:
        """

        self.expand()
        self._clear.click()

    def select_by_index(self, index):
        """Select option at index 'i'

        :param str index: Index
        :return:
        """

        self.expand()

        option = self._get_index(index)

        if option:
            if 'selected' not in option.class_:
                option.click()

    def select_by_text(self, text):
        """Select option that matches text criteria

        :param str text: Text criteria
        :return:
        """

        self.expand()

        option = self._get_text(text)

        if option.exists():
            option.click()

    def deselect_by_index(self, index):
        """Deselect option at index 'i'

        :param str index: Index
        :return:
        """

        self.expand()

        option = self._get_index(index)

        if option:
            if 'selected' in option.class_:
                option.click()

    def deselect_by_text(self, text):
        """Deselect option that matches text criteria

        :param str text: Text criteria
        :return:
        """

        self.expand()

        option = self._get_text(text)

        if option.exists():
            option.click()

    def options(self):
        """Return all available options

        :return: List of options
        :rtype: list
        """

        search_term = join(self.search_term, (By.XPATH, '/descendant-or-self::div[contains(@ng-repeat, '
                                                        '"filteredModel")]//label'))

        return [element.get_attribute('textContent').encode('ascii', 'ignore')
                for element in self.driver.find_elements(*search_term)]

    def selected_options(self):
        """Return all selected options

        :return: List of selected options
        :rtype: list
        """

        search_term = join(self.search_term, (By.XPATH, '/descendant-or-self::div[contains(@ng-repeat, '
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


        If the user wants to make the code above recognizable to the testing framework, they
        would add the attribute "data-qa-id" with a unique value as well as "data-qa-model"
        with a type.

        .. code-block:: html

            <select data-qa-id="some.identifier" data-qa-model="select" id="someClassId"
            class="someClass">
                <option value="1">Value 1</option>
                <option value="2">Value 2</option>
                <option value="3">Value 3</option>
                <option value="4">Value 4</option>
            </select>


        An example on how to interact with the element:

        .. code-block:: python

            from selenium.webdriver import Chrome
            from sampyl import App

            wd = webdriver.Chrome('/path/to/chromedriver')
            app = App(wd, "http://someurl.com/path")

            # Example usage. Returns ['Value 1', 'Value 2', 'Value 3', 'Value 4']
            app.page.some.identifier.options()
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


        If the user wants to make the code above recognizable to the testing framework, they
        would add the attribute "data-qa-id" with a unique value.

        .. code-block:: html

            <p data-qa-id="some.identifier" data-qa-model="text" id="someClassId"
            class="someClass">
                ...
            </p>


        An example on how to interact with the element:

        .. code-block:: python

            from selenium.webdriver import Chrome
            from sampyl import App

            wd = webdriver.Chrome('/path/to/chromedriver')
            app = App(wd, "http://someurl.com/path")

            # Prints text inside text elements
            print app.page.some.identifier

    """

    pass


MEMBERS = inspect.getmembers(sys.modules[__name__], predicate=lambda o: inspect.isclass(o) and issubclass(o, Element))
TYPES = {_type[0].lower(): _type[1] for _type in MEMBERS}
