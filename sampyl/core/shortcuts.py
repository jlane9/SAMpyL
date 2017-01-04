# -*- coding: utf-8 -*-
"""sampyl.core.shortcuts

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

# pylint: disable=line-too-long
__all__ = ['encode_ascii']


def encode_ascii(clean=False):
    """Function returns text as ascii

    :param clean: True, to delete trailing spaces
    :return:
    """

    def encode_ascii_decorator(func):
        """

        :param func:
        :return:
        """

        def func_wrapper(*args, **kwargs):
            """

            :param args:
            :param kwargs:
            :return:
            """

            text = func(*args, **kwargs)

            # Convert UNICODE to ASCII
            if isinstance(text, basestring):
                return text.encode('ascii', 'ignore').strip() if clean else text.encode('ascii', 'ignore')

            # Iterate list of UNICODE strings to ASCII
            elif isinstance(text, (list, tuple)):

                if clean:
                    return [item.encode('ascii', 'ignore').strip() for item in text
                            if isinstance(item, basestring)]

                return [item.encode('ascii', 'ignore') for item in text
                        if isinstance(item, basestring)]

            return ''

        return func_wrapper

    return encode_ascii_decorator
