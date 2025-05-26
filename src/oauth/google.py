import streamlit as st
from streamlit_oauth import OAuth2Component
import os
from dotenv import load_dotenv
load_dotenv()

AUTHORIZE_URL = os.environ.get('GOOGLE_AUTHORIZE_URL')
TOKEN_URL = os.environ.get('GOOGLE_TOKEN_URL')
REFRESH_TOKEN_URL = os.environ.get('GOOGLE_REFRESH_TOKEN_URL')
REVOKE_TOKEN_URL = os.environ.get('GOOGLE_REVOKE_TOKEN_URL')
CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI')
SCOPE = os.environ.get('GOOGLE_SCOPE', 'openid email profile')

oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)

def google_oauth_login():
    if 'google_token' not in st.session_state:
        result = oauth2.authorize_button("Google 登入", REDIRECT_URI, SCOPE)
        if result and 'token' in result:
            st.session_state.google_token = result.get('token')
            st.rerun()
        return None
    else:
        token = st.session_state['google_token']
        # 這裡可根據 token 取得 user info
        id_token = token.get('id_token')
        import jwt
        user_info = jwt.decode(id_token, options={"verify_signature": False})
        return user_info
