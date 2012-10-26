from django.db import models
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters import HtmlFormatter
from pygments import highlight

LEXER_CHOICES = sorted([(item[1][0], item[0]) for item in get_all_lexers()])
STYLE_CHOICES = sorted((item, item) for item in list(get_all_styles()))


class Snippet(models.Model):
    owner = models.ForeignKey('auth.User', related_name='snippets')
    title = models.CharField(max_length=100, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LEXER_CHOICES,
                                default='python',
                                max_length=100)
    style = models.CharField(choices=STYLE_CHOICES,
                             default='friendly',
                             max_length=100)
    highlighted = models.TextField()

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)
