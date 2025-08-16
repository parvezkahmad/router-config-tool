import os
os.environ["WATCHDOG_OBSERVER"] = "polling"  # Fix for inotify limit error

import streamlit as st
from jinja2 import Template

st.set_page_config(page_title="Router Config Generator", layout="wide")
st.title("Full Router Configuration Generator")

# -----------------------------
# Router configuration template
# -----------------------------
config_template = """
version {{ version }}
service timestamps debug datetime msec localtime
service timestamps log datetime msec localtime
service password-encryption
hostname {{ hostname }}
!
{% for lb in loopbacks %}
interface {{ lb.name }}
 description {{ lb.description }}
 {% if lb.vrf %}vrf forwarding {{ lb.vrf }}{% endif %}
 ip address {{ lb.ip }} {{ lb.mask }}
 {% if lb.ospf_process %}ip ospf {{ lb.ospf_process }} area {{ lb.ospf_area }}{% endif %}
 no shutdown
!
{% endfor %}

{% for ge in gigabit_interfaces %}
interface {{ ge.name }}
 description {{ ge.description }}
 mtu {{ ge.mtu }}
 {% if ge.ip %}ip address {{ ge.ip }} {{ ge.mask }}{% else %}no ip address{% endif %}
 ip ospf message-digest-key {{ ge.ospf_key }} md5 0 {{ ge.ospf_password }}
 ip ospf network point-to-point
 {% if ge.ospf_bfd %}ip ospf bfd{% endif %}
 {% if ge.ospf_process %}ip ospf {{ ge.ospf_process }} area {{ ge.ospf_area }}{% endif %}
 load-interval {{ ge.load_interval }}
 negotiation auto
 synchronous mode
 bfd template {{ ge.bfd_template }}
 no ip redirects
 no ip unreachables
 cdp enable
 service-policy input {{ ge.policy_in }}
 service-policy output {{ ge.policy_out }}
 {% if ge.shutdown %}shutdown{% else %}no shutdown{% endif %}
!
{% endfor %}

{% for policy in policies %}
policy-map {{ policy.name }}
{% for cls in policy.classes %}
 class {{ cls.name }}
  set dscp {{ cls.dscp }}
  set qos-group {{ cls.qos_group }}
{% endfor %}
!
{% endfor %}
"""

# -----------------------------
# Prepopulated Values from Your Full Config
# -----------------------------
version = "17.6"
hostname = "614-ACCESS-01"

loopbacks = [
    {"name": "Loopback0", "description": "*** LOOPBACK 0 ***", "vrf": None, "ip": "10.101.1.199", "mask": "255.255.255.255", "ospf_process": "100", "ospf_area": "34"},
    {"name": "Loopback100", "description": "*** LOOPBACK 100 ***", "vrf": "MANAGEMENT", "ip": "10.101.1.199", "mask": "255.255.255.255", "ospf_process": None, "ospf_area": None},
]

