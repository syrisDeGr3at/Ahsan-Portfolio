"""Generates Ahsan Rehman's portfolio pages into ../site."""
import html, json, pathlib

OUT = pathlib.Path(__file__).resolve().parent
REMOTE = "https://portfolio-seven-omega-25.vercel.app/"
LINKEDIN = "https://www.linkedin.com/in/muhammad-ahsan-a28b18326"
GITHUB = "https://github.com/m-ahsan139"
NAME = "Muhmmad Ahsan Rehman"
e = html.escape

DOORS = [
    dict(slug="legalmind", n="01", skill="AI Developer", short="AI Applications", proj="LegalMind AI",
         sub="Final-year team project · Applied AI", img="assets/legalmind/home.webp",
         alt="LegalMind AI home screen with conversation sidebar and suggested legal questions"),
    dict(slug="taskflow", n="02", skill="Web Developer", short="Web Development", proj="Taskflow",
         sub="Productivity · Web application", img="assets/taskflow.jpg",
         alt="Taskflow working application screenshot"),
    dict(slug="ledger", n="03", skill="Data Tools", short="Data Tools", proj="Ledger",
         sub="Data · Personal finance tool", img="assets/ledger.jpg",
         alt="Ledger working application screenshot"),
    dict(slug="textcraft", n="04", skill="Automation", short="Automation", proj="Textcraft",
         sub="Automation · Text processing", img="assets/textcraft.jpg",
         alt="Textcraft working application screenshot"),
]

def img(src, alt, eager=False, cls=""):
    return (f'<img src="{src}" alt="{e(alt)}"{"" if eager else " loading=\"lazy\""} decoding="async"{f" class=\"{cls}\"" if cls else ""} '
            f'onerror="this.onerror=null;this.src=\'{REMOTE}{src}\'">')

def head(title, desc, home=False):
    return f"""<!DOCTYPE html>
<html lang="en" data-mode="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="author" content="{NAME}">
<meta name="theme-color" content="#1A1818">
<meta property="og:type" content="profile">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{REMOTE}assets/ahsan-formal.webp">
<meta name="twitter:card" content="summary_large_image">
<script>try{{var m=localStorage.getItem('ahsan-mode');if(m)document.documentElement.dataset.mode=m}}catch(e){{}}
if(sessionStorage.getItem('ahsan-arrive')){{sessionStorage.removeItem('ahsan-arrive');document.documentElement.classList.add('arriving')}}
function pf(i){{var s=['assets/ahsan-formal.webp','{REMOTE}assets/ahsan-formal.webp'],k=+(i.dataset.k||0);i.classList.add('masked');if(k<s.length){{i.dataset.k=k+1;i.src=s[k]}}else{{i.onerror=null}}}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;1,400&family=Onest:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="vendor/lenis.css">
<link rel="stylesheet" href="css/style.css">

</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

SUN = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg>'

def header(current=None):
    links = [("index.html", "Home", current == "home")] + [(f'{d["slug"]}.html', d["short"], current == d["slug"]) for d in DOORS] + [("index.html#about", "My story", False), ("#contact", "Contact", False)]
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if c else ""}>{t}</a>' for h, t, c in links)
    menu = "".join(f'<li><a href="{d["slug"]}.html">{d["short"]}</a></li>' for d in DOORS)
    return f"""<header class="hdr"><div class="hdr-in">
  <a class="brand" href="index.html">Ahsan Rehman</a>
  <nav class="nav" aria-label="Main">{nav}</nav>
  <div class="hdr-r">
    <div class="tpill"><span class="mute">Local time</span><b data-t>—</b><i></i><span class="mute" data-d>—</span></div>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu <span class="burger"></span></button>
  </div>
</div></header>
<button class="rope" type="button" aria-label="Pull the cord to switch between light and dark mode"><span class="cord"></span><span class="bead"></span></button>
<nav class="menu" id="menu" aria-label="Menu">
  <ol>
    <li><a href="index.html">Home</a></li>
    {menu}
    <li><a href="index.html#about">My story</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
  <div class="menu-foot">
    <span><span class="dot"></span>&nbsp; Available for new opportunities</span>
    <span><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn ↗</a> &nbsp;·&nbsp; <a href="{GITHUB}" target="_blank" rel="noopener">GitHub ↗</a></span>
    <span>Local time <span data-time>—</span></span>
  </div>
