# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Account metrics."""

from __future__ import absolute_import

from datetime import datetime, timedelta

from flask import current_app
from invenio_accounts.models import User

from ..models import Metric


class AccountsMetric(Metric):
    """Aggregated metrics for number of accounts."""

    metric_class = "accounts"
    object_type = "System"

    @classmethod
    def all(cls):
        """Compute bibsched queue length."""
        dt = datetime.now() - timedelta(hours=6)

        system_name = current_app.config.get(
            'METRICS_ACCOUNTS_SYSTEMNAME', 'Invenio')

        data = {system_name: {
            'num': User.query.count(),
            'num.blocked': User.query.filter_by(active=False).count(),
            'num.active': User.query.filter_by(active=True).count(),
            'num.unconfirmed': User.query.filter(
                User.confirmed_at.is_(None)).count(),
            'logins6h': User.query.filter(User.current_login_at >= dt).count(),
        }}
        return data.items()
