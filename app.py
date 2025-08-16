import os
os.environ["WATCHDOG_OBSERVER"] = "polling"  # Fix for inotify limit error

import streamlit as st
from jinja2 import Template

# -----------------------------
# Router configuration template
# -----------------------------
config_template = """
version 17.6
service timestamps debug datetime msec localtime
service timestamps log datetime msec localtime
service password-encryption
!
hostname {{ hostname }}
!
vrf definition MANAGEMENT
 rd {{ vrf_management_rd }}
 address-family ipv4
  route-target export {{ vrf_management_rt_export }}
  route-target import {{ vrf_management_rt_import }}
 exit-address-family
!
vrf definition Mgmt-intf
!
interface Loopback0
 description *** LOOPBACK 0 ***
 ip address {{ loopback0_ip }} 255.255.255.255
!
interface Loopback100
 description *** LOOPBACK 100 ***
 vrf forwarding MANAGEMENT
 ip address {{ loopback100_ip }} 255.255.255.255
!
interface GigabitEthernet0/2/0
 description {{ gi0_2_0_desc }}
 ip address {{ gi0_2_0_ip }} 255.255.255.252
 no ip proxy-arp
 no shutdown
!
interface GigabitEthernet0/3/0
 description {{ gi0_3_0_desc }}
 ip address {{ gi0_3_0_ip }} 255.255.255.252
 no ip proxy-arp
 shutdown
!
"""

st.title("Router Config Generator")

# Input fields for router variables
hostname = st.text_input("Hostname", "614-ACCESS-01")

loopback0_ip = st.text_input("Loopback0 IP", "10.101.1.199")
loopback100_ip = st.text_input("Loopback100 IP", "10.101.1.199")

vrf_management_rd = st.text_input("VRF MANAGEMENT RD", "10.101.1.199:120")
vrf_management_rt_export = st.text_input("VRF MANAGEMENT Route-Target Export", "64512:120")
vrf_management_rt_import = st.text_input("VRF MANAGEMENT Route-Target Import", "64512:120")

gi0_2_0_desc = st.text_input("Gi0/2/0 Description", "*** 614-ACCESS-01 <-> 616-ACCESS-01 ***")
gi0_2_0_ip = st.text_input("Gi0/2/0 IP", "10.101.45.61")

gi0_3_0_desc = st.text_input("Gi0/3/0 Description", "*** 614-ACCESS-01 <-> 385-CORE-01 ***")
gi0_3_0_ip = st.text_input("Gi0/3/0 IP", "10.101.0.1")

# Generate config
if st.button("Generate Config"):
    template = Template(config_template)
    config = template.render(
        hostname=hostname,
        loopback0_ip=loopback0_ip,
        loopback100_ip=loopback100_ip,
        vrf_management_rd=vrf_management_rd,
        vrf_management_rt_export=vrf_management_rt_export,
        vrf_management_rt_import=vrf_management_rt_import,
        gi0_2_0_desc=gi0_2_0_desc,
        gi0_2_0_ip=gi0_2_0_ip,
        gi0_3_0_desc=gi0_3_0_desc,
        gi0_3_0_ip=gi0_3_0_ip
    )

    st.text_area("Generated Config", config, height=400)
    st.download_button("Download Config", config, file_name=f"{hostname}_config.txt")
