"""
DB 연결 정보 관리 페이지 — 입력, 조회, 수정, 삭제
"""
import streamlit as st
from connection_store import (
    list_connections,
    get_connection,
    save_connection,
    delete_connection,
    test_connection,
)

st.set_page_config(page_title="연결 관리", page_icon="🔌", layout="wide")
st.title("🔌 데이터베이스 연결 관리")

# ── 새 연결 추가 / 수정 폼 ────────────────────────────────────
st.subheader("연결 추가 / 수정")

# 기존 연결 선택 시 폼에 채워넣기
existing = list_connections()
edit_target = st.selectbox(
    "기존 연결 불러오기 (수정용)",
    ["-- 새 연결 --"] + existing,
    key="edit_target",
)

defaults = {"host": "", "port": 5432, "database": "", "user": "postgres", "password": ""}
edit_name = ""
if edit_target != "-- 새 연결 --":
    info = get_connection(edit_target)
    if info:
        defaults = info
        edit_name = edit_target

with st.form("conn_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("연결 이름", value=edit_name)
        host = st.text_input("호스트", value=defaults.get("host", ""))
        port = st.number_input("포트", value=int(defaults.get("port", 5432)), min_value=1, max_value=65535)
    with col2:
        database = st.text_input("데이터베이스", value=defaults.get("database", ""))
        user = st.text_input("사용자", value=defaults.get("user", "postgres"))
        password = st.text_input("비밀번호", value=defaults.get("password", ""), type="password")

    col_save, col_test, col_del = st.columns(3)
    with col_save:
        submitted = st.form_submit_button("💾 저장", use_container_width=True)
    with col_test:
        test_btn = st.form_submit_button("🔍 연결 테스트", use_container_width=True)
    with col_del:
        delete_btn = st.form_submit_button("🗑️ 삭제", use_container_width=True, type="secondary")

if submitted:
    if not name.strip():
        st.error("연결 이름을 입력하세요.")
    elif not host.strip():
        st.error("호스트를 입력하세요.")
    elif not database.strip():
        st.error("데이터베이스 이름을 입력하세요.")
    else:
        save_connection(name.strip(), host.strip(), int(port), database.strip(), user.strip(), password)
        st.success(f"'{name}' 저장 완료")
        st.rerun()

if test_btn:
    if not name.strip():
        st.error("연결 이름을 입력하세요.")
    else:
        # 임시 저장 후 테스트
        save_connection(name.strip(), host.strip(), int(port), database.strip(), user.strip(), password)
        ok, msg = test_connection(name.strip())
        if ok:
            st.success(f"✅ {msg}")
        else:
            st.error(f"❌ {msg}")

if delete_btn:
    if not name.strip():
        st.error("삭제할 연결 이름을 입력하세요.")
    elif delete_connection(name.strip()):
        st.success(f"'{name}' 삭제 완료")
        st.rerun()
    else:
        st.warning(f"'{name}' 연결을 찾을 수 없습니다.")

# ── 등록된 연결 목록 ──────────────────────────────────────────
st.divider()
st.subheader("등록된 연결 목록")

connections = list_connections()
if not connections:
    st.info("등록된 연결이 없습니다. 위 폼에서 추가하세요.")
else:
    for conn_name in connections:
        info = get_connection(conn_name)
        with st.expander(f"🗄️ {conn_name}", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.text(f"호스트: {info['host']}")
                st.text(f"포트: {info['port']}")
            with col2:
                st.text(f"DB: {info['database']}")
                st.text(f"사용자: {info['user']}")
            with col3:
                st.text(f"비밀번호: {'●' * min(len(info.get('password', '')), 8)}")
                if st.button("🔍 테스트", key=f"test_{conn_name}"):
                    ok, msg = test_connection(conn_name)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)