</nav>
"""

CTA = f"""<section class="band cta" aria-labelledby="cta-h">
  <div class="wrap">
    <span class="pill" data-reveal><span class="dot"></span> Open to new opportunities</span>
    <h2 class="h2" id="cta-h" data-split>Have a role in mind? <span class="serif">Let’s make it happen.</span></h2>
    <p data-reveal>I’m open to software engineering roles, AI and automation projects, and MS scholarship opportunities. Tell me a little about it and we can take it from there.</p>
    <div class="cta-row" data-reveal>
      <a class="btn solid" href="#contact" data-hire>Hire me <span class="arr">→</span></a>
      <a class="btn" href="index.html#works">See my work</a>
    </div>
  </div>
</section>
"""

def footer():
    work = "".join(f'<li><a href="{d["slug"]}.html">{d["skill"]}</a></li>' for d in DOORS)
    return f"""<footer class="ftr">
  <div class="wrap">
    <div class="fgrid">
      <div><p class="fbig">Thoughtful software.<br><span class="serif mute">Practical AI.</span></p></div>
      <div><h4>Work</h4><ul>{work}</ul></div>
      <div><h4>Navigate</h4><ul><li><a href="index.html">Home</a></li><li><a href="index.html#about">My story</a></li><li><a href="#contact">Contact</a></li></ul></div>
      <div><h4>Connect</h4><ul><li><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn ↗</a></li><li><a href="{GITHUB}" target="_blank" rel="noopener">GitHub ↗</a></li></ul></div>
      <div><h4>Status</h4><ul><li><span class="dot"></span>&nbsp; Available for work</li><li>Mirpur, AJK, Pakistan</li><li>Local time <span data-time>—</span></li></ul></div>
    </div>
    <div class="fbot">
      <span>© 2026 {NAME}. Designed and built by Ahsan. · <a href="legal.html">Privacy &amp; credits</a></span>
      <a href="#top">Back to top ↑</a>
    </div>
  </div>
</footer>
<a class="totop" href="#top" aria-label="Back to top">↑</a>
"""

OPTS = ["An engineering role", "An MS or research opportunity", "An AI or automation project", "A web application", "A question about this site"]

def modal():
    opts = "".join(f'<button class="opt" type="button" data-v="{e(o)}" aria-pressed="false">{e(o)} <span>→</span></button>' for o in OPTS)
    nav = lambda last="Next": f'<div class="step-nav"><button class="btn" type="button" data-prev>← Back</button><button class="btn solid" type="button" data-next>{last} <span class="arr">→</span></button></div>'
    return f"""<div class="modal" id="contact-modal" role="dialog" aria-modal="true" aria-labelledby="c-title" aria-hidden="true">
  <div class="modal-bg" data-close></div>
  <div class="sheet">
    <div class="sheet-top"><span class="steps-count">1 of 5</span><button class="btn" type="button" data-close style="min-height:40px;padding:0 16px">Close</button></div>
    <div class="steps-bar"><i></i></div>
    <div class="step on">
      <h3 id="c-title">What do you need?</h3>
      <p>Pick the closest one. It shapes the message you’ll send.</p>
      <div class="opts">{opts}</div>
    </div>
    <div class="step">
      <h3>Tell me a little more</h3>
      <p>About: <b id="c-need-label">—</b></p>
      <label class="field">Details<textarea id="c-details"></textarea></label>
      <p class="err" aria-live="polite"></p>
      {nav()}
    </div>
    <div class="step">
      <h3>Where and when?</h3>
      <p>Both optional.</p>
      <label class="field">Location or remote arrangement<input id="c-where" autocomplete="off"></label>
      <label class="field">Timeline<input id="c-when" autocomplete="off" placeholder="For example, applications close in March"></label>
      {nav()}
    </div>
    <div class="step">
      <h3>Who’s reaching out?</h3>
      <p>So the message has a proper sign-off.</p>
      <label class="field">Your name<input id="c-name" autocomplete="name"></label>
      <label class="field">Company, university or team<input id="c-org" autocomplete="organization"></label>
      <label class="trap" aria-hidden="true">Leave this empty<input id="c-trap" tabindex="-1" autocomplete="off"></label>
      <p class="err" aria-live="polite"></p>
      {nav("Review")}
    </div>
    <div class="step">
      <h3>Ready to send</h3>
      <p>Ahsan takes messages on LinkedIn. This copies your message and opens his profile.</p>
      <div class="preview" id="c-preview"></div>
      <div class="step-nav"><button class="btn" type="button" data-prev>← Edit</button>
        <a class="btn solid" id="c-send" href="{LINKEDIN}" target="_blank" rel="noopener">Copy &amp; open LinkedIn <span class="arr">→</span></a></div>
    </div>
    <div class="step">
      <h3>Almost there</h3>
      <p id="c-copied" aria-live="polite"></p>
      <div class="preview" id="c-final"></div>
      <div class="step-nav"><a class="btn" href="{LINKEDIN}" target="_blank" rel="noopener">Open LinkedIn again ↗</a><button class="btn solid" type="button" data-close>Done</button></div>
    </div>
  </div>
