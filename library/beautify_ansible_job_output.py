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
            tower_job_id = dict(type='str', required=True),
        ),
    )

    output = dict(
        changed=False,
        value='',
    )

    tower_base_url = module.params['tower_base_url']
    tower_username = module.params['tower_username']
    tower_password = module.params['tower_password']
    tower_job_id = module.params['tower_job_id']

    url = '/api/v2/jobs/' + tower_job_id + '/job_events'
    responses = []
    hosts = {}
    while True:
        response = requests.get(tower_base_url + url, auth=requests.auth.HTTPBasicAuth(tower_username, tower_password), verify=False)
        for result in response.json()['results']:
            if result['host_name'] != "":
                if result['changed']:
                    hosts.setdefault(result['host_name'],[]).append(result['task'])
        if response.json()['next'] == None:
            break
        url = response.json()['next']
    output['value'] = hosts
    module.exit_json(**output)

if __name__ == '__main__':
    main()
