# coding: utf-8

import json

import requests
from sentry.plugins.bases.notify import NotificationPlugin

import sentry_dingding
from .forms import DingDingOptionsForm

DingTalk_API = "https://oapi.dingtalk.com/robot/send?access_token={token}"


class DingDingPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to DingDing.
    """
    author = 'wilson-loo'
    author_url = 'https://github.com/wilsonloo/sentry-stack-dingding'
    version = sentry_dingding.VERSION
    description = 'Send error counts to DingDing with stack preview'
    resource_links = [
        ('Source', 'https://github.com/wilsonloo/sentry-stack-dingding.git'),
        ('Bug Tracker', 'https://github.com/wilsonloo/sentry-stack-dingding.git/issues'),
        ('README', 'https://github.com/wilsonloo/sentry-stack-dingding.git/blob/master/README.md'),
    ]

    slug = 'DingDing'
    title = 'DingDing'
    conf_key = slug
    conf_title = title
    project_conf_form = DingDingOptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('access_token', project)) and bool(self.get_option('stack_deep', project))

    def notify_users(self, group, event, *args, **kwargs):
        self.post_process(group, event, *args, **kwargs)

    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        if group.is_ignored():
            return

        access_token = self.get_option('access_token', group.project)
        send_url = DingTalk_API.format(token=access_token)
        title = u'【%s】的项目异常' % event.project.slug

        # splice stack
        stackDeep=self.get_option('stack_deep', group.project)
        # if event.data:
        #     if event.data["frames"]:
        #         stack = event.data["frames"]
        #     if event.data["stack"]:
        #         stack = event.data["stack"]

        # project_id, event_id, _snuba_data, _group_id, _groups_cache, _group_ids, _data, _project_cache, interfaces, search_message, _group_cache
        keys = vars(event).keys()
        event_keys_str = "[event keys:]" + ', '.join(keys)

        # data, _len
        interfaces = event.interfaces
        keys = vars(interfaces).keys()
        event_keys_str = event_keys_str + " [interface keys:]" + ', '.join(keys)

        event_keys_str = event_keys_str + " [interfaces:]" + type(interfaces) + "val:" + interfaces
        if 'data' in interfaces:
            event_keys_str = event_keys_str + " [data:]" + type(interfaces['data']) + "val:" + interfaces['data']
            # keys = vars(interfaces['data']).keys()
            # event_keys_str = event_keys_str + " [data keys:]" + ', '.join(keys)        

        # if stack:
        # # if event.frames and len(event.frames) > 0:
        # #     stack = event.frames[:stackDeep]
        #     stack = json.dumps(stack, indent=2)
        
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": u"#### {title} \n\n > {message} \n\n {stack} \n\n [详细信息]({url})".format(
                    title=title,
                    message=event.message or event.title,
                    stack=event_keys_str,
                    url=u"{}events/{}/".format(group.get_absolute_url(), event.event_id),
                )
            }
        }
        requests.post(
            url=send_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data).encode("utf-8")
        )
