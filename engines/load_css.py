import streamlit as st

def load_css():
    """Load the mobile-responsive CSS file"""
    
    with open('style.css', 'r') as f:
        css = f.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)