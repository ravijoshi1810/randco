#!/usr/bin/python

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'none'}

from ansible.module_utils.basic import AnsibleModule
import json
import requests

def main():
    
    module = AnsibleModule(
        supports_check_mode = True,
        argument_spec = dict(
            tower_base_url = dict(type='str', required=True),
            tower_username = dict(type='str', required=True),
            tower_password = dict(type='str', required=True, no_log=True),
            tower_job_id = dict(type='int', required=True),
        ),
    )

    output = dict(
        changed=False,
        job_id=0,
    )

    tower_base_url = module.params['tower_base_url']
    tower_username = module.params['tower_username']
    tower_password = module.params['tower_password']
    tower_job_id = module.params['tower_job_id']

    response = requests.get(tower_base_url + '/api/v2/workflow_job_nodes/?job_id=' + str(tower_job_id), auth=requests.auth.HTTPBasicAuth(tower_username, tower_password), verify=False)
    worflow_job_node = response.json()['results'][0]['id']
    response = requests.get(tower_base_url + '/api/v2/workflow_job_nodes/?success_nodes=' + str(worflow_job_node), auth=requests.auth.HTTPBasicAuth(tower_username, tower_password), verify=False)
    output['job_id'] = response.json()['results'][0]['summary_fields']['job']['id']
    
    module.exit_json(**output)

if __name__ == '__main__':
    main()
