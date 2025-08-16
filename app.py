# -------------------------
# Polling fix for Streamlit
# -------------------------
import os
os.environ["WATCHDOG_OBSERVER"] = "polling"
os.environ["STREAMLIT_WATCHDOG"] = "polling"

# -------------------------
# Imports
# -------------------------
import streamlit as st
from jinja2 import Template

# -------------------------
# Router configuration template
# -------------------------
config_template = """
hostname {{ hostname }}
!
interface {{ interface }}
 ip address {{ ip_address }} {{ subnet_mask }}
 no shutdown
!
ip route {{ network }} {{ subnet_mask }} {{ gateway }}
!
line vty 0 4
 password {{ vty_password }}
 login
!
"""

# -------------------------
# Streamlit App
# -------------------------
st.title("Router Configuration Generator")

# Input fields
hostname = st.text_input("Router Hostname", "Router1")
interface = st.text_input("Interface", "GigabitEthernet0/0")
ip_address = st.text_input("IP Address", "192.168.1.1")
subnet_mask = st.text_input("Subnet Mask", "255.255.255.0")
network = st.text_input("Network", "0.0.0.0")
gateway = st.text_input("Default Gateway", "192.168.1.254")
vty_password = st.text_input("VTY Password", "cisco", type="password")

# Generate configuration
if st.button("Generate Configuration"):
    template = Template(config_template)
    config = template.render(
        hostname=hostname,
        interface=interface,
        ip_address=ip_address,
        subnet_mask=subnet_mask,
        network=network,
        gateway=gateway,
        vty_password=vty_password
    )
    
    st.code(config, language="cisco")
    
    # Allow download as .txt file
    st.download_button(
        label="Download Config",
        data=config,
        file_name=f"{hostname}_config.txt",
        mime="text/plain"
    )
