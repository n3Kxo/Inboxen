# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-16 22:31
from __future__ import unicode_literals

import cms.fields
from django.db import migrations
import inboxen.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_auto_20180105_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helppage',
            name='body',
            field=cms.fields.RichTextField(allow_tags=[b'p', b'a', b'i', b'b', b'em', b'strong', b'ol', b'ul', b'li', b'pre', b'code', b'h1', b'h2', b'h3', b'h4', b'h5'], extensions=[b'markdown.extensions.toc'], help_text='Markdown text, support the TOC extension.', safe_attrs=[b'href', b'id'], validators=[inboxen.validators.ProhibitNullCharactersValidator()]),
        ),
        migrations.AlterField(
            model_name='peoplepage',
            name='intro_paragraph',
            field=cms.fields.RichTextField(blank=True, help_text='Text at the top of the page. Supports standard markdown.', validators=[inboxen.validators.ProhibitNullCharactersValidator()]),
        ),
    ]