</div>
"""

def tail(home=False):
    card = ""
    return f"""{modal()}
<script src="vendor/lenis.min.js"></script>
<script src="js/main.js"></script>
{card}
</body>
</html>
"""

# ---------------------------------------------------------------- home
def home():
    doors = "".join(f"""
      <a class="door" href="{d['slug']}.html" aria-label="{d['skill']}: {d['proj']}">
        <div class="door-in">{img(d['img'], d['alt'])}</div>
        <div class="leaf">
          <span class="knob"></span>
          <div class="n">{d['n']} / {len(DOORS):02d}</div>
          <div><div class="proj">{d['proj']}</div><h3>{d['skill']}</h3><p>{d['sub']}</p></div>
        </div>
      </a>""" for d in DOORS)
    story = [
        ("Now → Next", "Open to roles &amp; MS scholarships", "Software Engineer &amp; AI Developer · Mirpur, Pakistan",
         "Seeking engineering roles and MS opportunities in software engineering and applied AI, particularly retrieval-based systems, English–Urdu applications and the evaluation of intelligent software.",
         ["Trustworthy AI answers", "Bilingual applications", "Useful everyday workflows", "Reliable software"]),
        ("Final year", "LegalMind AI, final-year team project", "MUST Mirpur · supervised by Dr. Anum Tariq",
         "A bilingual Pakistan Laws RAG Assistant built with Momin Masood and Shaheer Ayyaz: section-aware retrieval, source citations and case workflows in a React and FastAPI application.",
         ["React", "FastAPI", "Pinecone", "MiniLM", "Gemini 2.5 Flash"]),
        ("Internship", "Intern at Moborid", "Professional experience",
         "Internship experience that formed part of my journey from university to professional work.", []),
        ("Internship", "Intern at WAPDA", "Certificate earned",
         "Completed an internship and earned an internship certificate.", []),
        ("2022 — 2026", "B.Sc. Software Engineering", "Mirpur University of Science and Technology (MUST)",
         "CGPA 3.25 / 4.00. PEC-recognised Level II programme in Mirpur, Azad Jammu &amp; Kashmir.",
         ["Web development", "Databases", "Machine learning", "Artificial intelligence", "Video editing"]),
    ]
    tl = "".join(f"""
        <li>
          <div class="when">{w}</div>
          <div><h3>{t}</h3><p class="where">{wh}</p><p>{p}</p>{('<ul class="chips">' + ''.join(f'<li>{c}</li>' for c in cs) + '</ul>') if cs else ''}</div>
        </li>""" for w, t, wh, p, cs in story)
    words = json.dumps(["a software engineer.", "an AI developer.", "building RAG systems.", "automating everyday work.", "always learning."])
    return head(f"{NAME} — Software Engineer & AI Developer",
                "Software Engineer & AI Developer from Mirpur, Pakistan. AI applications, web development and automation. Open to engineering roles and MS opportunities.", home=True) + f"""
