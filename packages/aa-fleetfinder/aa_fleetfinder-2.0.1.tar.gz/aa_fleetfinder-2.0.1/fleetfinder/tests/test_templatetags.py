"""
Test the apps' template tags
"""

# Django
from django.template import Context, Template
from django.test import TestCase

# AA Fleet Finder
from fleetfinder import __version__


class TestVersionedStatic(TestCase):
    """
    Test the fleetfinder_static template tag
    """

    def test_versioned_static(self):
        """
        Test should return a versioned static

        :return:
        :rtype:
        """

        context = Context(dict_={"version": __version__})
        template_to_render = Template(
            template_string=(
                "{% load fleetfinder %}"
                "{% fleetfinder_static 'fleetfinder/css/fleetfinder.min.css' %}"
            )
        )

        rendered_template = template_to_render.render(context)

        self.assertInHTML(
            needle=f'/static/fleetfinder/css/fleetfinder.min.css?v={context["version"]}',
            haystack=rendered_template,
        )
