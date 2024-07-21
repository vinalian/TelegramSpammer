from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    template = 'admin_tools/dashboard/custom-dashboard.html'
    
    class Media:
        css = {
            'all': ('admin_tools/css/custom-dashboard.css', 'admin_tools/css/custom-menu.css')
        }
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))

        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('django.contrib.*',),
        ))

        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*',),
        ))

        self.children.append(modules.RecentActions(_('Recent Actions'), 5))
        

class CustomAppIndexDashboard(AppIndexDashboard):
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            ) 
        ]

    def init_with_context(self, context):
        return super(CustomAppIndexDashboard, self).init_with_context(context)
