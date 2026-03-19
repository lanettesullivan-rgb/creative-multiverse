import random, textwrap
from io import StringIO
import streamlit as st

# ============================================================
# 1. Creative Layer Definitions
# ============================================================
layers = {
    "Industry": {1:"Beauty",2:"Fashion",3:"Technology",4:"Entertainment",5:"Real estate",6:"Wellness"},
    "Aesthetic": {1:"Luxury editorial",2:"Cinematic realism",3:"Futuristic design",4:"Surreal art film",5:"Mythic fantasy",6:"Documentary realism"},
    "Environment": {1:"Penthouse skyline",2:"Desert landscape",3:"Glass greenhouse",4:"Futuristic city",5:"Palace interior",6:"Ocean cliffside"},
    "Symbol": {1:"Chrome sculpture",2:"Floating diamonds",3:"Holographic screens",4:"Albino python",5:"Mirror fragments",6:"Glowing mist"},
    "Tone": {1:"Empowerment",2:"Mystery",3:"Aspiration",4:"Transformation",5:"Elegance",6:"Innovation"},
    "Narrative": {1:"Rebellion story",2:"Discovery story",3:"Transformation arc",4:"Rivalry conflict",5:"Rise to power",6:"Hidden world reveal"},
}

# ============================================================
# 2. Semantic Bias Map (Multi-theme Associations)
# ============================================================
theme_bias = {
    "eco":["Wellness","Ocean","Glass","Transformation","Documentary"],
    "nature":["Wellness","Ocean","Greenhouse"],
    "luxury":["Fashion","Luxury","Elegance","Palace"],
    "tech":["Technology","Futuristic","Innovation","Holographic"],
    "dream":["Surreal","Mythic","Mystery","Transformation"],
    "power":["Rise","Empowerment","Rivalry","Chrome"],
    "urban":["City","Skyline","Technology","Real estate"],
    "romance":["Elegance","Aspiration","Palace","Beauty"],
    "chaos":["Rebellion","Rivalry","Transformation","Desert"],
    "mystic":["Mythic","Surreal","Hidden","Glowing"],
}

# ============================================================
# 3. Generator Functions
# ============================================================
def parse_themes(theme_input:str):
    return [t.strip().lower() for t in theme_input.split(",") if t.strip()]

def blended_bias(themes:list, options:dict):
    if not themes:
        return random.randint(1,len(options))
    weight_map={}
    for theme in themes:
        related=theme_bias.get(theme,[])
        for i,val in options.items():
            score=sum(term.lower() in val.lower() for term in related)
            weight_map[i]=weight_map.get(i,0)+score
    weights=[weight_map.get(i,0)+1 for i in options]
    return random.choices(list(options.keys()),weights=weights)[0]

def generate_code(themes=None):
    return [blended_bias(themes,opts) for opts in layers.values()]

def decode_code(code):
    categories=list(layers.keys())
    return {categories[i]:layers[categories[i]][code[i]] for i in range(len(code))}

def expand(decoded):
    ind,aes,env,sym,tone,nar = (
        decoded["Industry"],decoded["Aesthetic"],decoded["Environment"],
        decoded["Symbol"],decoded["Tone"],decoded["Narrative"]
    )
    title=f'"{tone} in Motion"'
    movie=f"In a {env} bathed in {aes.lower()}, a {ind.lower()} visionary faces a {nar.lower()} defined by {tone.lower()} and mirrored in {sym.lower()}."
    campaign=f"{title} — a {aes.lower()} {ind.lower()} narrative set in a {env} surrounding {sym.lower()}, capturing {tone.lower()} as its core emotion."
    world=f"This {env.lower()} society treats {sym.lower()} as art and currency, powered by {tone.lower()} ideals that reshape {ind.lower()}."
    prompt=f"{aes}, {env}, featuring {sym}, tone of {tone.lower()}, {ind.lower()} theme, cinematic style, ultra detailed, realistic lighting."
    return {
        "Campaign Title":title,
        "Movie Concept":movie,
        "Worldbuilding":world,
        "AI Image Prompt":prompt,
        "Campaign Summary":campaign
    }

# ============================================================
# 4. Streamlit Front-End
# ============================================================
st.set_page_config(page_title="Creative Multiverse Spinner", layout="wide")

st.title("🌌 Creative Multiverse Spinner — Full Build")
st.caption("Build worlds, campaigns, and prompts from structured imagination.")

tab1, tab2 = st.tabs(["🎞 Single Universe", "🧩 Multi-Theme Batch"])

# -----------------------------------------------------------
# SINGLE UNIVERSE
# -----------------------------------------------------------
with tab1:
    st.subheader("Single Universe Generator")
    theme_input = st.text_input("Enter themes (comma-separated, optional):", "luxury, tech")
    if st.button("✨ Spin Universe"):
        themes = parse_themes(theme_input)
        code = generate_code(themes)
        decoded = decode_code(code)
        out = expand(decoded)

        st.subheader(f"Code: {'-'.join(map(str, code))}")
        st.caption(f"Themes used: {', '.join(themes) if themes else 'none (pure random)'}")
        with st.expander("Decoded Layers"):
            for k,v in decoded.items():
                st.write(f"**{k}:** {v}")
        for k,v in out.items():
            if k=="AI Image Prompt":
                st.markdown(f"**{k}:** `{v}`")
            else:
                st.markdown(f"### {k}\n{v}")

        buffer = StringIO()
        buffer.write(f"Creative Multiverse Universe\nCode: {'-'.join(map(str,code))}\nThemes: {', '.join(themes)}\n\n")
        for k,v in out.items():
            buffer.write(f"{k}\n{'-'*len(k)}\n{v}\n\n")
        st.download_button("💾 Download Universe (.txt)",buffer.getvalue().encode(),"creative_universe.txt")

# -----------------------------------------------------------
# MULTI-THEME BATCH
# -----------------------------------------------------------
with tab2:
    st.subheader("Batch Universe Pack")
    theme_input = st.text_input("Themes for pack (e.g. eco, luxury, mystic):","eco, luxury").strip()
    count = st.slider("How many universes to generate?",2,10,5)
    if st.button("🌐 Generate Pack"):
        themes = parse_themes(theme_input)
        universes=[]
        for _ in range(count):
            c=generate_code(themes);d=decode_code(c);o=expand(d)
            universes.append((c,d,o))

        for idx,(c,d,o) in enumerate(universes,1):
            st.markdown(f"## Universe {idx} — {o['Campaign Title']}")
            st.caption(f"Code: {'-'.join(map(str,c))}")
            st.caption(", ".join([f"{k}: {v}" for k,v in d.items()]))
            st.write(o["Movie Concept"])
            st.divider()

        buf=StringIO()
        buf.write("CREATIVE MULTIVERSE PACK\n"+"="*50+"\n")
        for i,(c,d,o) in enumerate(universes,1):
            buf.write(f"Universe {i} / Code: {'-'.join(map(str,c))}\n")
            for k,v in d.items(): buf.write(f"{k}: {v}\n")
            buf.write("\n")
            for k,v in o.items():
                buf.write(f"{k}\n{'~'*len(k)}\n{v}\n\n")
            buf.write("="*50+"\n")
        st.download_button("⬇️ Download Creative Pack",buf.getvalue().encode(),"creative_pack.txt")

st.markdown("---")
st.caption("© 2024 Creative Multiverse OS — Full App Build")
