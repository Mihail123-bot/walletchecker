import streamlit as st
from eth_account import Account
from solana.keypair import Keypair
import base58
from web3 import Web3
import secrets

def generate_eth_wallet():
    # Generate random private key
    private_key = secrets.token_hex(32)
    account = Account.from_key(private_key)
    return {
        'address': account.address,
        'private_key': private_key
    }

def generate_solana_wallet():
    # Generate Solana keypair
    keypair = Keypair()
    return {
        'address': str(keypair.public_key),
        'private_key': base58.b58encode(keypair.secret_key).decode('ascii')
    }

def main():
    st.set_page_config(page_title="Crypto Wallet Generator", layout="wide")
    
    st.title("🔐 Cryptocurrency Wallet Generator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Ethereum Wallet")
        if st.button("Generate ETH Wallet"):
            eth_wallet = generate_eth_wallet()
            st.success("Ethereum Wallet Generated!")
            st.code(f"Address: {eth_wallet['address']}")
            st.code(f"Private Key: {eth_wallet['private_key']}")
            
            # Add balance check
            w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/6e34ed8d853f4abb83516b5a3a51df0c'))
            balance = w3.eth.get_balance(eth_wallet['address'])
            eth_balance = w3.from_wei(balance, 'ether')
            st.metric("ETH Balance", f"{eth_balance:.4f} ETH")
    
    with col2:
        st.header("Solana Wallet")
        if st.button("Generate SOL Wallet"):
            sol_wallet = generate_solana_wallet()
            st.success("Solana Wallet Generated!")
            st.code(f"Address: {sol_wallet['address']}")
            st.code(f"Private Key: {sol_wallet['private_key']}")
            
    # Security Notice
    st.markdown("---")
    st.warning("""
    🔒 **Security Notice:**
    - Store your private keys securely
    - Never share private keys
    - Keep a backup of your wallet information
    """)
    
    # Additional Features
    st.markdown("---")
    st.header("Bulk Generation")
    num_wallets = st.slider("Number of wallets to generate", 1, 100, 1)
    
    if st.button("Generate Multiple Wallets"):
        st.write("### Generated Wallets")
        
        for i in range(num_wallets):
            st.write(f"### Wallet Set {i+1}")
            eth = generate_eth_wallet()
            sol = generate_solana_wallet()
            
            col3, col4 = st.columns(2)
            with col3:
                st.write("**Ethereum**")
                st.code(f"Address: {eth['address']}\nPrivate Key: {eth['private_key']}")
            
            with col4:
                st.write("**Solana**")
                st.code(f"Address: {sol['address']}\nPrivate Key: {sol['private_key']}")

if __name__ == "__main__":
    main()
