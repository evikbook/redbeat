
from celery.schedules import schedule


try:  # celery 3.x
    from celery.tests.case import AppCase
except ImportError:  # celery 4.x
    from unittest import TestCase
    from celery.contrib.testing.app import TestApp

    class AppCase(TestCase):
        def setUp(self):
            try:
                self.app = TestApp(config=self.config_dict)
            except:
                self.app = TestApp()
            self.setup()

from fakeredis import FakeStrictRedis
from redbeat.schedulers import RedBeatSchedulerEntry


class RedBeatCase(AppCase):

    def setup(self):
        self.app.conf.add_defaults({
            'REDBEAT_KEY_PREFIX': 'rb-tests:',
            'redbeat_key_prefix': 'rb-tests:',
        })
        self.app.redbeat_redis = FakeStrictRedis(decode_responses=True)
        self.app.redbeat_redis.flushdb()

    def create_entry(self, name=None, task=None, s=None, run_every=60, **kwargs):

        if name is None:
            name = 'test'

        if task is None:
            task = 'tasks.test'

        if s is None:
            s = schedule(run_every=run_every)

        e = RedBeatSchedulerEntry(name, task, s, app=self.app, **kwargs)

        return e
