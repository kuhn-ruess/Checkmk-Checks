# Alertmanger Extended

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0-blue)
<!-- compatibility-badges:end -->
The Original Version of the Alertmanager Check in Checkmk, does not allow you to remap the severity. This Version of the Check, alows you to do that.
Also you can enable to get alerted based on the Severity and not only the firing state.




For users of Checkmk 2.3:

You need to delete the shipped Alertmanger from your Installation.
Use this Ansible Playbook as Example how:

```
---
- hosts: all
  gather_facts: false
  tasks:
     - name: "Delete Shipped Alertmanager Check "
       ansible.builtin.file:
          path: "{{ item }}"
          state: absent
       loop:
         - /opt/omd/versions/{{ cmk_version }}.cee/lib/python3/cmk/base/plugins/agent_based/alertmanager.py
         - /opt/omd/versions/{{ cmk_version }}.cee/lib/python3/cmk/plugins/collection/agent_based/alertmanager.py
         become: true
```
On 2.4 everthing will work out of the box



<img width="756" alt="image" src="https://github.com/user-attachments/assets/8940a048-9bd2-46a5-9197-10de29ed20f9" />
