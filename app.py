import streamlit as st
from eth_account import Account
from web3 import Web3
import secrets

def generate_eth_wallet():
    private_key = secrets.token_hex(32)
    account = Account.from_key(private_key)
    return {
        'address': account.address,
        'private_key': private_key
    }

def main():
    st.set_page_config(page_title="Ethereum Wallet Generator", layout="wide")
    
    st.title("🔐 Ethereum Wallet Generator")
    
    if st.button("Generate ETH Wallet"):
        eth_wallet = generate_eth_wallet()
        st.success("Ethereum Wallet Generated!")
        st.code(f"Address: {eth_wallet['address']}")
        st.code(f"Private Key: {eth_wallet['private_key']}")
        
        # Add balance check
        w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR-INFURA-KEY'))
        balance = w3.eth.get_balance(eth_wallet['address'])
        eth_balance = w3.from_wei(balance, 'ether')
        st.metric("ETH Balance", f"{eth_balance:.4f} ETH")
    
    # Bulk Generation
    st.markdown("---")
    st.header("Bulk Generation")
    num_wallets = st.slider("Number of wallets to generate", 1, 100, 1)
    
    if st.button("Generate Multiple Wallets"):
        st.write("### Generated Wallets")
        
        for i in range(num_wallets):
            st.write(f"### Wallet Set {i+1}")
            eth = generate_eth_wallet()
            st.code(f"Address: {eth['address']}\nPrivate Key: {eth['private_key']}")

if __name__ == "__main__":
    main()
