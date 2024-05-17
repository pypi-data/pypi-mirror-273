"""
Tests for the template tags
"""

# Django
from django.template import Context, Template
from django.test import TestCase

# AA Discord Announcements
from aa_discord_announcements import __version__


class TestVersionedStatic(TestCase):
    """
    Test aa_discord_announcements_static
    """

    def test_versioned_static(self):
        """
        Test versioned static template tag
        :return:
        """

        context = Context(dict_={"version": __version__})
        template_to_render = Template(
            template_string=(
                "{% load aa_discord_announcements %}"
                "{% aa_discord_announcements_static 'aa_discord_announcements/css/aa-discord-announcements.min.css' %}"  # pylint: disable=line-too-long
            )
        )

        rendered_template = template_to_render.render(context=context)

        self.assertInHTML(
            needle=f'/static/aa_discord_announcements/css/aa-discord-announcements.min.css?v={context["version"]}',  # pylint: disable=line-too-long
            haystack=rendered_template,
        )
