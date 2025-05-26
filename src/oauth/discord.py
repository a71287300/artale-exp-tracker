import streamlit as st
from streamlit_oauth import OAuth2Component
import os
from dotenv import load_dotenv
load_dotenv()

AUTHORIZE_URL = os.environ.get('DISCORD_AUTHORIZE_URL')
TOKEN_URL = os.environ.get('DISCORD_TOKEN_URL')
REFRESH_TOKEN_URL = os.environ.get('DISCORD_REFRESH_TOKEN_URL')
REVOKE_TOKEN_URL = os.environ.get('DISCORD_REVOKE_TOKEN_URL')
CLIENT_ID = os.environ.get('DISCORD_CLIENT_ID')
CLIENT_SECRET = os.environ.get('DISCORD_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('DISCORD_REDIRECT_URI')
SCOPE = os.environ.get('DISCORD_SCOPE', 'identify email')

oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)

def discord_oauth_login():
    if 'discord_token' not in st.session_state:
        result = oauth2.authorize_button("Discord 登入", REDIRECT_URI, SCOPE)
        if result and 'token' in result:
            st.session_state.discord_token = result.get('token')
            st.rerun()
        return None
    else:
        token = st.session_state['discord_token']
        # 取得 Discord user info
        import requests
        headers = {"Authorization": f"Bearer {token['access_token']}"}
        resp = requests.get("https://discord.com/api/users/@me", headers=headers)
        if resp.status_code == 200:
            return resp.json()
        return None