<span id="top"></span>
{header("home")}
<main id="main">
  <section class="hero" aria-label="Introduction">
    <div class="hero-in">
      <div class="hero-txt">
        <div class="kicker" data-reveal><span class="dot"></span> Software Engineer &amp; AI Developer</div>
        <h1><span class="l1" data-split>Hi, I’m Ahsan.</span><span class="l2"><span data-split>I am</span> <span class="art" data-reveal>a</span></span><span class="sr">Software Engineer, AI Developer, Web Developer and Automation Builder.</span></h1>
        <div class="flip" aria-hidden="true" data-reveal>
          <div class="rings">{"<i></i>" * 12}</div>
          <div class="pages"><div class="page top"><span class="pt">Software Engineer</span></div><div class="page"><span class="pt"></span></div><span class="ct">01 / 04</span></div>
        </div>
        <div class="cta-row" data-reveal>
          <a class="btn solid hire" href="#contact" data-hire>Hire me <span class="circ"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></a>
          <a class="btn" href="#works">See my work</a>
        </div>
      </div>
      <div class="hero-pic" data-reveal>
        <img class="portrait" src="assets/ahsan-cutout.png" alt="Muhmmad Ahsan Rehman in a dark suit and white shirt" onerror="pf(this)" fetchpriority="high">
      </div>
    </div>
    <div class="hero-foot"><span><span class="dot" style="width:6px;height:6px"></span>&nbsp; Available for new opportunities</span><span class="mid">Mirpur, Pakistan · Open to MS scholarships</span><a href="#works">Scroll to explore <span>↓</span></a></div>
  </section>

  <section class="doors" id="works" aria-labelledby="works-h">
    <div class="pin">
      <div class="pin-in">
        <div class="wrap" style="width:100%">
          <div class="doors-head">
            <div>
              <div class="eyebrow">Selected work</div>
              <h2 class="h2" id="works-h" data-split>My work, <span class="serif">one door per skill.</span></h2>
              <p class="serif mute" data-reveal>Magic happens behind the doors.</p>
            </div>
            <div class="hint" data-reveal>Swipe along the wall <i></i></div>
          </div>
        </div>
        <div class="track">{doors}
          <div class="door-end"><p>Every door opens onto a working project.</p><a class="btn" href="{GITHUB}" target="_blank" rel="noopener">More on GitHub ↗</a></div>
        </div>
        <div class="wall-floor"><b></b></div>
      </div>
    </div>
  </section>

  <section class="band" id="about" aria-labelledby="about-h">
    <div class="wrap story">
      <div class="story-side">
        <div class="eyebrow">My story</div>
        <h2 class="h2" id="about-h" data-split>Let’s go back <span class="serif">in time.</span></h2>
        <p class="lead" data-reveal style="margin-top:22px">A MUST Mirpur graduate interested in AI applications, automation and software that makes information easier to use.</p>
        <div class="ruler" aria-hidden="true"><span>2022</span><span>2023</span><span>2024</span><span>2025</span><span>2026</span></div>
        <div class="ticks" aria-hidden="true"><b></b></div>
        <div class="counter" aria-hidden="true"><span class="cur">01</span><small>/ {len(story):02d}</small></div>
      </div>
      <ol class="tl">{tl}
      </ol>
    </div>
  </section>
{CTA}
</main>
{footer()}
""" + tail(home=True)

# ---------------------------------------------------------------- sub pages
def steps4(items):
    return '<div class="steps4">' + "".join(f'<div data-reveal><b>{n:02d}</b><h3>{t}</h3><p>{p}</p></div>' for n, (t, p) in enumerate(items, 1)) + '</div>'

def sec(k, title, body):
    return f"""<section class="sub-sec"><div class="wrap"><div class="sub-grid">
  <div><div class="k">{k}</div><h2 data-split>{title}</h2></div>
  <div class="prose" data-reveal>{body}</div>
