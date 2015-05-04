from __future__ import unicode_literals, print_function
from django.conf import settings
from django.utils.module_loading import import_string


class BaseParser(object):
    def parse(self):
        """
        Should get and return list of entries
        """
        raise NotImplemented('You should implement "parse" method')

    def make_instance(self):
        """
        Should return instance that will be populated with values from feed item
        """
        if self.model:
            return self.model()
        raise NotImplemented('You should implement "make_instance" method or define "model" attribute')

    def pre_save(self, item, instance):
        """
        Called right before saving instance
        """
        pass

    def post_save(self, item, instance):
        """
        Called right after saving instance
        """
        pass


class Importer(object):

    def do_import(self, use_parsers=None, override_settings=None):

        use_settings = override_settings or settings.PARSERS
        parsers = use_settings.items()

        if use_parsers is not None:
            parsers = filter(lambda x: x[0] in use_parsers, parsers)

        for name, parser_info in parsers:
            parser = import_string(parser_info['parser'])()
            excludes = parser_info.get('excludes', [])
            item_list = parser.parse()

            for item in item_list:
                instance = parser.make_instance()

                all_field_names = [field.name for field in type(instance)._meta.get_fields()]

                if excludes:
                    field_names = filter(lambda x: x not in excludes, all_field_names)
                else:
                    field_names = all_field_names

                for field_name in field_names:
                    getter_name = 'get_%s' % field_name
                    try:
                        value = getattr(parser, getter_name, None)(item)
                        setattr(instance, field_name, value)
                    except TypeError:
                        # no such getter :(
                        continue

                parser.pre_save(item, instance)
                instance.save()
                parser.post_save(item, instance)