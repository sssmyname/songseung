import streamlit as st
import os
import json
from datetime import datetime
import base64
import uuid
import random

st.set_page_config(page_title="Playlist - 송승현", page_icon="🎤", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp {
        background-color: #0A0A0C;
        color: #EEEEEE;
        font-family: 'Inter', sans-serif;
    }
    h1 {
        color: #FFFFFF !important;
        font-weight: 700;
        letter-spacing: -1px;
        margin: 0 !important;
        text-shadow: 0px 0px 12px rgba(0, 230, 118, 0.6);
        display: flex;
        align-items: center;
    }
    h2, h3, h4 {
        color: #FFFFFF !important;
        font-weight: 600;
    }
    div[data-testid="stWidgetLabel"] p, 
    div[data-testid="stWidgetLabel"] span,
    label, 
    .stTextArea label p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        letter-spacing: 0.5px;
    }
    [data-testid="stSidebar"] {
        background-color: #101211 !important;
        border-right: 2px solid #00E676;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(135deg, #00E676 0%, #00C853 100%);
        color: #0A0A0C !important;
        font-weight: bold;
        font-size: 16px;
        border: none;
        padding: 12px;
        box-shadow: 0px 4px 15px rgba(0, 230, 118, 0.4);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #69F0AE 0%, #00B248 100%);
        box-shadow: 0px 6px 20px rgba(0, 230, 118, 0.6);
        transform: translateY(-1px);
        color: #0A0A0C !important;
    }
    [data-testid="stMetricValue"] {
        color: #00E676 !important;
        font-weight: bold;
        font-size: 38px !important;
        text-shadow: 0px 0px 10px rgba(0, 230, 118, 0.4);
    }
    .track-box {
        border: 1px solid #1A221E;
        padding: 25px;
        border-radius: 12px;
        background-color: #121614;
        box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.6);
    }
    .main-banner {
        background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(10, 10, 12, 0.95)), url('https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=1200&q=80');
        background-size: cover;
        background-position: center;
        padding: 35px;
        border-radius: 12px;
        border: 1px solid #1A221E;
        margin-bottom: 25px;
        box-shadow: 0px 4px 20px rgba(0, 230, 118, 0.15);
    }
    .album-art-frame {
        width: 100% !important;
        height: 320px !important;
        overflow: hidden !important;
        border-radius: 12px !important;
        border: 3px solid #00E676 !important;
        box-shadow: 0px 0px 25px rgba(0, 230, 118, 0.5) !important;
        background-color: #121614 !important;
        margin-bottom: 20px !important;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .album-art-frame img {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
        object-position: center !important;
    }
    .audio-player-wrapper {
        background-color: #0A0A0C !important;
        border: 2px solid #00E676 !important;
        border-radius: 40px !important;
        padding: 10px 15px !important;
        box-shadow: 0px 5px 20px rgba(0, 230, 118, 0.2) !important;
        margin-top: 15px !important;
        margin-bottom: 25px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .audio-player-wrapper audio {
        width: 100% !important;
        height: 45px !important;
        border-radius: 30px !important;
        outline: none !important;
        filter: invert(0.9) hue-rotate(180deg) grayscale(0.2) !important;
    }
    .sidebar-img-fixed {
        width: 100% !important;
        height: 180px !important;
        overflow: hidden !important;
        border-radius: 8px !important;
        border: 1px solid #1A221E !important;
        margin-bottom: 15px !important;
    }
    .sidebar-img-fixed img {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
    }
    
    @media (max-width: 768px) {
        h1 {
            font-size: 1.2rem !important;
            letter-spacing: -0.5px;
        }
        .main-banner {
            padding: 20px 15px !important;
        }
        .track-box {
            padding: 15px !important;
        }
        .album-art-frame {
            height: 250px !important;
        }
        .audio-player-wrapper {
            padding: 8px 12px !important;
            border-radius: 35px !important;
        }
        .audio-player-wrapper audio {
            height: 40px !important;
        }
        h1 img {
            width: 30px !important;
            height: 30px !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 28px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

if "review_file" not in st.session_state:
    st.session_state.review_file = "reviews.json"
if "voted_reviews" not in st.session_state:
    st.session_state.voted_reviews = []
if "auto_play" not in st.session_state:
    st.session_state.auto_play = False
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

def load_reviews():
    if os.path.exists(st.session_state.review_file):
        try:
            with open(st.session_state.review_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_reviews(reviews_list):
    with open(st.session_state.review_file, "w", encoding="utf-8") as f:
        json.dump(reviews_list, f, ensure_ascii=False, indent=4)

def delete_review(review_id):
    reviews = load_reviews()
    reviews = [r for r in reviews if r.get('id') != review_id]
    save_reviews(reviews)

def delete_reply(review_id, reply_id):
    reviews = load_reviews()
    for r in reviews:
        if r.get('id') == review_id:
            r['replies'] = [rep for rep in r['replies'] if rep.get('id') != reply_id]
            break
    save_reviews(reviews)

current_reviews = load_reviews()
needs_save = False

for r in current_reviews:
    if 'id' not in r:
        r['id'] = str(uuid.uuid4())
        needs_save = True
    if 'upvotes' not in r:
        r['upvotes'] = 0
        needs_save = True
    if 'downvotes' not in r:
        r['downvotes'] = 0
        needs_save = True
    if 'replies' not in r:
        r['replies'] = []
        needs_save = True
    if 'password' not in r:
        r['password'] = ""
        needs_save = True

if needs_save:
    save_reviews(current_reviews)

def handle_vote(review_id, vote_type):
    reviews = load_reviews()
    for rev in reviews:
        if rev.get('id') == review_id:
            if vote_type == 'up':
                rev['upvotes'] = rev.get('upvotes', 0) + 1
            elif vote_type == 'down':
                rev['downvotes'] = rev.get('downvotes', 0) + 1
            break
    save_reviews(reviews)
    if review_id not in st.session_state.voted_reviews:
        st.session_state.voted_reviews.append(review_id)

if "shuffled_tracks" not in st.session_state:
    raw_files = [f for f in os.listdir('.') if f.endswith(('.mp3', '.wav'))]
    random.shuffle(raw_files)
    st.session_state.shuffled_tracks = raw_files

music_files = st.session_state.shuffled_tracks

if music_files:
    if "track_selector" not in st.session_state:
        st.session_state.track_selector = music_files[0]

    def next_track():
        current_idx = music_files.index(st.session_state.track_selector)
        next_idx = (current_idx + 1) % len(music_files)
        st.session_state.track_selector = music_files[next_idx]
        st.session_state.auto_play = True

    def prev_track():
        current_idx = music_files.index(st.session_state.track_selector)
        prev_idx = (current_idx - 1) % len(music_files)
        st.session_state.track_selector = music_files[prev_idx]
        st.session_state.auto_play = True

with st.sidebar:
    st.markdown("<h2 style='color:#00E676 !important; font-weight:700; margin-top:0; letter-spacing:-1px;'>🎵 playlist</h2>", unsafe_allow_html=True)
    st.divider()
    
    profile_target = None
    for p_file in ["캡처.jpg", "ㄸㄷ_2.jpg"]:
        if os.path.exists(p_file):
            profile_target = p_file
            break
            
    if profile_target:
        try:
            with open(profile_target, "rb") as img_file:
                sb_b64 = base64.b64encode(img_file.read()).decode()
                st.markdown(f'<div class="sidebar-img-fixed"><img src="data:image/jpeg;base64,{sb_b64}"></div>', unsafe_allow_html=True)
        except Exception:
            pass
        
    st.markdown("<h3 style='margin-bottom:5px;'>🎤 MY TRACKLIST</h3>", unsafe_allow_html=True)
    
    if not music_files:
        st.error("폴더에 음악 파일이 없습니다.")
        selected_music = None
    else:
        selected_music = st.selectbox("스트리밍할 트랙 선택", music_files, key="track_selector", label_visibility="collapsed")

    st.write("")
    st.markdown("<h3 style='margin-bottom:15px; border-bottom:2px solid #00E676; padding-bottom:5px;'>🏆 REALTIME CHART</h3>", unsafe_allow_html=True)
    
    track_scores = {}
    for r in current_reviews:
        t = r['track']
        if t not in track_scores:
            track_scores[t] = []
        track_scores[t].append(r['avg'])
        
    if track_scores:
        chart_data = [{"track": k, "avg": sum(v)/len(v)} for k, v in track_scores.items()]
        chart_data.sort(key=lambda x: x['avg'], reverse=True)
        
        for idx, item in enumerate(chart_data):
            st.markdown(f"""
            <div style='background-color:#121614; padding:12px; border-radius:8px; margin-bottom:10px; border-left:4px solid #00E676; display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <span style='color:#00E676; font-weight:bold; font-size:18px; margin-right:10px;'>{idx+1}위</span>
                    <span style='color:#EEEEEE; font-size:14px; font-weight:600;'>{item['track']}</span>
                </div>
                <span style='color:#00E676; font-weight:bold; font-size:16px;'>★ {item['avg']:.1f}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("평가 데이터가 없습니다.")

    st.write("")
    st.write("")
    st.markdown("<h3 style='margin-bottom:10px; border-bottom:2px solid #555566; padding-bottom:5px; color:#AAAAAA !important;'>⚙️ ADMIN AREA</h3>", unsafe_allow_html=True)
    
    if not st.session_state.is_admin:
        with st.expander("🔐 관리자 로그인"):
            admin_pwd = st.text_input("비밀번호를 입력하세요", type="password")
            if st.button("로그인"):
                if admin_pwd == "a159s753":
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.error("비밀번호가 일치하지 않습니다.")
    else:
        st.success("👑 관리자 모드가 활성화되었습니다.")
        if st.button("로그아웃"):
            st.session_state.is_admin = False
            st.rerun()

if selected_music:
    st.markdown('<div class="main-banner">', unsafe_allow_html=True)
    
    profile_svg = '<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#00E676"/><text x="50%" y="50%" font-family="sans-serif" font-size="50" fill="#0A0A0C" text-anchor="middle" dominant-baseline="central">👤</text></svg>'
    profile_b64 = base64.b64encode(profile_svg.encode('utf-8')).decode('utf-8')
    profile_img_src = f"data:image/svg+xml;base64,{profile_b64}"
    
    if profile_target:
        try:
            with open(profile_target, "rb") as img_file:
                b64_str = base64.b64encode(img_file.read()).decode()
                profile_img_src = f"data:image/jpeg;base64,{b64_str}"
        except Exception:
            pass

    st.markdown(f"""
    <h1>
        <img src="{profile_img_src}" style="width:40px; height:40px; border-radius:50%; object-fit:cover; margin-right:12px; border:2px solid #00E676; box-shadow: 0px 0px 8px rgba(0,230,118,0.5);">
        🎤 힙합꿈나무 송승현의 자작곡 평가하기 🎸
    </h1>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='color:#00E676; margin:8px 0 0 0; font-size:16px; font-weight:600;'>🎹 BEAT LAB & SOUND STREAMING 🎶</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.25])
    
    with col1:
        st.markdown('<div class="track-box">', unsafe_allow_html=True)
        st.markdown(f"<h3 style='margin-top:0; color:#00E676 !important; font-size:22px;'>🔥 Now Playing: {selected_music}</h3>", unsafe_allow_html=True)
        
        current_index = music_files.index(selected_music) if selected_music in music_files else 0
        
        cover_files = [f for f in os.listdir('.') if f.lower().endswith(('.gif', '.png', '.jpg', '.jpeg', '.webp')) and f not in ["캡처.jpg", "ㄸㄷ_2.jpg"]]
        
        fallback_svg = '<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#121614"/><text x="50%" y="50%" font-family="sans-serif" font-size="24" fill="#00E676" text-anchor="middle" dominant-baseline="middle">사진 폴더에 사진이나 GIF 움짤을 넣어주세요!</text></svg>'
        fb_b64 = base64.b64encode(fallback_svg.encode('utf-8')).decode('utf-8')
        assigned_cover = f"data:image/svg+xml;base64,{fb_b64}"
        
        if cover_files:
            c_file = cover_files[current_index % len(cover_files)]
            try:
                with open(c_file, "rb") as f:
                    c_b64 = base64.b64encode(f.read()).decode()
                c_ext = c_file.split('.')[-1].lower()
                c_mime = "gif" if c_ext == 'gif' else ("jpeg" if c_ext in ['jpg', 'jpeg'] else c_ext)
                assigned_cover = f"data:image/{c_mime};base64,{c_b64}"
            except Exception:
                pass
        else:
            backup_images = [
                "https://media.tenor.com/m8ZWcv-v96QAAAAC/dance-moves.gif",
                "https://media.tenor.com/y1vKIfbZ46gAAAAC/anime-dance.gif",
                "https://media.tenor.com/2Uee-E8E42IAAAAC/naruto-sasuke.gif",
                "https://media.tenor.com/8Qz_W4qU13UAAAAC/cat-jam.gif",
                "https://media.tenor.com/GfJTqO2Xl4QAAAAC/meme-dog.gif",
                "https://media.tenor.com/f2905Kj21aYAAAAC/spongebob-patrick.gif",
                "https://media.tenor.com/pZqN-H00fPMAAAAC/funny-laugh.gif",
                "https://media.tenor.com/8Tf5QzK073AAAAAC/huh-meme.gif",
                "https://media.tenor.com/tVvw0ZJd_r8AAAAC/monkey-dance.gif",
                "https://media.tenor.com/XFEtL2w9b78AAAAC/anime-wow.gif",
                "https://media.tenor.com/d_n49H5e3BIAAAAC/doge-dance.gif",
                "https://media.tenor.com/B7qjGv2GZ_MAAAAC/pepe-dance.gif",
                "https://media.tenor.com/Fw5uF70jLh8AAAAC/pika-dance.gif",
                "https://media.tenor.com/xO4bB1wK-8wAAAAC/shrek-dance.gif",
                "https://media.tenor.com/I7p20N-J3R8AAAAC/duck-dance.gif",
                "https://media.tenor.com/H0V167U2Zp8AAAAC/mario-dance.gif",
                "https://media.tenor.com/7bQ6zZ1OQv0AAAAC/goku-dance.gif",
                "https://media.tenor.com/H1Gj5P8vK-8AAAAC/cat-vibe.gif",
                "https://media.tenor.com/p_P_x2_1kAMAAAAC/kermit-dance.gif",
                "https://media.tenor.com/8V-N-B1_g0AAAAAC/jojo-dance.gif"
            ]
            assigned_cover = backup_images[current_index % len(backup_images)]
            
        st.markdown(f'<div class="album-art-frame"><img src="{assigned_cover}" referrerpolicy="no-referrer"></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="audio-player-wrapper">', unsafe_allow_html=True)
        
        should_autoplay = st.session_state.get("auto_play", False)
        st.audio(selected_music, autoplay=should_autoplay)
        st.session_state.auto_play = False
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            st.button("◀ 이전 곡", on_click=prev_track, use_container_width=True, key="main_prev")
        with btn_c2:
            st.button("다음 곡 ▶", on_click=next_track, use_container_width=True, key="main_next")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="track-box">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0; border-bottom:2px solid #00E676; padding-bottom:10px;'>📊 ⚡ CRITIC STATION</h3>", unsafe_allow_html=True)
        
        score_melody = st.number_input("🎵 Melody (멜로디라인 및 중독성) 🎹", min_value=1, max_value=5, value=3, step=1)
        score_rhythm = st.number_input("🥁 Rhythm & Beats (드럼 신기감 및 그루브) 🎧", min_value=1, max_value=5, value=3, step=1)
        score_origin = st.number_input("✨ Originality (곡의 독창성 및 실험성) ⚡", min_value=1, max_value=5, value=3, step=1)
        
        avg_score = round((score_melody + score_rhythm + score_origin) / 3, 1)
        st.metric("👑 TOTAL RATING SCORE", f"{avg_score} / 5.0")
        
        col_nick, col_pwd = st.columns(2)
        with col_nick:
            reviewer_name = st.text_input("👤 작성자 닉네임:", placeholder="예: 힙합마니아")
        with col_pwd:
            reviewer_pwd = st.text_input("🔒 비밀번호 (수정/삭제용):", type="password", placeholder="비밀번호 입력")
            
        feedback = st.text_area("📝 공개 댓글 (유저 상세설명):", placeholder="비트의 구성, 악기 소스, 전개 방식 등 프로듀싱 피드백을 자유롭게 남겨주세요.")
        
        uploaded_img = st.file_uploader("📸 이미지 첨부 (선택사항)", type=["png", "jpg", "jpeg"])
        
        st.write("")
        
        if st.button("REVIEW SUBMIT 🚀"):
            if not reviewer_name or not reviewer_pwd:
                st.warning("닉네임을 입력해야 리뷰를 등록할 수 있습니다!")
            else:
                st.success("트랙 피드백 리포트가 정상적으로 발행되었습니다.")
                
                img_b64 = None
                img_mime = None
                if uploaded_img is not None:
                    img_b64 = base64.b64encode(uploaded_img.getvalue()).decode()
                    img_mime = uploaded_img.type
                
                review_data = {
                    "id": str(uuid.uuid4()),
                    "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "track": selected_music,
                    "nickname": reviewer_name,
                    "password": reviewer_pwd,
                    "melody": score_melody,
                    "rhythm": score_rhythm,
                    "origin": score_origin,
                    "avg": avg_score,
                    "comment": feedback if feedback else "의견 없음",
                    "img_b64": img_b64,
                    "img_mime": img_mime,
                    "upvotes": 0,
                    "downvotes": 0,
                    "replies": []
                }
                current_reviews.append(review_data)
                save_reviews(current_reviews)
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("<div class='track-box'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; border-bottom:2px solid #00E676; padding-bottom:10px;'>💬 REALTIME FEEDBACK BOARD</h3>", unsafe_allow_html=True)
    
    if not current_reviews:
        st.info("아직 등록된 실시간 피드백이 없습니다. 첫 리뷰를 남겨보세요!")
    else:
        for r in reversed(current_reviews):
            img_html = ""
            if r.get("img_b64") and r.get("img_mime"):
                img_html = f"<img src='data:{r['img_mime']};base64,{r['img_b64']}' style='max-width:100%; border-radius:8px; margin-top:12px; border:1px solid #1A221E;' />"
                
            st.markdown(f"""
            <div style='background-color:#0A0A0C; padding:15px; border-radius:8px; margin-bottom:8px; border-left:4px solid #00E676; border-top:1px solid #1A221E; border-right:1px solid #1A221E; border-bottom:1px solid #1A221E;'>
                <p style='margin:0; font-size:12px; color:#888899;'>{r['date']} | <b>트랙: {r['track']}</b> | <b style='color:#00E676;'>작성자: {r.get('nickname', '익명')}</b></p>
                <p style='margin:6px 0; font-weight:bold; color:#00E676; font-size:15px;'>👑 총점: {r['avg']} / 5.0 <span style='font-size:12px; color:#EEEEEE; font-weight:normal;'>(멜로디:{r['melody']} 리듬:{r['rhythm']} 독창성:{r['origin']})</span></p>
                <p style='margin:0; color:#EEEEEE; font-size:14px; background-color:#121614; padding:10px; border-radius:6px;'>{r['comment']}</p>
                {img_html}
            </div>
            """, unsafe_allow_html=True)

            has_voted = r['id'] in st.session_state.voted_reviews

            if st.session_state.is_admin:
                btn_col1, btn_col2, btn_col3, _ = st.columns([1.5, 1.5, 1.5, 2])
            else:
                btn_col1, btn_col2, _ = st.columns([1.5, 1.5, 3])

            with btn_col1:
                st.button(f"🟢 👍 추천 {r['upvotes']}", key=f"up_{r['id']}", disabled=has_voted, on_click=handle_vote, args=(r['id'], 'up'))
            with btn_col2:
                st.button(f"🔴 👎 비추천 {r['downvotes']}", key=f"dn_{r['id']}", disabled=has_voted, on_click=handle_vote, args=(r['id'], 'down'))
            
            if st.session_state.is_admin:
                with btn_col3:
                    if st.button("🗑️ 강제 삭제", key=f"del_admin_{r['id']}"):
                        delete_review(r['id'])
                        st.rerun()

            if not st.session_state.is_admin:
                with st.expander("🗑️ 본인 댓글 삭제"):
                    del_pwd = st.text_input("비밀번호 확인", type="password", key=f"del_pwd_{r['id']}")
                    if st.button("삭제하기", key=f"del_btn_{r['id']}"):
                        if del_pwd == r.get('password'):
                            delete_review(r['id'])
                            st.rerun()
                        else:
                            st.error("비밀번호가 일치하지 않습니다.")

            for reply in r['replies']:
                reply_img_html = ""
                if reply.get("img_b64") and reply.get("img_mime"):
                    reply_img_html = f"<img src='data:{reply['img_mime']};base64,{reply['img_b64']}' style='max-width:80%; border-radius:8px; margin-top:8px; border:1px solid #1A221E;' />"
                
                st.markdown(f"""
                <div style='background-color:#121614; padding:12px; border-radius:8px; margin-left:30px; margin-bottom:8px; border-left:3px solid #334433;'>
                    <p style='margin:0; font-size:12px; color:#888899;'>↳ {reply['date']} | <b style='color:#AAAAAA;'>작성자: {reply['nickname']}</b></p>
                    <p style='margin:6px 0 0 0; color:#EEEEEE; font-size:13px;'>{reply['comment']}</p>
                    {reply_img_html}
                </div>
                """, unsafe_allow_html=True)
                
                if st.session_state.is_admin:
                    del_rep_col1, _ = st.columns([2.5, 5])
                    with del_rep_col1:
                        if st.button("🗑️ 대댓글 강제 삭제", key=f"del_rep_admin_{reply['id']}"):
                            delete_reply(r['id'], reply['id'])
                            st.rerun()
                else:
                    with st.expander(f"🗑️ 본인 대댓글 삭제 ({reply['nickname']})"):
                        rep_del_pwd = st.text_input("비밀번호 확인", type="password", key=f"del_rep_pwd_{reply['id']}")
                        if st.button("삭제하기", key=f"del_rep_btn_{reply['id']}"):
                            if rep_del_pwd == reply.get('password'):
                                delete_reply(r['id'], reply['id'])
                                st.rerun()
                            else:
                                st.error("비밀번호가 일치하지 않습니다.")

            with st.expander("💬 대댓글 달기"):
                with st.form(key=f"form_{r['id']}"):
                    col_rn, col_rp = st.columns(2)
                    with col_rn:
                        reply_nick = st.text_input("닉네임", key=f"nick_{r['id']}")
                    with col_rp:
                        reply_pwd = st.text_input("비밀번호", type="password", key=f"pwd_{r['id']}")
                        
                    reply_comment = st.text_area("내용", key=f"comm_{r['id']}")
                    reply_img = st.file_uploader("사진 첨부 (선택)", type=["png", "jpg", "jpeg"], key=f"img_{r['id']}")
                    
                    if st.form_submit_button("등록"):
                        if not reply_nick or not reply_pwd:
                            st.warning("닉네임과 비밀번호를 모두 입력해주세요!")
                        else:
                            r_img_b64 = None
                            r_img_mime = None
                            if reply_img is not None:
                                r_img_b64 = base64.b64encode(reply_img.getvalue()).decode()
                                r_img_mime = reply_img.type
                                
                            new_reply = {
                                "id": str(uuid.uuid4()),
                                "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                "nickname": reply_nick,
                                "password": reply_pwd,
                                "comment": reply_comment if reply_comment else "의견 없음",
                                "img_b64": r_img_b64,
                                "img_mime": r_img_mime
                            }
                            r['replies'].append(new_reply)
                            save_reviews(current_reviews)
                            st.rerun()

            st.write("---")

    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.warning("👈 왼쪽 패널에서 음악 파일을 선택하면 플레이어가 활성화됩니다.")