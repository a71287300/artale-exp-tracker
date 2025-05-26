import streamlit as st
import time
import cv2
import json
import os
from database import Database
from window_utils import get_window, get_experience_region, get_active_windows, bring_window_to_front
from screenshot import capture_screenshot
from ocr import extract_experience
from utils import calculate_experience_per_minute
from oauth.google import google_oauth_login
from oauth.discord import discord_oauth_login
from extra_streamlit_components import CookieManager

db = Database()
cookie_manager = CookieManager()

def oauth_login():
    st.title("Artale經驗值追蹤器")
    st.write("請選擇登入方式：")
    user_info = None
    provider = None

    if 'google_token' in st.session_state:
        user_info = google_oauth_login()
        provider = 'google'
    elif 'discord_token' in st.session_state:
        user_info = discord_oauth_login()
        provider = 'discord'

    if user_info:
        if st.button("登出"):
            if provider == 'google':
                st.session_state.pop('google_token', None)
            elif provider == 'discord':
                st.session_state.pop('discord_token', None)
            st.rerun()
        return user_info
    else:
        google_oauth_login()
        discord_oauth_login()
        return None

def main():
    user_info = oauth_login()
    if not user_info:
        st.stop()

    # 取得唯一 user_id
    if "email" in user_info:
        user_id = user_info["email"]
        user_name = user_info.get("name", user_info["email"])
    elif "id" in user_info:
        user_id = user_info["id"]
        user_name = user_info.get("username", user_info["id"])
    else:
        st.error("無法取得使用者資訊")
        st.stop()

    st.success(f"歡迎, {user_name}")

    if 'window' not in st.session_state:
        st.session_state.window = None
    if 'region' not in st.session_state:
        st.session_state.region = None
    if 'final_results' not in st.session_state:
        st.session_state.final_results = None
    if 'is_paused' not in st.session_state:
        st.session_state.is_paused = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'pause_time' not in st.session_state:
        st.session_state.pause_time = 0

    window_titles = get_active_windows()
    default_window = "MapleStory Worlds-Artale (繁體中文版)"
    if 'window_name' not in st.session_state:
        if default_window in window_titles:
            st.session_state.window_name = default_window
        else:
            st.session_state.window_name = window_titles[0] if window_titles else None

    window_name = st.selectbox(
        "選擇遊戲視窗:",
        window_titles,
        index=window_titles.index(st.session_state.window_name) if st.session_state.window_name in window_titles else 0
    )
    if st.button("選擇視窗"):
        st.session_state.window_name = window_name
        st.session_state.window = get_window(window_name)
        if st.session_state.window:
            st.success(f"已選擇視窗: {window_name}")
        else:
            st.error("找不到視窗，請檢查名稱。")

    if st.session_state.window:
        # region 設定預設值
        default_region = {
            "x": 53,
            "y": 93,
            "w": 13,
            "h": 3
        }
        # 從資料庫取得使用者的區域設定
        user_region = db.get_window_region(user_id)
        if user_region is None:
            user_region = default_region

        col1, col2 = st.columns(2)
        with col1:
            x = st.slider("X 位置 (%)", 0, 100, user_region["x"])
            y = st.slider("Y 位置 (%)", 0, 100, user_region["y"])
        with col2:
            w = st.slider("寬度 (%)", 1, 100, user_region["w"])
            h = st.slider("高度 (%)", 1, 100, user_region["h"])

        col1, col2 = st.columns(2)
        with col1:
            preview_button = st.button("瀏覽區域")
        with col2:
            if st.button("儲存視窗設定"):
                region = {"x": x, "y": y, "w": w, "h": h}
                db.save_window_region(user_id, region)
                st.success("已儲存視窗設定")

        if preview_button:
            st.info("正在擷取視窗...")
            bring_window_to_front(st.session_state.window)
            time.sleep(0.5)
            screenshot = capture_screenshot(st.session_state.window)
            if screenshot is not None:
                st.success("成功擷取畫面")
                height, width = screenshot.shape[:2]
                region = {
                    'x': int(width * x / 100),
                    'y': int(height * y / 100),
                    'w': int(width * w / 100),
                    'h': int(height * h / 100)
                }
                st.session_state.region = region
                preview = screenshot.copy()
                cv2.rectangle(preview, 
                            (region['x'], region['y']),
                            (region['x'] + region['w'], region['y'] + region['h']),
                            (0, 255, 0), 2)
                st.image(preview, channels="BGR", caption="預覽區域", use_container_width=True)
            else:
                st.error("擷取畫面失敗")

    col1, col2 = st.columns(2)
    with col1:
        start_button = st.button("開始追蹤")
    with col2:
        stop_button = st.button("結束")

    status_placeholder = st.empty()
    cropped_placeholder = st.empty()
    result_placeholder = st.empty()
    final_result_placeholder = st.empty()

    if start_button:
        st.session_state.final_results = None
        final_result_placeholder.empty()
        if st.session_state.window and st.session_state.region:
            st.session_state.start_time = time.time()
            initial_experience = None
            should_stop = False
            try:
                while not should_stop:
                    if stop_button:
                        should_stop = True
                        continue
                    current_time = time.time()
                    elapsed_time = current_time - st.session_state.start_time
                    status_placeholder.info("正在擷取畫面...")
                    screenshot = capture_screenshot(st.session_state.window)
                    if screenshot is None:
                        status_placeholder.error("擷取畫面失敗")
                        break
                    status_placeholder.info("正在處理畫面...")
                    region = st.session_state.region
                    cropped = screenshot[region['y']:region['y']+region['h'], 
                                      region['x']:region['x']+region['w']]
                    cropped_placeholder.image(cropped, caption="擷取區域", channels="BGR")
                    processed_placeholder = st.empty()
                    current_experience = extract_experience(cropped, show_processed=False, image_placeholder=processed_placeholder, ocr_engine='easyocr')
                    status_placeholder.info(f"目前經驗值: {current_experience}")
                    if current_experience is not None:
                        if initial_experience is None:
                            initial_experience = current_experience
                            result_placeholder.info(f"初始讀數: {initial_experience:,}")
                        else:
                            total_gained = current_experience - initial_experience
                            minutes_elapsed = elapsed_time / 60.0
                            experience_per_minute = total_gained / minutes_elapsed if minutes_elapsed > 0 else 0
                            current_results = {
                                "初始經驗值": f"{initial_experience:,}",
                                "最終經驗值": f"{current_experience:,}",
                                "總獲得經驗值": f"{total_gained:,}",
                                "平均每分鐘經驗值": f"{experience_per_minute:,.2f}",
                                "總計時間": f"{elapsed_time:.1f}秒"
                            }
                            result_text = ""
                            for k, v in current_results.items():
                                result_text += f"**{k}**  \n{v}  \n\n"
                            result_placeholder.success(result_text)
                            st.session_state.final_results = current_results
                    time.sleep(1)
                if should_stop:
                    status_placeholder.success("追蹤已結束")
            except Exception as e:
                st.error(f"追蹤時發生錯誤: {str(e)}")
                st.exception(e)
        else:
            st.error("請先選擇視窗並設定區域。")

    if st.session_state.final_results and not start_button:
        final_result_placeholder.success("最終追蹤結果：")
        final_result_placeholder.write(st.session_state.final_results)
        with st.expander("儲存本次紀錄"):
            monster_name = st.text_input("怪物/副本名稱")
            note = st.text_input("備註")
            if st.button("儲存紀錄"):
                if monster_name:
                    record_data = {
                        "user_id": user_id,
                        "user_name": user_name,
                        "怪物/副本": monster_name,
                        "備註": note,
                        **st.session_state.final_results
                    }
                    if db.save_record(user_id, record_data):
                        st.success("成功儲存紀錄！")
                else:
                    st.warning("請至少輸入怪物/副本名稱")
    # 歷史紀錄區塊（登入後一律顯示在最下方）
    st.markdown("---")
    st.subheader("🕑 歷史紀錄")
    records = db.get_user_records(user_id)
    if records:
        for record in records:
            if isinstance(record, tuple):
                # (id, user, monster, note, initial_exp, final_exp, total_exp, exp_per_min, total_time, timestamp)
                if len(record) == 10:
                    record_id, user, monster, note, initial_exp, final_exp, total_exp, exp_per_min, total_time, timestamp = record
                else:
                    st.write(str(record))
                    st.markdown("---")
                    continue
                cols = st.columns([2, 2, 2, 2, 1])
                with cols[0]:
                    st.markdown(f"**時間**\n\n{timestamp}")
                with cols[1]:
                    st.markdown(f"**怪物名稱**\n\n{monster}")
                with cols[2]:
                    st.markdown(f"**備註**\n\n{note}")
                with cols[3]:
                    st.metric("經驗值/分", f"{float(exp_per_min.replace(',', '')):,.2f}")
                with cols[4]:
                    if st.button("刪除", key=f"delete_{record_id}"):
                        db.delete_record(record_id)
                        st.rerun()
                st.markdown("---")


if __name__ == "__main__":
    main()