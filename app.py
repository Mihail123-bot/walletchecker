import streamlit as st
from eth_account import Account
from web3 import Web3
import secrets
import time

def check_wallet_balance(address, w3):
    try:
        balance = w3.eth.get_balance(address)
        return w3.from_wei(balance, 'ether')
    except:
        return 0

def generate_and_check_wallets():
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR-INFURA-KEY'))
    found_wallets = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    num_checks = st.session_state.get('num_checks', 1000)
    
    for i in range(num_checks):
        private_key = secrets.token_hex(32)
        account = Account.from_key(private_key)
        address = account.address
        
        balance = check_wallet_balance(address, w3)
        
        if balance > 0:
            found_wallets.append({
                'address': address,
                'private_key': private_key,
                'balance': balance
            })
            st.success(f"Found wallet with balance: {balance} ETH!")
            
        progress = (i + 1) / num_checks
        progress_bar.progress(progress)
        status_text.text(f"Checked {i + 1}/{num_checks} wallets. Found: {len(found_wallets)}")
        
    return found_wallets

def main():
    st.set_page_config(page_title="ETH Wallet Checker", layout="wide")
    
    st.title("💰 Ethereum Wallet Balance Checker")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input("Number of wallets to check", 
                       min_value=100, 
                       max_value=100000, 
                       value=1000,
                       key='num_checks')
    
    if st.button("Start Checking"):
        found_wallets = generate_and_check_wallets()
        
        if found_wallets:
            st.header("🎯 Found Wallets with Balance")
            for wallet in found_wallets:
                st.write("---")
                st.code(f"""
                Address: {wallet['address']}
                Private Key: {wallet['private_key']}
                Balance: {wallet['balance']} ETH
                """)
                
                # Export option
                wallet_data = f"Address: {wallet['address']}\nPrivate Key: {wallet['private_key']}\nBalance: {wallet['balance']} ETH"
                st.download_button(
                    label="Export Wallet Info",
                    data=wallet_data,
                    file_name=f"wallet_{wallet['address'][:8]}.txt"
                )
        else:
            st.info("No wallets with balance found in this batch.")
    
    st.markdown("---")
    st.markdown("""
    #### Features:
    - Checks random Ethereum addresses for balances
    - Generates private keys for found wallets
    - Real-time progress tracking
    - Export wallet information
    """)

if __name__ == "__main__":
    main()
