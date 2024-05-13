# -*- coding: utf-8; -*-

from unittest import TestCase

import sqlalchemy as sa

from rattail import clientele
from rattail.config import make_config


class TestClienteleHandler(TestCase):

    def setUp(self):
        self.config = make_config([], extend=False)
        self.app = self.config.get_app()
        self.handler = clientele.ClienteleHandler(self.config)
        self.engine = sa.create_engine('sqlite://')
        self.app.model.Base.metadata.create_all(bind=self.engine)

    def test_get_all_customers(self):
        model = self.app.model
        session = self.app.make_session(bind=self.engine)

        # add some customers
        session.add(model.Customer(name='Fred Flintstone'))
        session.add(model.Customer(name='Wilma Flintstone'))
        session.add(model.Customer(name='Barney Rubble', active_in_pos=False))

        # getting "all" will exclude inactive by default
        customers = self.handler.get_all_customers(session)
        self.assertEqual(len(customers), 2)

        # but we can request them too
        customers = self.handler.get_all_customers(session, include_inactive=True)
        self.assertEqual(len(customers), 3)

        session.commit()
        session.close()
