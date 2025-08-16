import os
os.environ["WATCHDOG_OBSERVER"] = "polling"  # Fix for inotify limit error

import streamlit as st
from jinja2 import Template

# -----------------------------
# Router configuration template
# -----------------------------
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

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Router Config Generator", page_icon="🖧", layout="centered")
st.title("🚀 Router Config Generator")

# Input fields
hostname = st.text_input("Hostname")
ip_address = st.text_input("IP Address")
subnet_mask = st.text_input("Subnet Mask")
network = st.text_input("OSPF Network")
vty_password = st.text_input("VTY Password", type="password")

# Generate button
if st.button("Generate Config"):
    if not (hostname and ip_address and subnet_mask and network and vty_password):
        st.warning("⚠️ Please fill in all fields.")
    else:
        # Render template
        template = Template(config_template)
        config = template.render(
            hostname=hostname,
            ip_address=ip_address,
            subnet_mask=subnet_mask,
            network=network,
            vty_password=vty_password
        )
        
        # Display config
        st.subheader("Generated Router Configuration")
        st.code(config, language="cisco")
        
        # Download button
        st.download_button(
            label="📥 Download Config as .txt",
            data=config,
            file_name=f"{hostname}_config.txt",
            mime="text/plain"
        )
