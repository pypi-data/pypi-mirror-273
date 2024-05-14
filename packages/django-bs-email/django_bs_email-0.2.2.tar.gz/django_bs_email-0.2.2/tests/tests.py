from django.template import Context, Template
from django.test import TestCase


class CustomTemplateTagTests(TestCase):
    def test_custom_template_tag(self):
        # Define the custom template tag usage
        template_code = """
            {% load bootstrap_email %}
            {% bootstrap_email %}
            <body class="bg-light">
                <p>Hello, world!</p>
            </body>
            {% end_bootstrap_email %}
        """

        # Render the template with the given context
        rendered_template = Template(template_code).render(Context({}))

        # Assert that it actually compiles
        self.assertIn(
            "<!-- Compiled with Python Bootstrap Email version:",
            rendered_template,
        )
