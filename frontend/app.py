"""Streamlit Dashboard for Exercise 02.

Consumes the Node Registry API. Configuration:
- `API_URL` environment variable (default: http://localhost:8080)

Features:
- List nodes (GET /api/nodes)
- Register node (POST /api/nodes)
- Delete node (DELETE /api/nodes/{name})
- Health status (GET /health)
"""

import os
from typing import Any, Dict, List

import pandas as pd
import requests
import streamlit as st
from requests.exceptions import RequestException

API_URL = os.getenv("API_URL", "http://localhost:8080")

st.set_page_config(page_title="Nodes Dashboard", layout="wide")


def safe_rerun():
    if hasattr(st, "experimental_rerun"):
        try:
            st.experimental_rerun()
        except Exception:
            st.session_state["_rerun"] = st.session_state.get("_rerun", 0) + 1
    else:
        st.session_state["_rerun"] = st.session_state.get("_rerun", 0) + 1


if "_rerun" not in st.session_state:
    st.session_state["_rerun"] = 0


def get_health() -> (bool, Any):
    try:
        r = requests.get(f"{API_URL}/health", timeout=4)
        r.raise_for_status()
        # try to return json, fallback to text
        try:
            return True, r.json()
        except Exception:
            return True, r.text
    except RequestException as e:
        return False, str(e)


def get_nodes() -> List[Dict[str, Any]]:
    try:
        r = requests.get(f"{API_URL}/api/nodes", timeout=4)
        r.raise_for_status()
        return r.json()
    except RequestException:
        return []


def register_node(name: str, host: str, port: int) -> (bool, Any):
    payload = {"name": name, "host": host, "port": int(port)}
    try:
        r = requests.post(f"{API_URL}/api/nodes", json=payload, timeout=5)
        r.raise_for_status()
        try:
            return True, r.json()
        except Exception:
            return True, r.text
    except RequestException as e:
        return False, str(e)


def delete_node(name: str) -> (bool, Any):
    try:
        r = requests.delete(f"{API_URL}/api/nodes/{name}", timeout=5)
        if r.status_code in (200, 204):
            return True, "deleted"
        return False, r.text
    except RequestException as e:
        return False, str(e)


def render_sidebar():
    st.sidebar.title("Health & Controls")
    healthy, info = get_health()
    st.sidebar.markdown("**API reachable:** " + ("✅" if healthy else "❌"))
    if healthy:
        try:
            st.sidebar.json(info)
        except Exception:
            st.sidebar.text(str(info))

    st.sidebar.button("Refresh", on_click=safe_rerun)


def main():
    render_sidebar()

    st.title("Nodes Dashboard")

    nodes = get_nodes()

    left, right = st.columns([2, 1])

    with left:
        st.header("Registered Nodes")
        if not nodes:
            st.info("No nodes available or API not reachable.")
        else:
            df = pd.DataFrame(nodes)
            # normalize columns order if available
            cols = [
                c
                for c in (
                    "id",
                    "name",
                    "host",
                    "port",
                    "status",
                    "created_at",
                    "updated_at",
                )
                if c in df.columns
            ]
            if cols:
                st.dataframe(df[cols])
            else:
                st.dataframe(df)

    with right:
        st.header("Register Node")
        with st.form("register_form"):
            name = st.text_input("Name")
            host = st.text_input("Host (hostname or IP)")
            port = st.number_input("Port", min_value=1, max_value=65535, value=8080)
            submitted = st.form_submit_button("Register")
            if submitted:
                if not name or not host:
                    st.error("Name and host are required.")
                else:
                    ok, resp = register_node(name, host, port)
                    if ok:
                        st.success("Node registered")
                        safe_rerun()
                    else:
                        st.error(f"Failed to register: {resp}")

        st.markdown("---")
        st.header("Delete Node")
        names = [n.get("name") for n in nodes] if nodes else []
        if names:
            to_delete = st.selectbox("Select node to delete", names)
            if st.button("Delete"):
                ok, msg = delete_node(to_delete)
                if ok:
                    st.success("Node deleted")
                    safe_rerun()
                else:
                    st.error(f"Delete failed: {msg}")
        else:
            st.info("No nodes to delete.")


if __name__ == "__main__":
    main()