# All Gigabit interfaces you provided
gigabit_interfaces = [
    {"name": "GigabitEthernet0/2/0", "description": "*** 614-ACCESS-01 <-> 616-ACCESS-01 ***", "mtu": "9000", "ip": "10.101.45.61", "mask": "255.255.255.252", "ospf_key": "1", "ospf_password": "K4Hr4mm44!", "ospf_process": "100", "ospf_area": "34", "ospf_bfd": True, "load_interval": "30", "bfd_template": "bfdtemplate1", "policy_in": "BB-IN", "policy_out": "BB-OUT", "shutdown": False},
    {"name": "GigabitEthernet0/2/1", "description": "*** NOT IN USE ***", "mtu": "9000", "ip": None, "mask": None, "ospf_key": "1", "ospf_password": "K4Hr4mm44!", "ospf_process": "100", "ospf_area": "34", "ospf_bfd": True, "load_interval": "30", "bfd_template": "bfdtemplate1", "policy_in": "BB-IN", "policy_out": "BB-OUT", "shutdown": True},
    {"name": "GigabitEthernet0/2/2", "description": "*** NOT IN USE ***", "mtu": "9000", "ip": None, "mask": None, "ospf_key": "1", "ospf_password": "K4Hr4mm44!", "ospf_process": "100", "ospf_area": "34", "ospf_bfd": True, "load_interval": "30", "bfd_template": "bfdtemplate1", "policy_in": "BB-IN", "policy_out": "BB-OUT", "shutdown": True},
    {"name": "GigabitEthernet0/2/3", "description": "*** NOT IN USE ***", "mtu": "9000", "ip": None, "mask": None, "ospf_key": "1", "ospf_password": "K4Hr4mm44!", "ospf_process": "100", "ospf_area": "34", "ospf_bfd": True, "load_interval": "30", "bfd_template": "bfdtemplate1", "policy_in": "BB-IN", "policy_out": "BB-OUT", "shutdown": True},
    {"name": "GigabitEthernet0/2/4", "description": "*** NOT IN USE ***", "mtu": "9000", "ip": None, "mask": None, "ospf_key": "1", "ospf_password": "K4Hr4mm44!", "ospf_process": "100", "ospf_area": "34", "ospf_bfd": True, "load_interval": "30", "bfd_template": "bfdtemplate1", "policy_in": "BB-IN", "policy_out": "BB-OUT", "shutdown": True},
    {"name": "GigabitEthernet0/2/5", "description": "*** NOT IN USE ***", "mtu": "9000", "ip": None, "mask": None, "ospf_key": "1", "ospf_password": "K4Hr4mm44!", "ospf_process": "100", "ospf_area": "34", "ospf_bfd": True, "load_interval": "30", "bfd_template": "bfdtemplate1", "policy_in": "BB-IN", "policy_out": "BB-OUT", "shutdown": True},
    {"name": "GigabitEthernet0/2/6", "description": "*** NOT IN USE ***", "mtu": "9000", "ip": None, "mask": None, "ospf_key": "1", "ospf_password": "K4Hr4mm44!", "ospf_process": None, "ospf_area": None, "ospf_bfd": True, "load_interval": "30", "bfd_template": "bfdtemplate1", "policy_in": "BB-IN", "policy_out": "BB-OUT", "shutdown": True},
    {"name": "GigabitEthernet0/2/7", "description": "*** NOT IN USE ***", "mtu": "9000", "ip": None, "mask": None, "ospf_key": "1", "ospf_password": "K4Hr4mm44!", "ospf_process": None, "ospf_area": None, "ospf_bfd": True, "load_interval": "30", "bfd_template": "bfdtemplate1", "policy_in": "BB-IN", "policy_out": "BB-OUT", "shutdown": True},
    {"name": "GigabitEthernet0/3/0", "description": "*** 614-ACCESS-01 <-> 385-CORE-01 ***", "mtu": "9000", "ip": None, "mask": None, "ospf_key": "1", "ospf_password": "K4Hr4mm44!", "ospf_process": "100", "ospf_area": "34", "ospf_bfd": True, "load_interval": "30", "bfd_template": "bfdtemplate1", "policy_in": "BB-IN", "policy_out": "BB-OUT", "shutdown": True},
]

# Sample policies (add more if needed)
policies = [
    {"name": "LAN-IN", "classes": [
        {"name": "SCADA_DCC", "dscp": "cs7", "qos_group": "7"},
        {"name": "SCADA_NCC", "dscp": "cs7", "qos_group": "7"},
        {"name": "MANAGEMENT", "dscp": "cs6", "qos_group": "6"},
        {"name": "VOIP", "dscp": "ef", "qos_group": "5"},
        {"name": "WAMS", "dscp": "cs6", "qos_group": "6"},
        {"name": "CCTV", "dscp": "cs1", "qos_group": "1"},
        {"name": "RAP", "dscp": "af32", "qos_group": "3"},
        {"name": "PMR", "dscp": "af22", "qos_group": "2"},
        {"name": "CMS", "dscp": "af42", "qos_group": "4"},
    ]}
]

# -----------------------------
# Generate Config Button
# -----------------------------
if st.button("Generate Router Config"):
    template = Template(config_template)
    rendered_config = template.render(
        version=version,
        hostname=hostname,
        loopbacks=loopbacks,
        gigabit_interfaces=gigabit_interfaces,
        policies=policies
    )
    st.subheader("Generated Router Configuration")
    st.code(rendered_config, language="text")

    st.download_button("Download Config", rendered_config, file_name=f"{hostname}_config.txt")
