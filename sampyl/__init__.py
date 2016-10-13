from sampyl.core.element import SeleniumObject
from urlparse import urlparse


class App(SeleniumObject):
    """The App implementation
    """

    scheme = ''
    hostname = ''

    def __init__(self, web_driver, url=None):

        super(App, self).__init__(web_driver)

        url_path = url if isinstance(url, basestring) else ''
        path = urlparse(url_path)

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
        """

        :param str path:
        :return:
        """

        if isinstance(path, basestring):
            self.get('%s://%s%s' % (self.scheme, self.hostname, urlparse(path).path))
