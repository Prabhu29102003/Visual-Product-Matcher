import streamlit as st
import json
import re
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Visual Product Matcher", layout="wide", page_icon="🛍")

# ---------- LOAD DATA ----------
json_file = "products.json"

if not os.path.exists(json_file):
    st.error(f"Error: {json_file} not found. Please make sure it exists in the same folder as app.py.")
    st.stop()

with open(json_file, "r") as f:
    products = json.load(f)

# ---------- STYLING ----------
st.markdown("""
<style>
body, h1, h2, h3, h4, p, div, span {font-family: 'Times New Roman', Times, serif;}
h1{text-align:center;color:#222;margin-bottom:30px;}
.search-section{
    background:#007bff;padding:25px;border-radius:12px;margin-bottom:30px;
    display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:20px;
}
.search-section input{
    width:300px;padding:10px 12px;border-radius:6px;border:none;font-size:1rem;
}
.search-section button{
    padding:10px 20px;border-radius:6px;background:#ffcc00;border:none;font-weight:bold;
    cursor:pointer;transition:0.3s;
}
.search-section button:hover{background:#ffb900;}
.results{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
    gap:25px;margin-top:20px;
}
.product-card{
    background:#fff;border-radius:12px;padding:15px;
    text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}
.product-card:hover{
    transform: translateY(-5px);
    box-shadow:0 8px 20px rgba(0,0,0,0.15);
}
.product-card img{
    width:100%;border-radius:10px;height:180px;object-fit:cover;margin-bottom:10px;
}
.product-card p{margin:5px 0;font-size:0.95rem;}
.product-card .tags{
    display:flex;flex-wrap:wrap;justify-content:center;gap:5px;margin-bottom:5px;
}
.product-card .tag{
    background:#f1f1f1;padding:3px 8px;border-radius:12px;font-size:0.75rem;
}
.product-card .price{color:green;font-weight:bold;font-size:1rem;margin-top:5px;}
</style>
""", unsafe_allow_html=True)

# ---------- UTILITIES ----------
def extract_keywords(text):
    name = re.split(r'[./_?=&-]+', text.split('/')[-1].lower())
    return [w for w in name if w and w.isalnum()]

def search_products(keywords):
    results = []
    for p in products:
        match_count = sum(any(k in t.lower() for t in p["tags"]) for k in keywords)
        if match_count > 0:
            p["score"] = match_count
            results.append(p)
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

# ---------- MAIN UI ----------
st.title("🛍 Visual Product Matcher")

# --- Search / Upload Section ---
st.markdown('<div class="search-section">', unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["jpg","jpeg","png"])
uploaded_preview = None
if uploaded_file:
    uploaded_preview = uploaded_file
    st.image(uploaded_preview, width=220, caption="Uploaded Image Preview")

url_input = st.text_input("Paste Image URL")
url_preview = None
if url_input:
    url_preview = url_input
    st.image(url_preview, width=220, caption="URL Image Preview")

query = uploaded_file.name if uploaded_file else url_input if url_input else None
search_clicked = st.button("Search Similar Products")
st.markdown("</div>", unsafe_allow_html=True)

# --- Process Search ---
if query and search_clicked:
    st.info("Searching for similar products...")
    keywords = extract_keywords(query)
    results = search_products(keywords)

    if results:
        st.markdown('<div class="results">', unsafe_allow_html=True)
        for p in results:
            tags_html = "".join([f'<span class="tag">{t}</span>' for t in p['tags']])
            st.markdown(f"""
            <div class="product-card">
                <img src="{p['image']}" alt="{p['name']}"/>
                <p><b>{p['name']}</b></p>
                <div class="tags">{tags_html}</div>
                <p class="price">{p['price']}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No matching products found.")
elif not query:
    st.info("Upload an image or paste a URL to start searching.")