</div></div></section>"""

def sub_page(d, label, title_tag, intro, tags, buttons, hero_img, body):
    i = DOORS.index(d); nx = DOORS[(i + 1) % len(DOORS)]
    tagh = "".join(f'<span class="chip">{t}</span>' for t in tags)
    return head(f"{d['proj']} — {NAME}", intro) + f"""<span id="top"></span>
{header(d['slug'])}
<main id="main">
  <section class="sub-hero"><div class="wrap">
    <a class="back" href="index.html#works">← Back to the doors</a>
    <div class="eyebrow">{d['n']} / {len(DOORS):02d} · {label}</div>
    <h1 data-split>{d['proj']}</h1>
    <p class="tag serif" data-reveal>{title_tag}</p>
    <p class="lead" data-reveal>{intro}</p>
    <div class="cta-row" data-reveal style="margin-bottom:22px">{buttons}</div>
    <div class="chips" data-reveal style="margin-bottom:50px">{tagh}</div>
    <div class="shot" data-reveal>{img(hero_img[0], hero_img[1], eager=True)}</div>
  </div></section>
  {body}
  <div class="wrap"><div class="next"><span class="mute">Next door</span><a href="{nx['slug']}.html">{nx['skill']} <span>→ {nx['proj']}</span></a></div></div>
{CTA}
</main>
{footer()}
""" + tail()

def legalmind():
    d = DOORS[0]
    shots = [
        ("home", "Conversation workspace", "Start a legal conversation, switch between cases, or choose a suggested question."),
        ("chat", "Grounded answers", "Read a response alongside the legal sources retrieved to support it."),
        ("citations", "Inspect the sources", "Expand the citation panel to inspect supporting legal passages."),
        ("urdu", "English & Urdu", "Explore the bilingual query-and-response workflow."),
        ("upload", "Case documents", "Upload documents within the context of a case."),
        ("intake", "Case intake", "Capture structured facts before generating a case summary."),
        ("draft", "Legal draft generator", "Choose a document type and provide the context for an assisted draft."),
        ("checklist", "Compliance & risk checklist", "Supply case context for an assisted checklist."),
    ]
    entries = "".join(f"""<div class="entry">
      <div data-reveal><div class="k mute">Screen {n:02d}</div><h3>{e(t)}</h3><p>{e(p)}</p></div>
      <div class="shot" data-reveal>{img(f'assets/legalmind/{s}.webp', 'LegalMind AI: ' + t)}</div>
    </div>""" for n, (s, t, p) in enumerate(shots, 1))
    body = sec("The problem", "Find the law. <span class='serif'>Understand the source.</span>",
               "<p>Legal documents are lengthy, and locating the right section can be difficult. LegalMind AI brings retrieval and a conversational interface together to help users explore Pakistani legal information in English and Urdu.</p>"
               "<p>The project includes case-based conversations, document upload, expandable citations, and workflows for case intake, draft generation and compliance checklists. When the available context does not sufficiently support an answer, a grounding check can trigger a refusal.</p>") + f"""
  <section class="sub-sec"><div class="wrap">
    <div class="k mute">How it works</div><h2 class="h2" data-split style="font-size:clamp(30px,4vw,56px)">From legal sections to <span class="serif">source-based answers.</span></h2>
    {steps4([("Prepare", "Organise documents into section-aware chunks and encode them with MiniLM embeddings."),
             ("Retrieve", "Search Pinecone for candidate passages and use a cross-encoder to rank them for the question."),
             ("Check", "Evaluate whether the retrieved context provides enough support to proceed."),
             ("Respond", "Use Gemini 2.5 Flash with the retrieved context and present citations in the chat interface.")])}
  </div></section>
  <section class="sub-sec"><div class="wrap">
    <div class="k mute">Product walkthrough</div><h2 class="h2" data-split style="font-size:clamp(30px,4vw,56px)">Inside the <span class="serif">application.</span></h2>
    <p class="note">Screenshots extracted from the project report.</p>
    <div style="margin-top:30px">{entries}</div>
  </div></section>
  <section class="sub-sec"><div class="wrap">
    <div class="k mute">Reported project evaluation</div><h2 class="h2" data-split style="font-size:clamp(30px,4vw,56px)">Results, <span class="serif">with their context.</span></h2>
    <div class="stats">
      <div data-reveal><b>129</b><span>Functional tests passed</span><p>The automated suite uses mocked external services; it checks application logic, not live service behaviour.</p></div>
      <div data-reveal><b>933 ms</b><span>Mean retrieval latency</span><p>36 samples in the development environment. Retrieval only; excludes Gemini answer generation.</p></div>
      <div data-reveal><b>83.3%</b><span>Retrieval recall@k</span><p>The correct statute was retrieved for 15 of 18 answerable questions. This does not measure final-answer accuracy.</p></div>
    </div>
    <p class="note">Source: project report, Chapters 7–8. Small evaluation sets and unrecorded benchmark hardware limit generalisation. Generated-answer quality was not scored automatically.</p>
  </div></section>
