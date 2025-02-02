import streamlit as st
from cryptofuzz import Ethereum
from random import choice as c
import time

def mHash():
    """ Generated random hash without repetition (default size: 64) """
    return ''.join(c('0123456789abcdef') for _ in range(64))

def main():
    st.title("Ethereum Rich Wallet Finder")
    st.markdown("""
    ### Welcome to the Ethereum Wallet Scanner
    Upload a text file containing Ethereum addresses to scan
    """)
    
    uploaded_file = st.file_uploader("Choose a file with Ethereum addresses", type="txt")
    
    if uploaded_file:
        addresses = set(uploaded_file.getvalue().decode().split())
        
        if st.button("Start Scanning"):
            eth = Ethereum()
            scan_count = st.empty()
            address_display = st.empty()
            found_addresses = st.container()
            
            counter = 1
            while True:
                hex64 = mHash()
                priv = hex64
                addr = eth.hex_addr(priv)
                
                scan_count.text(f"Total Scans: {counter}")
                address_display.text(f"Current Address: {addr}")
                
                if addr in addresses:
                    with found_addresses:
                        st.success(f"""
                        Found Match!
                        Address: {addr}
                        Private Key: {priv}
                        """)
                        
                        with open("EthereumRichWinnerWallet.txt", "a") as f:
                            f.write(f'\nAddress = {addr}')
                            f.write(f'\nPrivate Key = {priv}')
                            f.write('\n=========================================================\n')
                
                counter += 1
                time.sleep(0.1)

if __name__ == "__main__":
    main()
