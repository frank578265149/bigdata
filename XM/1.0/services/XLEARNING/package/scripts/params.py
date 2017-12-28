#!/usr/bin/env python

from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.default import default
from resource_management.libraries.resources import HdfsResource
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources

config = Script.get_config()
install_dir = config['configurations']['xlearning-env']['install_dir']
download_url = config['configurations']['xlearning-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

java64_home = config['hostLevelParams']['java_home']
conf_dir = '/etc/xlearning'
xlearning_user = config['configurations']['xlearning-env']['xlearning_user']
xlearning_group = user_group = config['configurations']['cluster-env']['user_group']
xlearning_log_dir = config['configurations']['xlearning-env']['xlearning_log_dir']

xlearning_principal = default('configurations/xlearning-env/xlearning_principal', 'xlearning')
xlearning_keytab = default('configurations/xlearning-env/xlearning_keytab', '')

xlearning_pid_dir = config['configurations']['xlearning-env']['xlearning_pid_dir']
xlearning_pid_file = format("{xlearning_pid_dir}/xlearning.pid")

env_content = config['configurations']['xlearning-env']['env_content']
log_content = config['configurations']['xlearning-env']['log_content']
jaas_content = config['configurations']['xlearning-env']['jaas_content']

security_enabled = config['configurations']['cluster-env']['security_enabled']

history_log_dir = config['configurations']['xlearning-site']['xlearning.history.log.dir']
tf_board_history_dir = config['configurations']['xlearning-site']['xlearning.history.log.dir']
xlearning_staging_dir = config['configurations']['xlearning-site']['xlearning.history.log.dir']

kerberos_params = ''

if security_enabled:
    _hostname_lowercase = config['hostname'].lower()
    xlearning_principal = xlearning_principal.replace('_HOST', _hostname_lowercase)
    kerberos_params = " -Djava.security.auth.login.config=" + conf_dir + "/xlearning_jaas.conf"

hadoop_bin_dir = '/opt/hadoop/bin'
hadoop_conf_dir = '/etc/hadoop'
hdfs_site = config['configurations']['hdfs-site']
default_fs = config['configurations']['core-site']['fs.defaultFS']
dfs_type = default("/commandParams/dfs_type", "")
kinit_path_local = get_kinit_path(default('/configurations/kerberos-env/executable_search_paths', None))
security_enabled = config['configurations']['cluster-env']['security_enabled']
smokeuser = config['configurations']['cluster-env']['smokeuser']
smokeuser_principal = config['configurations']['cluster-env']['smokeuser_principal_name']
smoke_user_keytab = config['configurations']['cluster-env']['smokeuser_keytab']
hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
hdfs_principal_name = config['configurations']['hadoop-env']['hdfs_principal_name']
hdfs_user_keytab = config['configurations']['hadoop-env']['hdfs_user_keytab']
import functools

HdfsResource = functools.partial(
    HdfsResource,
    user=hdfs_user,
    hdfs_resource_ignore_file="/var/lib/ambari-agent/data/.hdfs_resource_ignore",
    security_enabled=security_enabled,
    keytab=hdfs_user_keytab,
    kinit_path_local=kinit_path_local,
    hadoop_bin_dir=hadoop_bin_dir,
    hadoop_conf_dir=hadoop_conf_dir,
    principal_name=hdfs_principal_name,
    hdfs_site=hdfs_site,
    default_fs=default_fs,
    immutable_paths=get_not_managed_resources(),
    dfs_type=dfs_type
)