""" + sec("Project context", "A team <span class='serif'>effort.</span>",
          "<p>Developed by Muhammad Ahsan Rehman, Momin Masood and Shaheer Ayyaz at MUST, Mirpur, under the supervision of Dr. Anum Tariq.</p>"
          "<p>This case study describes the team’s application and report findings. A public project demo and source repository have not been provided.</p>"
          "<p>LegalMind AI supports access to legal information. Its generated content requires review and is not a substitute for professional legal advice.</p>") + f"""
  <section class="sub-sec"><div class="wrap">
    <div class="k mute">Engineering notes</div><h2 class="h2" data-split style="font-size:clamp(30px,4vw,56px)">Behind the <span class="serif">conversation.</span></h2>
    {steps4([("Two kinds of storage", "SQLite stores application records such as chat history, while Pinecone indexes embeddings for semantic retrieval."),
             ("Retrieval before generation", "Section-aware chunks retain the legal context. Passages are retrieved and reranked before the model receives them."),
             ("A grounding check", "Before answering, the system assesses whether the retrieved context gives enough support, and can refuse when it doesn’t."),
             ("An inspectable response", "Citations give the reader a route back to supporting passages; the source panel is part of the reading workflow.")])}
  </div></section>"""
    return sub_page(d, d["sub"], "Law, with context.",
                    "A final-year team project at MUST Mirpur: a bilingual Pakistan Laws RAG Assistant connecting conversational answers to legal source material.",
                    ["React", "FastAPI", "SQLite", "Pinecone", "MiniLM", "Gemini 2.5 Flash", "RAG"],
                    '<a class="btn solid" href="#contact" data-hire>Discuss this project <span class="arr">→</span></a>',
                    (d["img"], "Actual LegalMind AI conversation workspace from the project report"), body)

APPS = {
    "taskflow": dict(
        tag="A calmer way to organise work.", motto="Plan / Prioritise / Finish — a little structure, a lot more focus.",
        intro="A personal Kanban workspace for turning a list of tasks into visible progress. Capture priorities, move work between stages, and keep the next action clear.",
        tags=["JavaScript", "LocalStorage", "JSON export"],
        idea="<p>Tasks often end up scattered across notes. Taskflow brings them into one board with three simple stages: to do, in progress and done.</p><p>The application runs directly in the browser with no account required. Its scope is deliberately focused on an everyday workflow visitors can try immediately.</p>",
        how=[("Capture", "Add a task title and choose a priority without leaving the board."), ("Organise", "Move tasks between stages with an accessible status selector. Search by title to narrow the board."), ("Measure", "See total tasks, work in progress, completed tasks and a calculated completion percentage."), ("Keep", "Changes persist in this browser. Export a JSON snapshot to keep a separate copy.")],
        walk=[("Plan a learning session", "Add “Read the API guide”, choose a priority, and create a second task for “Build a small example”. The board turns a broad intention into individual actions."), ("Follow work through stages", "Move the first task into In progress, then Done. The summary reflects your board, making the relationship between active and completed work easy to inspect."), ("Keep a copy of the board", "Search for a task when the list grows. Export a JSON snapshot before clearing browser data or moving devices; the board does not sync between browsers.")],
        scope="Tasks stay in local storage on the current browser and device. Clearing browser data removes them; exports provide a portable copy. There is no account sync or shared workspace.",
        walk_title="Make the next action <span class='serif'>easy to see.</span>"),
    "ledger": dict(
        tag="Make everyday spending visible.", motto="Track / Understand / Export — your everyday spending, in perspective.",
        intro="A lightweight expense tracker with category filters, a visual spending breakdown and CSV export. Designed around quick entries and understandable totals.",
        tags=["JavaScript", "Data visualisation", "CSV export"],
        idea="<p>A list of transactions is useful only when it tells a clear story. Ledger groups everyday expenses and turns the current view into totals and category comparisons.</p><p>The application runs directly in the browser with no account required. Its scope is deliberately focused on an everyday workflow visitors can try immediately.</p>",
        how=[("Record", "Enter a description, positive amount, date and spending category."), ("Explore", "Filter the transaction list by category and see the summary update with it."), ("Understand", "Compare category totals through a bar chart and percentage breakdown."), ("Export", "Download the filtered records as CSV for use in a spreadsheet.")],
        walk=[("Capture the essentials", "Add a description, a positive amount in PKR, a date and a category. Small, consistent entries make the transaction list easier to review later."), ("Read the current view", "Choose a category to narrow the records. Compare the filtered total with the category breakdown; the chart describes the entries in the selected view."), ("Take the data with you", "Export the filtered records as CSV. The application uses local browser storage and does not connect to a bank or move data between devices.")],
        scope="Expenses stay in local storage on the current browser and device. Clearing browser data removes them; exports provide a portable copy. There is no account sync or shared workspace.",
        walk_title="From individual entries <span class='serif'>to a clearer picture.</span>"),
    "textcraft": dict(
        tag="Repeat the workflow. Skip the repetition.", motto="Clean / Transform / Reuse — messy text, beautifully organised.",
        intro="A configurable text-cleanup tool that turns repetitive editing into a reusable sequence of rules. Preview the output, copy it, or download a text file.",
        tags=["JavaScript", "Rule-based automation", "Text export"],
        idea="<p>Cleaning lists by hand takes repeated edits: remove blanks, tidy spaces, find duplicates. Textcraft applies selected operations in a consistent order and keeps the result visible beside the input.</p><p>The application runs directly in the browser with no account required. Its scope is deliberately focused on an everyday workflow visitors can try immediately.</p>",
        how=[("Input", "Paste a list, notes or other plain text into the input area."), ("Configure", "Choose whitespace cleanup, lowercase conversion, blank-line removal, deduplication, sorting or bullets."), ("Run", "Apply the selected rules and compare input and output character counts."), ("Use", "Copy the result or export a text file. A session history records the latest five runs.")],
        walk=[("Start with a repeated task", "Paste a list with extra spaces, blank lines or repeated entries. Keeping the original beside the result makes the transformation easier to review."), ("Select only useful changes", "Turn on whitespace cleanup, empty-line removal or deduplication as needed. Sorting, lowercase and bullets are optional operations for different outputs."), ("Review before you reuse", "Run the workflow and inspect the result. Copy it or download a text file; recent runs appear in the session history. These are deterministic rules, not AI-generated text.")],
        scope="Text is processed locally using deterministic rules, with no AI model or server request. Run history lasts for the current session; download any output you want to keep.",
        walk_title="Choose the rules. <span class='serif'>Inspect the result.</span>"),
}

def app_page(d):
    a = APPS[d["slug"]]
    walk = "".join(f'<div class="entry" style="grid-template-columns:120px minmax(0,1fr)"><div class="k mute">{n:02d}</div><div data-reveal><h3>{t}</h3><p>{p}</p></div></div>' for n, (t, p) in enumerate(a["walk"], 1))
    body = sec("The idea", "A small tool. <span class='serif'>A clear purpose.</span>", a["idea"]) + f"""
  <section class="sub-sec"><div class="wrap">
    <div class="k mute">How it works</div><h2 class="h2" data-split style="font-size:clamp(30px,4vw,56px)">From input to <span class="serif">useful output.</span></h2>
    {steps4(a["how"])}
  </div></section>
