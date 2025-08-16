import os
os.environ["WATCHDOG_OBSERVER"] = "polling"  # Fix for inotify limit error

import streamlit as st
from jinja2 import Template

# Router config template
config_template = """
hostname {{ hostname }}
!
interface GigabitEthernet0/0
    ip address {{ ip_address }} {{ subnet_mask }}
!
router ospf 1
    network {{ network }} area 0
!
line vty 0 4
    password {{ vty_password }}
    login
!
end
"""

# Streamlit UI
st.title("🚀 Router Config Generator")

hostname = st.text_input("Hostname")
ip_address = st.text_input("IP Address")
subnet_mask = st.text_input("Subnet Mask")
network = st.text_input("OSPF Network")
vty_password = st.text_input("VTY Password")

if st.button("Generate Config"):
    template = Template(config_template)
    config = template.render(
        hostname=hostname,
        ip_address=ip_address,
        subnet_mask=subnet_mask,
        network=network,
        vty_password=vty_password
    )
    
    # Show config in browser
    st.code(config, language="cisco")
    
    # Download as .txt
    st.download_button(
        label="Download Config",
        data=config,
        file_name=f"{hostname}_config.txt",
        mime="text/plain"
    )
