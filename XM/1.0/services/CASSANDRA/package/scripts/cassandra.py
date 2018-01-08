#!/usr/bin/env python
from resource_management import *
from resource_management.core.resources import Directory
from resource_management.core.resources.system import Execute, File

from resource_management.core.source import InlineTemplate, Template
from resource_management.libraries.functions.format import format


# wget http://rpm.datastax.com/community/noarch/opscenter-5.2.5-1.noarch.rpm
# wget http://rpm.datastax.com/community/noarch/cassandra30-3.0.9-1.noarch.rpm
# wget http://rpm.datastax.com/community/noarch/cassandra30-tools-3.0.9-1.noarch.rpm

def cassandra():
    import params

    Directory(
        [params.log_dir, params.pid_dir, params.conf_dir],
        owner=params.cassandra_user,
        group=params.user_group,
        recursive=True)
    configurations = params.config['configurations']['cassandra-site']

    File(
        format("{conf_dir}/cassandra.yaml"),
        content=Template(
            "cassandra.yaml.j2", configurations=configurations),
        owner=params.cassandra_user,
        group=params.user_group)