""" + sec("Implementation", "Simple interactions. <span class='serif'>Visible results.</span>",
          "<p>Semantic HTML provides the structure, responsive CSS adapts the layout, and JavaScript handles the application state and interactions. Exports are generated locally in the browser.</p>"
          f"<p><b>Data and scope.</b> {a['scope']}</p>") + f"""
  <section class="sub-sec"><div class="wrap">
    <div class="k mute">A practical walkthrough</div><h2 class="h2" data-split style="font-size:clamp(30px,4vw,56px)">{a['walk_title']}</h2>
    <div style="margin-top:30px">{walk}</div>
    <div class="cta-row" style="margin-top:40px"><a class="btn solid" href="apps/{d['slug']}.html" target="_blank" rel="noopener">Try {d['proj']} yourself <span class="arr">↗</span></a></div>
  </div></section>"""
    return sub_page(d, d["sub"], a["tag"], a["intro"], a["tags"],
                    f'<a class="btn solid" href="apps/{d["slug"]}.html" target="_blank" rel="noopener">Open working app <span class="arr">↗</span></a><span class="mute serif" style="align-self:center">{a["motto"]}</span>',
                    (d["img"], f"{d['proj']} working application screenshot with illustrative sample content"), body)

def legal():
    rows = [("Lenis 1.3.23", "© darkroom.engineering", "Smooth scrolling on desktop", "MIT"),
            ("Onest", "© The Onest Project Authors", "The site’s typeface", "SIL Open Font License 1.1"),
            ("EB Garamond", "© The EB Garamond Project Authors", "Captions and accents", "SIL Open Font License 1.1")]
    tr = "".join(f"<tr><td><b>{a}</b><br><span class='mute'>{b}</span></td><td>{c}</td><td>{l}</td></tr>" for a, b, c, l in rows)
    return head(f"Privacy & credits — {NAME}", "Privacy notes and open-source credits for Ahsan Rehman's portfolio.") + f"""<span id="top"></span>
{header()}
<main id="main" class="legal">
  <section class="sub-hero"><div class="wrap">
    <a class="back" href="index.html">← Back home</a>
    <h1 data-split style="font-size:clamp(44px,7vw,100px)">Privacy &amp; credits</h1>
  </div></section>
  <section class="sub-sec"><div class="wrap"><div class="sub-grid">
    <div><h2>Privacy</h2></div>
    <div class="prose">
      <p>This site sets no cookies and runs no analytics.</p>
      <p>It saves one item in your browser’s local storage, <code>ahsan-mode</code>, to remember your light or dark choice, and a short-lived session flag, <code>ahsan-arrive</code>, that plays the door transition when you open a project.</p>
      <p>The contact form doesn’t send anything to a server. It writes a message for you, copies it, and opens LinkedIn so you can send it yourself.</p>
      <p>The working apps (Taskflow, Ledger, Textcraft) keep their data in your own browser only.</p>
    </div>
  </div></div></section>
  <section class="sub-sec"><div class="wrap"><div class="sub-grid">
    <div><h2>Credits</h2></div>
    <div class="prose">
      <table><thead><tr><th>Name</th><th>Used for</th><th>Licence</th></tr></thead><tbody>{tr}</tbody></table>
      <p>Layout and interaction concept inspired by Rishi Thakor’s portfolio (therishithakor.com).</p>
      <p>Photographs and project screenshots are © {NAME} and the LegalMind AI team.</p>
    </div>
  </div></div></section>
</main>
{footer()}
""" + tail()

if __name__ == "__main__":
    (OUT / "index.html").write_text(home(), encoding="utf-8")
    (OUT / "legalmind.html").write_text(legalmind(), encoding="utf-8")
    for d in DOORS[1:]:
        (OUT / f"{d['slug']}.html").write_text(app_page(d), encoding="utf-8")
    (OUT / "legal.html").write_text(legal(), encoding="utf-8")
    print("built", sorted(p.name for p in OUT.glob("*.html")))
