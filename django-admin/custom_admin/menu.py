import os
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from admin_tools.menu import items, Menu


class CustomMenu(Menu):
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            
            items.AppList(
                _('Applications'),
                exclude=('django.contrib.*',)
            ),
            items.AppList(
                _('Administration'),
                models=('django.contrib.*',)
            ),
            self.get_version_menu_item(),
        ]
    
    def get_version_menu_item(self) -> items.MenuItem:
        project_name = os.environ.get('CI_PROJECT_NAME')
        environ = os.environ.get('STAGE')
        commit = os.environ.get('CI_COMMIT_SHORT_SHA')
        return items.MenuItem(
            'Версия',
            children=[
                items.MenuItem(f'Проект: {project_name}'),
                items.MenuItem(f'Окружение: {environ}'),
                items.MenuItem(f'Коммит: {commit}'),
            ],
            css_classes={
                'prod': ['build-prod'],
                'dev': ['build-dev'],
            }.get(environ, [])
        )

    def init_with_context(self, context):
        return super(CustomMenu, self).init_with_context(context)
