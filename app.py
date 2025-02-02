import streamlit as st
from eth_account import Account
from web3 import Web3
import secrets
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime

# Multiple RPC endpoints for load balancing
RPC_ENDPOINTS = [
    'https://mainnet.infura.io/v3/6e34ed8d853f4abb83516b5a3a51df0c',
    'https://mainnet.infura.io/v3/6e34ed8d853f4abb83516b5a3a51df0c',
    'https://eth-mainnet.g.alchemy.com/v2/YOUR-KEY-3'
]

class WalletChecker:
    def __init__(self):
        self.w3_connections = [Web3(Web3.HTTPProvider(rpc)) for rpc in RPC_ENDPOINTS]
        self.found_wallets = []
        self.checked_count = 0
        self.running = False
    
    def check_rpc_connection(self):
        for i, w3 in enumerate(self.w3_connections):
            if w3.is_connected():
                st.success(f"RPC {i+1} Connected!")
            else:
                st.error(f"RPC {i+1} Failed!")

    def check_single_wallet(self):
        w3 = self.w3_connections[self.checked_count % len(self.w3_connections)]
        private_key = secrets.token_hex(32)
        account = Account.from_key(private_key)
        address = account.address
        
        try:
            balance = w3.eth.get_balance(address)
            balance_eth = w3.from_wei(balance, 'ether')
            
            if balance_eth > 0:
                wallet_info = {
                    'address': address,
                    'private_key': private_key,
                    'balance': balance_eth
                }
                self.found_wallets.append(wallet_info)
                return wallet_info
            return None
        except Exception as e:
            return None

    def brute_force_wallets(self, num_threads=50):
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            while self.running:
                if len(futures) < num_threads:
                    futures.append(executor.submit(self.check_single_wallet))
                
                for future in as_completed(futures[:]):
                    futures.remove(future)
                    self.checked_count += 1
                    if future.result():
                        yield future.result()

def main():
    st.set_page_config(page_title="ETH Wallet Brute Force", layout="wide")
    st.title("💰 Advanced ETH Wallet Checker")
    
    checker = WalletChecker()
    
    # RPC Connection Check
    if st.button("Check RPC Connections"):
        checker.check_rpc_connection()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        threads = st.number_input("Number of Threads", min_value=1, max_value=100, value=50)
    with col2:
        check_delay = st.number_input("Check Delay (ms)", min_value=0, max_value=1000, value=10)
    
    stats_placeholder = st.empty()
    found_placeholder = st.empty()
    
    if st.button("Start Brute Force"):
        checker.running = True
        start_time = time.time()
        
        try:
            for wallet in checker.brute_force_wallets(num_threads=threads):
                # Update stats
                elapsed_time = time.time() - start_time
                checks_per_second = checker.checked_count / elapsed_time
                
                stats_placeholder.metric(
                    label="Statistics",
                    value=f"Checked: {checker.checked_count:,}",
                    delta=f"Speed: {checks_per_second:.2f}/s"
                )
                
                # Display found wallet
                with found_placeholder.container():
                    st.success(f"💎 Found wallet with {wallet['balance']} ETH!")
                    st.code(f"""
                    Address: {wallet['address']}
                    Private Key: {wallet['private_key']}
                    Balance: {wallet['balance']} ETH
                    Found at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    """)
                    
                    # Export option
                    wallet_data = f"Address: {wallet['address']}\nPrivate Key: {wallet['private_key']}\nBalance: {wallet['balance']} ETH"
                    st.download_button(
                        label="Export Wallet Info",
                        data=wallet_data,
                        file_name=f"wallet_{wallet['address'][:8]}.txt"
                    )
                
                time.sleep(check_delay / 1000)  # Convert ms to seconds
                
        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
        finally:
            checker.running = False

if __name__ == "__main__":
    main()
