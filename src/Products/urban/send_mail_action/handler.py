# -*- coding: utf-8 -*-

from plone.app.contentrules.handlers import execute_rules


def send_mail_action(event):
    execute_rules(event)
