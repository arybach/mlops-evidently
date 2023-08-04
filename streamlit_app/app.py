import os
from typing import Text

import requests
import streamlit as st

from streamlit_app.utils.ui import (
    set_page_container_style,
    display_sidebar_header,
    display_header,
    display_report
)


if __name__ == '__main__':
    # Configure some styles
    set_page_container_style()
    # Sidebar: Logo and links
    display_sidebar_header()

    # Get the SSL certificate and key paths from environment variables
    ssl_cert_path = os.getenv("SSL_CERT_PATH")
    ssl_key_path = os.getenv("SSL_KEY_PATH")

    # Check if SSL certificates and keys are available
    # use_https = ssl_cert_path is not None and ssl_key_path is not None
    # scheme = "https" if use_https else "http"
    # use http as ec2 instance is not configured with ssl and streamlit on public ip will error out
    scheme = "http"
    host: Text = os.getenv('FASTAPI_APP_HOST', 'localhost')
    base_route: Text = f'{scheme}://{host}:8501'

    try:
        window_size: int = st.sidebar.number_input(
            label='window_size',
            min_value=1,
            step=1,
            value=3000
        )

        model_name: Text = st.sidebar.text_input(
            label='Model Name',
            value='xgboost_model'  # Provide a default value or use st.selectbox to let the user choose
        )

        clicked_model_performance: bool = st.sidebar.button(
            label='Model performance'
        )
        clicked_target_drift: bool = st.sidebar.button(label='Target drift')

        report_selected: bool = False
        request_url: Text = base_route

        if clicked_model_performance:
            report_selected = True
            request_url += f'/monitor-model/{model_name}?window_size={window_size}'

        if clicked_target_drift:
            report_selected = True
            request_url += f'/monitor-target/{model_name}?window_size={window_size}'

        if report_selected:
            resp: requests.Response = requests.get(request_url)
            report_name = 'Model Performance' if clicked_model_performance else 'Target Drift'
            display_header(report_name, window_size)
            display_report(resp.content)

    except Exception as e:
        st.error(e)
