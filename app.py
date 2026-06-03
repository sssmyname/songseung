import streamlit as st
import os
import json
from datetime import datetime
import base64
import uuid

st.set_page_config(page_title="Playlist - 송승현", page_icon="🎤", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp {
        background-color: #0D0D11;
        color: #EEEEEE;
        font-family: 'Inter', sans-serif;
    }
    h1 {
        color: #FFFFFF !important;
        font-weight: 700;
        letter-spacing: -1px;
        margin: 0 !important;
        text-shadow: 0px 0px 12px rgba(255, 85, 0, 0.6);
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
        background-color: #13131A !important;
        border-right: 2px solid #FF5500;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(135deg, #FF5500 0%, #FF2200 100%);
        color: #FFFFFF !important;
        font-weight: bold;
        font-size: 16px;
        border: none;
        padding: 12px;
        box-shadow: 0px 4px 15px rgba(255, 85, 0, 0.4);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #FF7733 0%, #FF4400 100%);
        box-shadow: 0px 6px 20px rgba(255, 85, 0, 0.6);
        transform: translateY(-1px);
        color: #FFFFFF !important;
    }
    [data-testid="stMetricValue"] {
        color: #FF5500 !important;
        font-weight: bold;
        font-size: 38px !important;
        text-shadow: 0px 0px 10px rgba(255, 85, 0, 0.4);
    }
    .track-box {
        border: 1px solid #252533;
        padding: 25px;
        border-radius: 12px;
        background-color: #161622;
        box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.5);
    }
    .main-banner {
        background: linear-gradient(rgba(0, 0, 0, 0.35), rgba(13, 13, 17, 0.95)), url('https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=1200&q=80');
        background-size: cover;
        background-position: center;
        padding: 35px;
        border-radius: 12px;
        border: 1px solid #252533;
        margin-bottom: 25px;
        box-shadow: 0px 4px 20px rgba(255, 85, 0, 0.2);
    }
    .album-art-frame {
        width: 100% !important;
        height: 320px !important;
        overflow: hidden !important;
        border-radius: 12px !important;
        border: 3px solid #FF5500 !important;
        box-shadow: 0px 0px 25px rgba(255, 85, 0, 0.6) !important;
        background-color: #000000 !important;
        margin-bottom: 20px !important;
    }
    .album-art-frame img {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
        object-position: center !important;
    }
    .audio-player-wrapper {
        background-color: #09090D !important;
        border: 1px solid #252533 !important;
        border-radius: 40px !important;
        padding: 15px 20px !important;
        box-shadow: inset 0px 2px 5px rgba(0,0,0,0.6) !important;
        margin-top: 15px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .audio-player-wrapper audio {
        width: 100% !important;
        height: 45px !important;
        transform: scale(1.15) !important;
        transform-origin: center center !important;
        filter: invert(90%) hue-rotate(165deg) saturate(220%) !important;
    }
    .sidebar-img-fixed {
        width: 100% !important;
        height: 180px !important;
        overflow: hidden !important;
        border-radius: 8px !important;
        border: 1px solid #252533 !important;
        margin-bottom: 15px !important;
    }
    .sidebar-img-fixed img {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
    }
    
    @media (max-width: 768px) {
        h1 {
            font-size: 1.4rem !important;
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
            padding: 10px 15px !important;
        }
        .audio-player-wrapper audio {
            transform: scale(1.0) !important;
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

with st.sidebar:
    st.markdown("<h2 style='color:#FF5500 !important; font-weight:700; margin-top:0; letter-spacing:-1px;'>🎵 playlist</h2>", unsafe_allow_html=True)
    st.divider()
    
    if os.path.exists("ㄸㄷ_2.jpg"):
        st.markdown('<div class="sidebar-img-fixed"><img src="ㄸㄷ_2.jpg"></div>', unsafe_allow_html=True)
        
    st.markdown("<h3 style='margin-bottom:5px;'>🎤 MY TRACKLIST</h3>", unsafe_allow_html=True)
    music_files = [f for f in os.listdir('.') if f.endswith(('.mp3', '.wav'))]
    
    if not music_files:
        st.error("폴더에 음악 파일이 없습니다.")
        selected_music = None
    else:
        if "track_selector" not in st.session_state:
            st.session_state.track_selector = music_files[0]

        def next_track():
            current_idx = music_files.index(st.session_state.track_selector)
            next_idx = (current_idx + 1) % len(music_files)
            st.session_state.track_selector = music_files[next_idx]

        def prev_track():
            current_idx = music_files.index(st.session_state.track_selector)
            prev_idx = (current_idx - 1) % len(music_files)
            st.session_state.track_selector = music_files[prev_idx]

        col_prev, col_next = st.columns(2)
        with col_prev:
            st.button("◀ 이전 곡", on_click=prev_track, use_container_width=True)
        with col_next:
            st.button("다음 곡 ▶", on_click=next_track, use_container_width=True)

        selected_music = st.selectbox("스트리밍할 트랙 선택", music_files, key="track_selector", label_visibility="collapsed")

    st.write("")
    st.markdown("<h3 style='margin-bottom:15px; border-bottom:2px solid #FF5500; padding-bottom:5px;'>🏆 REALTIME CHART</h3>", unsafe_allow_html=True)
    
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
            <div style='background-color:#161622; padding:12px; border-radius:8px; margin-bottom:10px; border-left:4px solid #FF5500; display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <span style='color:#FF5500; font-weight:bold; font-size:18px; margin-right:10px;'>{idx+1}위</span>
                    <span style='color:#EEEEEE; font-size:14px; font-weight:600;'>{item['track']}</span>
                </div>
                <span style='color:#FF5500; font-weight:bold; font-size:16px;'>★ {item['avg']:.1f}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("평가 데이터가 없습니다.")

if selected_music:
    st.markdown('<div class="main-banner">', unsafe_allow_html=True)
    
    profile_img_src = "ㄸㄷ_2.jpg" if os.path.exists("ㄸㄷ_2.jpg") else "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=100&q=80"
    st.markdown(f"""
    <h1>
        <img src="{profile_img_src}" style="width:40px; height:40px; border-radius:50%; object-fit:cover; margin-right:12px; border:2px solid #FF5500; box-shadow: 0px 0px 8px rgba(255,85,0,0.5);">
        🎤 힙합꿈나무 송승현의 자작곡 평가하기 🎸
    </h1>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='color:#FF5500; margin:8px 0 0 0; font-size:16px; font-weight:600;'>🎹 BEAT LAB & SOUND STREAMING 🎶</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.25])
    
    with col1:
        st.markdown('<div class="track-box">', unsafe_allow_html=True)
        st.markdown(f"<h3 style='margin-top:0; color:#FF5500 !important; font-size:22px;'>🔥 Now Playing: {selected_music}</h3>", unsafe_allow_html=True)
        
        backup_images = [
            "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=600&q=80",
            "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=600&q=80",
            "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600&q=80",
            "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=600&q=80",
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&q=80",
            "https://images.unsplash.com/photo-1507838153414-b4b713384a76?w=600&q=80",
            "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=600&q=80",
            "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=600&q=80",
            "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?w=600&q=80",
            "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=600&q=80",
            "https://images.unsplash.com/photo-1511192336575-5a79af67a629?w=600&q=80",
            "https://images.unsplash.com/photo-1506157786151-b8491531f063?w=600&q=80",
            "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&q=80",
            "https://images.unsplash.com/photo-1510915228340-29c85a43dcfe?w=600&q=80",
            "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=600&q=80",
            "https://images.unsplash.com/photo-1484876065684-b683cf17d276?w=600&q=80",
            "https://images.unsplash.com/photo-1453090927415-5f45085b65c0?w=600&q=80",
            "https://images.unsplash.com/photo-1511735111819-9a3f7709049c?w=600&q=80",
            "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?w=600&q=80",
            "https://images.unsplash.com/photo-1513829092322-02d373236fa1?w=600&q=80"
        ]
        
        current_index = music_files.index(selected_music) if selected_music in music_files else 0
        assigned_cover = backup_images[current_index % len(backup_images)]
        
        st.markdown(f'<div class="album-art-frame"><img src="{assigned_cover}"></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="audio-player-wrapper">', unsafe_allow_html=True)
        st.audio(selected_music)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="track-box">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0; border-bottom:2px solid #FF5500; padding-bottom:10px;'>📊 ⚡ CRITIC STATION</h3>", unsafe_allow_html=True)
        
        score_melody = st.number_input("🎵 Melody (멜로디라인 및 중독성) 🎹", min_value=1, max_value=5, value=3, step=1)
        score_rhythm = st.number_input("🥁 Rhythm & Beats (드럼 신기감 및 그루브) 🎧", min_value=1, max_value=5, value=3, step=1)
        score_origin = st.number_input("✨ Originality (곡의 독창성 및 실험성) ⚡", min_value=1, max_value=5, value=3, step=1)
        
        avg_score = round((score_melody + score_rhythm + score_origin) / 3, 1)
        st.metric("👑 TOTAL RATING SCORE", f"{avg_score} / 5.0")
        
        reviewer_name = st.text_input("👤 작성자 닉네임:", placeholder="닉네임을 입력해주세요 (예: 힙합마니아)")
        feedback = st.text_area("📝 공개 댓글 (유저 상세설명):", placeholder="비트의 구성, 악기 소스, 전개 방식 등 프로듀싱 피드백을 자유롭게 남겨주세요.")
        
        uploaded_img = st.file_uploader("📸 이미지 첨부 (선택사항)", type=["png", "jpg", "jpeg"])
        
        st.write("")
        
        if st.button("REVIEW SUBMIT 🚀"):
            if not reviewer_name:
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
    st.markdown("<h3 style='margin-top:0; border-bottom:2px solid #FF5500; padding-bottom:10px;'>💬 REALTIME FEEDBACK BOARD</h3>", unsafe_allow_html=True)
    
    if not current_reviews:
        st.info("아직 등록된 실시간 피드백이 없습니다. 첫 리뷰를 남겨보세요!")
    else:
        for r in reversed(current_reviews):
            img_html = ""
            if r.get("img_b64") and r.get("img_mime"):
                img_html = f"<img src='data:{r['img_mime']};base64,{r['img_b64']}' style='max-width:100%; border-radius:8px; margin-top:12px; border:1px solid #252533;' />"
                
            st.markdown(f"""
            <div style='background-color:#0D0D11; padding:15px; border-radius:8px; margin-bottom:8px; border-left:4px solid #FF5500; border-top:1px solid #252533; border-right:1px solid #252533; border-bottom:1px solid #252533;'>
                <p style='margin:0; font-size:12px; color:#888899;'>{r['date']} | <b>트랙: {r['track']}</b> | <b style='color:#FF5500;'>작성자: {r.get('nickname', '익명')}</b></p>
                <p style='margin:6px 0; font-weight:bold; color:#FF5500; font-size:15px;'>👑 총점: {r['avg']} / 5.0 <span style='font-size:12px; color:#EEEEEE; font-weight:normal;'>(멜로디:{r['melody']} 리듬:{r['rhythm']} 독창성:{r['origin']})</span></p>
                <p style='margin:0; color:#EEEEEE; font-size:14px; background-color:#13131A; padding:10px; border-radius:6px;'>{r['comment']}</p>
                {img_html}
            </div>
            """, unsafe_allow_html=True)

            has_voted = r['id'] in st.session_state.voted_reviews

            btn_col1, btn_col2, _ = st.columns([1.5, 1.5, 3])
            with btn_col1:
                st.button(f"🟢 👍 추천 {r['upvotes']}", key=f"up_{r['id']}", disabled=has_voted, on_click=handle_vote, args=(r['id'], 'up'))
            with btn_col2:
                st.button(f"🔴 👎 비추천 {r['downvotes']}", key=f"dn_{r['id']}", disabled=has_voted, on_click=handle_vote, args=(r['id'], 'down'))

            for reply in r['replies']:
                reply_img_html = ""
                if reply.get("img_b64") and reply.get("img_mime"):
                    reply_img_html = f"<img src='data:{reply['img_mime']};base64,{reply['img_b64']}' style='max-width:80%; border-radius:8px; margin-top:8px; border:1px solid #252533;' />"
                st.markdown(f"""
                <div style='background-color:#13131A; padding:12px; border-radius:8px; margin-left:30px; margin-bottom:8px; border-left:3px solid #555566;'>
                    <p style='margin:0; font-size:12px; color:#888899;'>↳ {reply['date']} | <b style='color:#AAAAAA;'>작성자: {reply['nickname']}</b></p>
                    <p style='margin:6px 0 0 0; color:#EEEEEE; font-size:13px;'>{reply['comment']}</p>
                    {reply_img_html}
                </div>
                """, unsafe_allow_html=True)

            with st.expander("💬 대댓글 달기"):
                with st.form(key=f"form_{r['id']}"):
                    reply_nick = st.text_input("닉네임", key=f"nick_{r['id']}")
                    reply_comment = st.text_area("내용", key=f"comm_{r['id']}")
                    reply_img = st.file_uploader("사진 첨부 (선택)", type=["png", "jpg", "jpeg"], key=f"img_{r['id']}")
                    
                    if st.form_submit_button("등록"):
                        if not reply_nick:
                            st.warning("닉네임을 입력해주세요!")
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