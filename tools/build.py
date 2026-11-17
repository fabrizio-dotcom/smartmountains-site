#!/usr/bin/env python3
"""
Smart Mountains static site generator (optional).

The deployable site is the plain HTML already committed in /public.
Run this only if you want to change shared parts (header, footer, copy in both
languages) in one place:

    python3 tools/build.py

It rewrites the HTML files in /public. It never touches /public/assets.
No dependencies beyond Python 3.8+.
"""
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public"
SITE = "https://smartmountains.net"
MAIL = "hello@smartmountains.net"
CALENDLY = "https://calendly.com/fabcamp/fab"
FAB = "https://www.fabcampaigns.com"
YEAR = "2026"

# ---------------------------------------------------------------- artwork

def ridge(seed, base, amp, width=1440, steps=7, rough=0.55):
    """Midpoint-displacement ridgeline. Returns a list of (x, y)."""
    rnd = random.Random(seed)
    n = 2 ** steps
    ys = [0.0] * (n + 1)
    ys[0] = rnd.uniform(-amp, amp) * 0.5
    ys[n] = rnd.uniform(-amp, amp) * 0.5
    span, scale = n, amp
    while span > 1:
        half = span // 2
        for i in range(half, n, span):
            ys[i] = (ys[i - half] + ys[i + half]) / 2 + rnd.uniform(-scale, scale)
        span, scale = half, scale * rough
    return [(round(i * width / n, 1), round(base + ys[i], 1)) for i in range(n + 1)]


def path_fill(points, bottom=700, width=1440):
    d = "M0 %s " % bottom + " ".join("L%s %s" % p for p in points) + " L%s %s Z" % (width, bottom)
    return d


def hero_art():
    far = ridge(11, 380, 110)
    mid = ridge(23, 450, 90)
    near = ridge(37, 535, 70)
    front = ridge(51, 650, 30, rough=0.5)
    # sensor markers placed on the near ridge, just below the crest
    picks = [int(len(near) * f) for f in (0.22, 0.41, 0.63, 0.82)]
    marks = []
    for k, idx in enumerate(picks):
        x, y = near[idx]
        y += 26
        marks.append(
            '<g class="sensor"><circle class="sensor-ring d%d" cx="%s" cy="%s" r="7" fill="none" stroke="#E07D2C" stroke-width="2"/>'
            '<circle cx="%s" cy="%s" r="4.5" fill="#E07D2C"/></g>' % (k + 1, x, y, x, y)
        )
    line = " ".join("%s,%s" % (near[i][0], near[i][1] + 26) for i in picks)
    return (
        '<svg class="art" viewBox="0 0 1440 700" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">'
        '<path d="%s" fill="#1E3D58"/>'
        '<path d="%s" fill="#16304A"/>'
        '<path d="%s" fill="#0F2238"/>'
        '<polyline points="%s" fill="none" stroke="#E07D2C" stroke-opacity=".55" stroke-width="1.5" stroke-dasharray="3 7"/>'
        "%s"
        '<path d="%s" fill="#F6F4EF"/>'
        "</svg>"
    ) % (path_fill(far), path_fill(mid), path_fill(near), line, "".join(marks), path_fill(front))


def contour_art():
    """Soft topographic contour lines for inner page heroes."""
    import math
    rnd = random.Random(5)
    cx, cy = 1050, 220
    paths = []
    phases = [rnd.uniform(0, 6.28) for _ in range(4)]
    for r in range(40, 560, 38):
        pts = []
        for a in range(0, 361, 6):
            t = math.radians(a)
            wob = (
                1
                + 0.10 * math.sin(2 * t + phases[0])
                + 0.07 * math.sin(3 * t + phases[1])
                + 0.04 * math.sin(5 * t + phases[2])
            )
            rr = r * wob
            pts.append((cx + rr * 1.5 * math.cos(t), cy + rr * 0.62 * math.sin(t)))
        d = "M" + " L".join("%.1f %.1f" % p for p in pts) + "Z"
        paths.append('<path d="%s"/>' % d)
    return (
        '<svg class="contours" viewBox="0 0 1440 440" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
        '<g fill="none" stroke="#7FCBA4" stroke-opacity=".28" stroke-width="1">%s</g></svg>' % "".join(paths)
    )


LOGO = (
    '<svg viewBox="0 0 40 40" aria-hidden="true" focusable="false">'
    '<path d="M3 31 L15 11 L21 21 L26 14 L37 31 Z" fill="none" stroke="#7FCBA4" stroke-width="2.2" stroke-linejoin="round"/>'
    '<circle cx="26" cy="9" r="3.2" fill="#E07D2C"/></svg>'
)

FAVICON = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
    '<rect width="64" height="64" rx="12" fill="#0A1628"/>'
    '<path d="M8 48 L24 20 L32 33 L40 23 L56 48 Z" fill="none" stroke="#7FCBA4" stroke-width="4" stroke-linejoin="round"/>'
    '<circle cx="42" cy="14" r="5" fill="#E07D2C"/></svg>'
)

# ---------------------------------------------------------------- copy

T = {
    "en": {
        "lang": "en",
        "home_url": "/",
        "nav": [("/", "Home"), ("/about/", "About"), ("/next-generation/", "Next Generation"), ("/partner-with-us/", "Partner With Us")],
        "other_label": "Italiano",
        "other_code": "IT",
        "skip": "Skip to content",
        "menu": "Menu",
        "tagline": "A Fab Campaigns concept",
        "footer_line": "Monitoring infrastructure for mountain territories, built with the people who live there.",
        "fab_link": "Fab Campaigns",
        "legal": "&copy; %s Fab Campaigns Ltd. Registered in England and Wales, company number 10302961." % YEAR,
        "flinks_title": "Contact",
    },
    "it": {
        "lang": "it",
        "home_url": "/it/",
        "nav": [("/it/", "Home"), ("/it/chi-siamo/", "Chi siamo"), ("/it/nuova-generazione/", "Nuova generazione"), ("/it/partner/", "Collabora")],
        "other_label": "English",
        "other_code": "EN",
        "skip": "Vai al contenuto",
        "menu": "Menu",
        "tagline": "Un concept di Fab Campaigns",
        "footer_line": "Infrastrutture di monitoraggio per i territori di montagna, costruite con chi li abita.",
        "fab_link": "Fab Campaigns",
        "legal": "&copy; %s Fab Campaigns Ltd. Registrata in Inghilterra e Galles, numero 10302961." % YEAR,
        "flinks_title": "Contatti",
    },
}

# ---------------------------------------------------------------- page bodies

def home_en():
    return {
        "title": "Smart Mountains | Monitoring infrastructure for mountain territories",
        "desc": "Mountain territories carry risk they cannot yet see. Smart Mountains, a Fab Campaigns concept, builds slope-monitoring infrastructure with the territory, starting in the Alps.",
        "hero": """
<header class="hero">
  %(art)s
  <div class="wrap">
    <p class="eyebrow">A Fab Campaigns concept</p>
    <h1>Mountain territories carry risk they cannot yet see.</h1>
    <p class="lede">Landslides, debris flows and failing infrastructure are moving faster than the monitoring built to watch them. Smart Mountains is a way to close that gap: monitoring infrastructure built and run with the territory, starting with slope movement in the Alps.</p>
    <div class="btns">
      <a class="btn" href="/partner-with-us/">Start a conversation</a>
      <a class="btn ghost" href="#approach">How it works</a>
    </div>
  </div>
</header>""",
        "body": """
<section id="problem">
  <div class="wrap split">
    <div>
      <p class="kicker">The problem</p>
      <h2>Decisions are made on incomplete data</h2>
      <p class="measure">Municipalities, civil protection, park authorities and infrastructure operators make choices about roads, settlements and water with partial information. A satellite pass here, a manual survey there, a forecast that stops at the valley floor. Each source tells part of the story, and none of them was designed to work with the others.</p>
    </div>
    <p class="pull">The data exists. The system that turns it into a local decision mostly does not.</p>
  </div>
</section>

<section id="approach" class="alt">
  <div class="wrap">
    <p class="kicker">How it works</p>
    <h2>Monitor, predict, act</h2>
    <div class="cols">
      <article class="card"><span class="num">01</span><h3>Monitor</h3><p>Satellite radar (InSAR, Sentinel-1) shows ground movement across a whole slope. Corner reflectors and ground sensors confirm it where it matters and cover what the radar cannot see.</p></article>
      <article class="card"><span class="num">02</span><h3>Predict</h3><p>Models are calibrated to each territory, its history and its measurements on the ground, so a signal can be read as a trend instead of an alarm.</p></article>
      <article class="card"><span class="num">03</span><h3>Act</h3><p>Civil protection, municipalities and infrastructure managers receive decision support with the evidence behind it, and can see how sure we are.</p></article>
    </div>
  </div>
</section>

<section id="model" class="dark">
  <div class="wrap">
    <p class="kicker">The model</p>
    <h2>Infrastructure, owned with the territory</h2>
    <p class="measure">Smart Mountains is built as infrastructure, not sold as software. The value sits in a monitoring network that stays in place, run by people who live there.</p>
    <div class="cols four">
      <article class="card on-dark"><h3>Built locally</h3><p>Each site is set up with local partners, through a local joint venture or business network, so the cost of switching it on becomes local work and training.</p></article>
      <article class="card on-dark"><h3>Long horizons</h3><p>Service agreements run for years, not weeks. What we offer is a network and the continuity that keeps it reliable.</p></article>
      <article class="card on-dark"><h3>Data stays local</h3><p>We do not sell data. Local authorities keep control of what is measured on their land.</p></article>
      <article class="card on-dark"><h3>A profession for the valley</h3><p>Running a network takes hydraulics, electronics and geomatics. We want to grow that skill set locally, with schools, universities and training bodies, as a new Alpine profession: the territory steward. <a href="/next-generation/">Read more</a></p></article>
    </div>
  </div>
</section>

<div class="band">
  <div class="wrap split">
    <h2>We say what we cannot see.</h2>
    <p>Radar has blind spots. Steep, wooded or snow-covered slopes can lose signal, and some areas have no historical archive. Every site brief states what is covered, what is not, and what we will check on the ground.</p>
  </div>
</div>

<section id="territories">
  <div class="wrap">
    <p class="kicker">Territories</p>
    <h2>Where we are working</h2>
    <p class="measure">Three mountain regions shape the first work. We name individual sites once the local authority agrees.</p>
    <div class="cols">
      <article class="card"><span class="tag">Pilot design</span><h3>Dolomiti Bellunesi, Veneto</h3><p>Slope stability and early warning for municipalities in and around the national park.</p></article>
      <article class="card"><span class="tag">Exploring</span><h3>Valtellina, Lombardy</h3><p>Slope and debris-flow risk along a valley with dense infrastructure and hydropower.</p></article>
      <article class="card"><span class="tag">Exploring</span><h3>Swiss Alps, Valais</h3><p>Debris-flow research here goes back decades. We are learning from it before we propose anything.</p></article>
    </div>
  </div>
</section>

<section class="cta">
  <div class="wrap">
    <h2>Describe your territory.</h2>
    <p>If you manage land, infrastructure or water in mountain terrain, tell us about it. We choose pilot territories carefully, and we start with a conversation.</p>
    <div class="btns"><a class="btn" href="/partner-with-us/">Partner with us</a></div>
  </div>
</section>""",
    }


def home_it():
    return {
        "title": "Smart Mountains | Infrastrutture di monitoraggio per i territori di montagna",
        "desc": "I territori di montagna convivono con rischi che ancora non vedono. Smart Mountains, un concept di Fab Campaigns, costruisce con il territorio infrastrutture di monitoraggio dei versanti, a partire dalle Alpi.",
        "hero": """
<header class="hero">
  %(art)s
  <div class="wrap">
    <p class="eyebrow">Un concept di Fab Campaigns</p>
    <h1>I territori di montagna convivono con rischi che ancora non riescono a vedere.</h1>
    <p class="lede">Frane, colate detritiche e infrastrutture sotto stress si muovono più in fretta del monitoraggio costruito per osservarle. Smart Mountains è un modo per colmare questo vuoto: infrastrutture di monitoraggio costruite e gestite insieme al territorio, a partire dal movimento dei versanti sulle Alpi.</p>
    <div class="btns">
      <a class="btn" href="/it/partner/">Avvia un confronto</a>
      <a class="btn ghost" href="#approccio">Come funziona</a>
    </div>
  </div>
</header>""",
        "body": """
<section id="problema">
  <div class="wrap split">
    <div>
      <p class="kicker">Il problema</p>
      <h2>Si decide con dati incompleti</h2>
      <p class="measure">Comuni, protezione civile, enti parco e gestori di infrastrutture decidono su strade, abitati e acqua con informazioni parziali. Un passaggio satellitare qui, un rilievo manuale là, una previsione che si ferma al fondovalle. Ogni fonte racconta una parte della storia e nessuna è stata pensata per funzionare con le altre.</p>
    </div>
    <p class="pull">I dati esistono. Il sistema che li trasforma in una decisione locale, per lo più, no.</p>
  </div>
</section>

<section id="approccio" class="alt">
  <div class="wrap">
    <p class="kicker">Come funziona</p>
    <h2>Monitorare, prevedere, agire</h2>
    <div class="cols">
      <article class="card"><span class="num">01</span><h3>Monitorare</h3><p>Il radar satellitare (InSAR, Sentinel-1) mostra il movimento del terreno su un intero versante. Riflettori d’angolo e sensori a terra lo confermano dove serve e coprono ciò che il radar non vede.</p></article>
      <article class="card"><span class="num">02</span><h3>Prevedere</h3><p>I modelli sono calibrati su ogni territorio, sulla sua storia e sulle misure a terra, così un segnale si legge come tendenza e non come allarme.</p></article>
      <article class="card"><span class="num">03</span><h3>Agire</h3><p>Protezione civile, comuni e gestori di infrastrutture ricevono un supporto alle decisioni con le prove che lo sostengono, e vedono quanto siamo sicuri.</p></article>
    </div>
  </div>
</section>

<section id="modello" class="dark">
  <div class="wrap">
    <p class="kicker">Il modello</p>
    <h2>Un’infrastruttura costruita con il territorio</h2>
    <p class="measure">Smart Mountains nasce come infrastruttura, non come software da vendere. Il valore sta in una rete di monitoraggio che resta sul posto, gestita da chi vive lì.</p>
    <div class="cols four">
      <article class="card on-dark"><h3>Costruita sul posto</h3><p>Ogni sito nasce con partner locali, attraverso una joint venture o una rete d’impresa, così il costo di attivazione diventa lavoro e formazione sul territorio.</p></article>
      <article class="card on-dark"><h3>Orizzonti lunghi</h3><p>I contratti di servizio durano anni, non settimane. Offriamo una rete e la continuità che la mantiene affidabile.</p></article>
      <article class="card on-dark"><h3>I dati restano locali</h3><p>Non vendiamo dati. Le amministrazioni locali mantengono il controllo di ciò che si misura sul loro territorio.</p></article>
      <article class="card on-dark"><h3>Un mestiere per la valle</h3><p>Gestire una rete richiede idraulica, elettronica e geomatica. Vogliamo far crescere queste competenze sul posto, con scuole, università ed enti di formazione, come nuovo mestiere alpino: il <em>custode del territorio</em>. <a href="/it/nuova-generazione/">Approfondisci</a></p></article>
    </div>
  </div>
</section>

<div class="band">
  <div class="wrap split">
    <h2>Diciamo ciò che non riusciamo a vedere.</h2>
    <p>Il radar ha punti ciechi. I versanti ripidi, boscati o innevati possono perdere il segnale e alcune aree non hanno un archivio storico. Ogni scheda di sito dichiara cosa è coperto, cosa no e cosa verificheremo sul campo.</p>
  </div>
</div>

<section id="territori">
  <div class="wrap">
    <p class="kicker">Territori</p>
    <h2>Dove lavoriamo</h2>
    <p class="measure">Tre regioni di montagna orientano il primo lavoro. Indichiamo i singoli siti solo dopo l’accordo dell’amministrazione locale.</p>
    <div class="cols">
      <article class="card"><span class="tag">Progetto pilota</span><h3>Dolomiti Bellunesi, Veneto</h3><p>Stabilità dei versanti e allerta precoce per i comuni dentro e intorno al parco nazionale.</p></article>
      <article class="card"><span class="tag">In esplorazione</span><h3>Valtellina, Lombardia</h3><p>Rischio da frana e colata detritica lungo una valle con molte infrastrutture e impianti idroelettrici.</p></article>
      <article class="card"><span class="tag">In esplorazione</span><h3>Alpi svizzere, Vallese</h3><p>La ricerca sulle colate detritiche qui ha decenni di storia. Prima di proporre qualcosa, impariamo da essa.</p></article>
    </div>
  </div>
</section>

<section class="cta">
  <div class="wrap">
    <h2>Descrivi il tuo territorio.</h2>
    <p>Se gestisci territorio, infrastrutture o acqua in ambiente montano, raccontacelo. Scegliamo con cura i territori pilota e partiamo da una conversazione.</p>
    <div class="btns"><a class="btn" href="/it/partner/">Collabora con noi</a></div>
  </div>
</section>""",
    }


def about_en():
    return {
        "title": "About | Smart Mountains, a Fab Campaigns concept",
        "desc": "Smart Mountains is a concept built inside Fab Campaigns: slope-monitoring infrastructure for mountain territories, tested with real territories first.",
        "hero": """
<header class="page-hero">
  %(contours)s
  <div class="wrap">
    <p class="eyebrow">About</p>
    <h1>A concept built inside Fab Campaigns</h1>
    <p class="lede">The technology to watch an Alpine slope is mature. The partnerships and local structures that put it to work are not. Fab Campaigns designs partnerships. Smart Mountains is where that work meets a physical problem.</p>
  </div>
</header>""",
        "body": """
<section>
  <div class="wrap split">
    <div>
      <p class="kicker">Why here</p>
      <h2>Why it lives in Fab Campaigns</h2>
      <p>Fab Campaigns is a partnership studio and incubator based in Winchester, UK. It builds the agreements, governance and shared structures that let organisations with different interests work on one asset.</p>
      <p>Smart Mountains applies that method to monitoring infrastructure in mountain territories. It brings a territory, technology providers, training bodies and funders around a single network, and keeps the arrangement clear for each of them.</p>
      <p><a href="%(fab)s" rel="noopener">Visit Fab Campaigns</a></p>
    </div>
    <p class="pull">A concept first, so it can be tested with real territories before it carries the weight of a company.</p>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <p class="kicker">How it grows</p>
    <h2>One territory, then more, then its own form</h2>
    <ol class="steps">
      <li><div><h3>Prove it in one territory</h3><p>Start with one site, one local authority and a small group of partners. Show what the network sees and what it changes.</p></div></li>
      <li><div><h3>Add territories and technology partners</h3><p>Repeat what worked, with technology chosen for each place instead of fixed in advance.</p></div></li>
      <li><div><h3>Take its own form when needed</h3><p>If the work calls for its own structure, Smart Mountains will take one. Until then it stays inside Fab Campaigns, which keeps it light.</p></div></li>
    </ol>
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <p class="kicker">Technology</p>
    <h2>Technology, chosen per territory</h2>
    <div class="cols">
      <article class="card on-dark"><span class="num">01</span><h3>Satellite radar</h3><p>Interferometric radar (InSAR) detects ground movement at millimetre scale over wide areas, using Sentinel-1 data from the European Copernicus programme.</p></article>
      <article class="card on-dark"><span class="num">02</span><h3>Ground sensing</h3><p>Corner reflectors give the radar a fixed target to measure against. Ground sensors add what satellites cannot see: soil moisture, slope movement, water flow.</p></article>
      <article class="card on-dark"><span class="num">03</span><h3>Territory models</h3><p>Models are trained on each place’s own history, calibrated on site, then tested against what happens on the slope.</p></article>
    </div>
    <p class="note">We work with sensor makers, data providers and modelling specialists. Collaborations are set up through framework agreements, so each party knows its role and what it shares.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <p class="kicker">Incubation</p>
    <h2>Built with partners in the Alps</h2>
    <div class="cols four">
      <article class="card"><h3>Fab Campaigns, Winchester</h3><p>Partnership studio and incubator. <a href="%(fab)s" rel="noopener">fabcampaigns.com</a></p></article>
      <article class="card"><h3>Imprese Favolose, Belluno</h3><p>Territorial incubator for Alpine climate technology.</p></article>
    </div>
  </div>
</section>

<section class="cta">
  <div class="wrap">
    <h2>This is built to work on a slope, not on a slide.</h2>
    <p>If you manage land, infrastructure or investments in mountain environments, we would like to hear how your territory works.</p>
    <div class="btns"><a class="btn" href="/partner-with-us/">Partner with us</a></div>
  </div>
</section>""",
    }


def about_it():
    return {
        "title": "Chi siamo | Smart Mountains, un concept di Fab Campaigns",
        "desc": "Smart Mountains è un concept nato dentro Fab Campaigns: infrastrutture di monitoraggio dei versanti per i territori di montagna, messe alla prova prima con territori reali.",
        "hero": """
<header class="page-hero">
  %(contours)s
  <div class="wrap">
    <p class="eyebrow">Chi siamo</p>
    <h1>Un concept nato dentro Fab Campaigns</h1>
    <p class="lede">La tecnologia per osservare un versante alpino è matura. Mancano le alleanze e le strutture locali che la mettono al lavoro. Fab Campaigns progetta partnership. Smart Mountains è il punto in cui questo lavoro incontra un problema fisico.</p>
  </div>
</header>""",
        "body": """
<section>
  <div class="wrap split">
    <div>
      <p class="kicker">Perché qui</p>
      <h2>Perché vive dentro Fab Campaigns</h2>
      <p>Fab Campaigns è uno studio di partnership e incubatore con sede a Winchester, nel Regno Unito. Costruisce gli accordi, la governance e le strutture condivise che permettono a organizzazioni con interessi diversi di lavorare su un unico bene.</p>
      <p>Smart Mountains applica questo metodo alle infrastrutture di monitoraggio nei territori di montagna. Riunisce un territorio, fornitori di tecnologia, enti di formazione e finanziatori attorno a un’unica rete e mantiene chiaro l’accordo per ciascuno.</p>
      <p><a href="%(fab)s" rel="noopener">Visita Fab Campaigns</a></p>
    </div>
    <p class="pull">Prima un concept, per metterlo alla prova con territori reali prima che porti il peso di un’azienda.</p>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <p class="kicker">Come cresce</p>
    <h2>Un territorio, poi altri, poi una forma propria</h2>
    <ol class="steps">
      <li><div><h3>Dimostrarlo in un territorio</h3><p>Partire da un sito, un’amministrazione locale e un gruppo ristretto di partner. Mostrare cosa vede la rete e cosa cambia.</p></div></li>
      <li><div><h3>Aggiungere territori e partner tecnologici</h3><p>Ripetere ciò che ha funzionato, con tecnologie scelte per ogni luogo e non fissate in anticipo.</p></div></li>
      <li><div><h3>Prendere una forma propria quando serve</h3><p>Se il lavoro richiede una struttura propria, Smart Mountains ne assumerà una. Fino ad allora resta dentro Fab Campaigns, che la mantiene leggera.</p></div></li>
    </ol>
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <p class="kicker">Tecnologia</p>
    <h2>Tecnologia scelta per ogni territorio</h2>
    <div class="cols">
      <article class="card on-dark"><span class="num">01</span><h3>Radar satellitare</h3><p>Il radar interferometrico (InSAR) rileva movimenti del terreno a scala millimetrica su aree vaste, usando i dati Sentinel-1 del programma europeo Copernicus.</p></article>
      <article class="card on-dark"><span class="num">02</span><h3>Sensori a terra</h3><p>I riflettori d’angolo offrono al radar un bersaglio fisso con cui misurare. I sensori a terra aggiungono ciò che i satelliti non vedono: umidità del suolo, movimento del versante, portata d’acqua.</p></article>
      <article class="card on-dark"><span class="num">03</span><h3>Modelli per territorio</h3><p>I modelli sono addestrati sulla storia di ciascun luogo, calibrati sul campo e verificati con ciò che accade sul versante.</p></article>
    </div>
    <p class="note">Lavoriamo con produttori di sensori, fornitori di dati e specialisti di modellistica. Le collaborazioni si definiscono con accordi quadro, così ogni parte conosce il proprio ruolo e cosa condivide.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <p class="kicker">Incubazione</p>
    <h2>Costruita con partner nelle Alpi</h2>
    <div class="cols four">
      <article class="card"><h3>Fab Campaigns, Winchester</h3><p>Studio di partnership e incubatore. <a href="%(fab)s" rel="noopener">fabcampaigns.com</a></p></article>
      <article class="card"><h3>Imprese Favolose, Belluno</h3><p>Incubatore territoriale per le tecnologie climatiche alpine.</p></article>
    </div>
  </div>
</section>

<section class="cta">
  <div class="wrap">
    <h2>Nasce per funzionare su un versante, non su una slide.</h2>
    <p>Se gestisci territorio, infrastrutture o investimenti in ambiente montano, vorremmo sapere come funziona il tuo territorio.</p>
    <div class="btns"><a class="btn" href="/it/partner/">Collabora con noi</a></div>
  </div>
</section>""",
    }


def partner_en():
    return {
        "title": "Partner With Us | Smart Mountains",
        "desc": "Territories, technology partners, funders and local partners: how to work with Smart Mountains, a Fab Campaigns concept for mountain monitoring infrastructure.",
        "hero": """
<header class="page-hero">
  %(contours)s
  <div class="wrap">
    <p class="eyebrow">Partner with us</p>
    <h1>Every territory is different.</h1>
    <p class="lede">We do not deploy a generic platform. We build with local partners, around the risks of one specific place, and plan for the long term.</p>
  </div>
</header>""",
        "body": """
<section>
  <div class="wrap">
    <p class="kicker">Ways to work together</p>
    <h2>Four ways in</h2>
    <div class="cols four">
      <article class="card"><span class="num">01</span><h3>Territories</h3><p>For municipalities, national parks, civil protection bodies, mountain communities and operators of roads, water or hydropower who want to see slope movement before it becomes an emergency.</p></article>
      <article class="card"><span class="num">02</span><h3>Technology partners</h3><p>For sensor makers, satellite data providers and modelling specialists who want their work to run inside a real territorial network, with a clear role and clear terms.</p></article>
      <article class="card"><span class="num">03</span><h3>Schools, universities and training bodies</h3><p>For technical schools, universities and vocational training bodies that want to build the pathway for the territory steward and teach on live sites. <a href="/next-generation/">About the pathway</a></p></article>
      <article class="card"><span class="num">04</span><h3>Funders and local partners</h3><p>For public funding programmes, foundations, investors and local development bodies interested in long-term environmental infrastructure. Conversations run through Fab Campaigns.</p></article>
    </div>
  </div>
</section>

<section class="alt" id="contact">
  <div class="wrap split">
    <div>
      <p class="kicker">Start a conversation</p>
      <h2>Tell us about your territory</h2>
      <p>A short email is enough. It helps us to know:</p>
      <ul class="clean">
        <li>where the territory is</li>
        <li>what is at stake there: settlements, roads, water, tourism</li>
        <li>what monitoring exists today</li>
      </ul>
      <p class="note">We reply in English or Italian.</p>
    </div>
    <div class="contact-box">
      <p class="kicker">Write to us</p>
      <p><a class="mail" href="mailto:%(mail)s">%(mail)s</a></p>
      <p>Or pick a time that suits you.</p>
      <div class="btns"><a class="btn dark" href="%(cal)s" rel="noopener">Book a call</a></div>
    </div>
  </div>
</section>""",
    }


def partner_it():
    return {
        "title": "Collabora | Smart Mountains",
        "desc": "Territori, partner tecnologici, finanziatori e partner locali: come collaborare con Smart Mountains, un concept di Fab Campaigns per infrastrutture di monitoraggio in montagna.",
        "hero": """
<header class="page-hero">
  %(contours)s
  <div class="wrap">
    <p class="eyebrow">Collabora con noi</p>
    <h1>Ogni territorio è diverso.</h1>
    <p class="lede">Non installiamo una piattaforma generica. Costruiamo con partner locali, attorno ai rischi di un luogo preciso, con una visione di lungo periodo.</p>
  </div>
</header>""",
        "body": """
<section>
  <div class="wrap">
    <p class="kicker">Come lavorare insieme</p>
    <h2>Quattro modi per iniziare</h2>
    <div class="cols four">
      <article class="card"><span class="num">01</span><h3>Territori</h3><p>Per comuni, parchi nazionali, enti di protezione civile, comunità montane e gestori di strade, acqua o idroelettrico che vogliono vedere il movimento dei versanti prima che diventi un’emergenza.</p></article>
      <article class="card"><span class="num">02</span><h3>Partner tecnologici</h3><p>Per produttori di sensori, fornitori di dati satellitari e specialisti di modellistica che vogliono far lavorare il proprio contributo dentro una rete territoriale reale, con un ruolo e condizioni chiari.</p></article>
      <article class="card"><span class="num">03</span><h3>Scuole, università ed enti di formazione</h3><p>Per istituti tecnici, università ed enti di formazione professionale che vogliono costruire il percorso del <em>custode del territorio</em> e insegnare su siti attivi. <a href="/it/nuova-generazione/">Il percorso</a></p></article>
      <article class="card"><span class="num">04</span><h3>Finanziatori e partner locali</h3><p>Per programmi di finanziamento pubblico, fondazioni, investitori e agenzie di sviluppo locale interessati a infrastrutture ambientali di lungo periodo. Le conversazioni passano da Fab Campaigns.</p></article>
    </div>
  </div>
</section>

<section class="alt" id="contatti">
  <div class="wrap split">
    <div>
      <p class="kicker">Avvia un confronto</p>
      <h2>Raccontaci il tuo territorio</h2>
      <p>Basta una breve email. Ci aiuta sapere:</p>
      <ul class="clean">
        <li>dove si trova il territorio</li>
        <li>cosa è in gioco: abitati, strade, acqua, turismo</li>
        <li>quale monitoraggio esiste oggi</li>
      </ul>
      <p class="note">Rispondiamo in italiano o in inglese.</p>
    </div>
    <div class="contact-box">
      <p class="kicker">Scrivici</p>
      <p><a class="mail" href="mailto:%(mail)s">%(mail)s</a></p>
      <p>Oppure scegli un orario che ti va bene.</p>
      <div class="btns"><a class="btn dark" href="%(cal)s" rel="noopener">Prenota una chiamata</a></div>
    </div>
  </div>
</section>""",
    }



def next_en():
    return {
        "title": "Next Generation | Smart Mountains",
        "desc": "A path for a new Alpine profession, the territory steward, built with schools, universities and training bodies so young people can look after their own valleys.",
        "hero": """
<header class="page-hero">
  %(contours)s
  <div class="wrap">
    <p class="eyebrow">Next generation</p>
    <h1>No single career path leads to looking after an Alpine slope.</h1>
    <p class="lede">Hydraulics, electronics and geomatics are taught, and employed, in separate places. Valleys need people who bring them together, and young people who would like to stay need a reason and a route to do it. Smart Mountains is designing that route: a new Alpine profession, the territory steward.</p>
  </div>
</header>""",
        "body": """
<section>
  <div class="wrap split">
    <div>
      <p class="kicker">The profession</p>
      <h2>The territory steward</h2>
      <p>One person who can walk a slope, read what the instruments say about it, and keep those instruments working. The role joins three disciplines that are usually taught and employed apart.</p>
    </div>
    <p class="pull">Someone from the valley, trained to look after it.</p>
  </div>
  <div class="wrap">
    <div class="cols">
      <article class="card"><span class="num">01</span><h3>Hydraulics</h3><p>How water moves through a slope, a torrent or a catchment, and what it does to the ground.</p></article>
      <article class="card"><span class="num">02</span><h3>Electronics</h3><p>Sensors, power and communications that keep working in snow, cold and remote terrain.</p></article>
      <article class="card"><span class="num">03</span><h3>Geomatics</h3><p>Satellite and ground data, maps and analysis, turned into something a mayor or an engineer can use.</p></article>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <p class="kicker">The pathway</p>
    <h2>From the classroom to the slope</h2>
    <ol class="steps">
      <li><div><h3>Secondary schools</h3><p>Technical and vocational schools in the valley bring real monitoring sites into the curriculum, with real data from slopes the students know.</p></div></li>
      <li><div><h3>Universities</h3><p>Universities contribute teaching, scientific validation and a route into advanced study for those who want one.</p></div></li>
      <li><div><h3>Training on the slope</h3><p>Short, practical courses in installation, data quality and running a network, on live sites. Certification is being designed with training partners.</p></div></li>
      <li><div><h3>Work in the valley</h3><p>Trained people run the network in their own territory, through the local business network that set it up.</p></div></li>
    </ol>
    <p class="note">The pathway is in design. We will name schools, universities and training bodies once they agree to be named.</p>
  </div>
</section>

<section class="green">
  <div class="wrap">
    <p class="kicker">Who gains</p>
    <h2>A programme that stays local</h2>
    <div class="cols four">
      <article class="card on-dark"><h3>Young people</h3><p>A skilled job connected to the place they come from, and a reason to stay or come back.</p></article>
      <article class="card on-dark"><h3>Schools and universities</h3><p>Live infrastructure to teach on, and a say in how the programme is built. They are founding partners, not suppliers of graduates.</p></article>
      <article class="card on-dark"><h3>Territories</h3><p>Skills that remain after the project ends. The cost of switching on a site becomes local work and training.</p></article>
      <article class="card on-dark"><h3>The network</h3><p>Each site trains the people who run the next one, so growth does not depend on bringing people in from outside.</p></article>
    </div>
  </div>
</section>

<section class="cta">
  <div class="wrap">
    <h2>Teach, train or take part.</h2>
    <p>If you run a school, a course or a local business, or you are a young person who wants to work on mountain risk, write to us. We are building this with the people who will use it.</p>
    <div class="btns"><a class="btn" href="%(mail_ng)s">Write to us</a><a class="btn ghost" href="/partner-with-us/">Partner with us</a></div>
  </div>
</section>""",
    }


def next_it():
    return {
        "title": "Nuova generazione | Smart Mountains",
        "desc": "Un percorso per un nuovo mestiere alpino, il custode del territorio, costruito con scuole, università ed enti di formazione perché i giovani possano prendersi cura delle proprie valli.",
        "hero": """
<header class="page-hero">
  %(contours)s
  <div class="wrap">
    <p class="eyebrow">Nuova generazione</p>
    <h1>Nessun percorso unico porta a prendersi cura di un versante alpino.</h1>
    <p class="lede">Idraulica, elettronica e geomatica si studiano, e si assumono, in luoghi diversi. Le valli hanno bisogno di persone che le sappiano unire, e i giovani che vorrebbero restare hanno bisogno di un motivo e di un percorso per farlo. Smart Mountains sta progettando quel percorso: un nuovo mestiere alpino, il <em>custode del territorio</em>.</p>
  </div>
</header>""",
        "body": """
<section>
  <div class="wrap split">
    <div>
      <p class="kicker">Il mestiere</p>
      <h2>Il <em>custode del territorio</em></h2>
      <p>Una persona che sa percorrere un versante, leggere cosa dicono gli strumenti e mantenere quegli strumenti in funzione. Il ruolo unisce tre discipline che di solito si insegnano, e si impiegano, separatamente.</p>
    </div>
    <p class="pull">Una persona della valle, formata per prendersene cura.</p>
  </div>
  <div class="wrap">
    <div class="cols">
      <article class="card"><span class="num">01</span><h3>Idraulica</h3><p>Come l’acqua si muove in un versante, in un torrente o in un bacino, e cosa fa al terreno.</p></article>
      <article class="card"><span class="num">02</span><h3>Elettronica</h3><p>Sensori, alimentazione e comunicazioni che continuano a funzionare con neve, freddo e in luoghi isolati.</p></article>
      <article class="card"><span class="num">03</span><h3>Geomatica</h3><p>Dati satellitari e a terra, mappe e analisi, trasformati in qualcosa che un sindaco o un tecnico può usare.</p></article>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <p class="kicker">Il percorso</p>
    <h2>Dall’aula al versante</h2>
    <ol class="steps">
      <li><div><h3>Scuole superiori</h3><p>Gli istituti tecnici e professionali della valle portano siti di monitoraggio reali nei programmi, con dati veri di versanti che gli studenti conoscono.</p></div></li>
      <li><div><h3>Università</h3><p>Le università portano didattica, validazione scientifica e una strada verso studi avanzati per chi la vuole.</p></div></li>
      <li><div><h3>Formazione sul campo</h3><p>Corsi brevi e pratici su installazione, qualità dei dati e gestione di una rete, su siti attivi. La certificazione è in corso di progettazione con i partner formativi.</p></div></li>
      <li><div><h3>Lavoro in valle</h3><p>Le persone formate gestiscono la rete nel proprio territorio, attraverso la rete d’impresa locale che l’ha avviata.</p></div></li>
    </ol>
    <p class="note">Il percorso è in fase di progettazione. Indicheremo scuole, università ed enti di formazione quando avranno accettato di essere nominati.</p>
  </div>
</section>

<section class="green">
  <div class="wrap">
    <p class="kicker">Chi ne beneficia</p>
    <h2>Un programma che resta sul territorio</h2>
    <div class="cols four">
      <article class="card on-dark"><h3>Giovani</h3><p>Un lavoro qualificato legato al luogo da cui vengono, e un motivo per restare o tornare.</p></article>
      <article class="card on-dark"><h3>Scuole e università</h3><p>Un’infrastruttura reale su cui insegnare e voce in capitolo nella costruzione del programma. Sono partner fondatori, non fornitori di diplomati.</p></article>
      <article class="card on-dark"><h3>Territori</h3><p>Competenze che restano dopo la fine del progetto. Il costo di attivazione di un sito diventa lavoro e formazione locali.</p></article>
      <article class="card on-dark"><h3>La rete</h3><p>Ogni sito forma le persone che gestiranno il successivo, così la crescita non dipende dal far arrivare persone da fuori.</p></article>
    </div>
  </div>
</section>

<section class="cta">
  <div class="wrap">
    <h2>Insegna, forma o partecipa.</h2>
    <p>Se dirigi una scuola, un corso o un’impresa locale, o sei un giovane che vuole lavorare sul rischio in montagna, scrivici. Lo costruiamo con le persone che lo useranno.</p>
    <div class="btns"><a class="btn" href="%(mail_ng)s">Scrivici</a><a class="btn ghost" href="/it/partner/">Collabora con noi</a></div>
  </div>
</section>""",
    }


# ---------------------------------------------------------------- layout

PAGES = [
    # key, en path, it path, en builder, it builder
    ("home", "/", "/it/", home_en, home_it),
    ("about", "/about/", "/it/chi-siamo/", about_en, about_it),
    ("next", "/next-generation/", "/it/nuova-generazione/", next_en, next_it),
    ("partner", "/partner-with-us/", "/it/partner/", partner_en, partner_it),
]


def layout(lang, path, alt_path, page, current_idx):
    t = T[lang]
    ctx = {"art": hero_art(), "contours": contour_art(), "fab": FAB, "mail": MAIL, "cal": CALENDLY,
           "mail_ng": "mailto:%s?subject=%s" % (MAIL, "Next%20generation" if lang == "en" else "Nuova%20generazione")}
    hero = page["hero"] % ctx
    body = page["body"] % ctx if "%(" in page["body"] else page["body"]
    en_path = path if lang == "en" else alt_path
    it_path = alt_path if lang == "en" else path
    nav = ""
    for i, (href, label) in enumerate(t["nav"]):
        cur = ' aria-current="page"' if i == current_idx else ""
        nav += '<a href="%s"%s>%s</a>' % (href, cur, label)
    other = alt_path
    nav += '<a class="lang" href="%s" hreflang="%s" lang="%s" aria-label="%s">%s</a>' % (
        other, "it" if lang == "en" else "en", "it" if lang == "en" else "en", t["other_label"], t["other_code"])
    jsonld = (
        '{"@context":"https://schema.org","@type":"WebSite","name":"Smart Mountains","url":"%s/",'
        '"publisher":{"@type":"Organization","name":"Fab Campaigns Ltd","url":"%s"}}' % (SITE, FAB)
    )
    return """<!doctype html>
<html lang="%(lang)s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(site)s%(path)s">
<link rel="alternate" hreflang="en" href="%(site)s%(en)s">
<link rel="alternate" hreflang="it" href="%(site)s%(it)s">
<link rel="alternate" hreflang="x-default" href="%(site)s%(en)s">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Smart Mountains">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(site)s%(path)s">
<meta property="og:image" content="%(site)s/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0A1628">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/source-serif-4-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">%(jsonld)s</script>
</head>
<body>
<a class="skip" href="#main">%(skip)s</a>
<div class="site-header">
  <div class="wrap">
    <a class="brand" href="%(home)s" aria-label="Smart Mountains">%(logo)s<span>Smart Mountains</span></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">%(menu)s</button>
    <nav class="nav" id="nav" aria-label="Main">%(nav)s</nav>
  </div>
</div>
<main id="main">
%(hero)s
%(body)s
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="top">
      <div>
        <p class="tag">Smart Mountains</p>
        <small>%(tagline)s. %(footer_line)s</small>
      </div>
      <div class="flinks">
        %(flinks)s
      </div>
    </div>
    <small>%(legal)s</small>
  </div>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
""" % {
        "lang": lang, "title": page["title"], "desc": page["desc"], "site": SITE, "path": path,
        "en": en_path, "it": it_path, "jsonld": jsonld, "skip": t["skip"], "home": t["home_url"],
        "logo": LOGO, "menu": t["menu"], "nav": nav, "hero": hero, "body": body,
        "tagline": t["tagline"], "footer_line": t["footer_line"], "legal": t["legal"],
        "flinks": '<a href="mailto:%s">%s</a><a href="%s" rel="noopener">fabcampaigns.com</a><a href="%s">%s</a>' % (
            MAIL, MAIL, FAB, alt_path, t["other_label"]),
    }


def write(rel, text):
    p = OUT / rel.lstrip("/")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def main():
    for idx, (key, en_path, it_path, en_fn, it_fn) in enumerate(PAGES):
        write(en_path + "index.html", layout("en", en_path, it_path, en_fn(), idx))
        write(it_path + "index.html", layout("it", it_path, en_path, it_fn(), idx))
    write("/favicon.svg", FAVICON)

    urls = []
    for _, en_path, it_path, _, _ in PAGES:
        for p in (en_path, it_path):
            urls.append(
                "  <url><loc>%s%s</loc>"
                '<xhtml:link rel="alternate" hreflang="en" href="%s%s"/>'
                '<xhtml:link rel="alternate" hreflang="it" href="%s%s"/></url>' % (SITE, p, SITE, en_path, SITE, it_path)
            )
    write("/sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + "\n".join(urls) + "\n</urlset>\n")
    write("/robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE)

    write("/404.html", """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Page not found | Smart Mountains</title><meta name="robots" content="noindex">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/style.css"></head>
<body><main id="main"><header class="page-hero"><div class="wrap">
<p class="eyebrow">404</p><h1>This slope is not on our map.</h1>
<p class="lede">The page you were looking for has moved or does not exist. <a href="/">Back to the home page</a> or <a href="/it/">torna alla home in italiano</a>.</p>
</div></header></main></body></html>
""")

    write("/_redirects",
          "# Old WordPress URLs\n"
          "/chi-siamo        /it/chi-siamo/  301\n"
          "/chi-siamo/       /it/chi-siamo/  301\n"
          "/en               /               301\n"
          "/en/              /               301\n"
          "/en/about         /about/         301\n"
          "/en/about/        /about/         301\n"
          "/en/partner-with-us   /partner-with-us/  301\n"
          "/en/partner-with-us/  /partner-with-us/  301\n"
          "/it/about         /it/chi-siamo/  301\n"
          "/it/about/        /it/chi-siamo/  301\n"
          "/it/partner-with-us   /it/partner/  301\n"
          "/it/partner-with-us/  /it/partner/  301\n")
    write("/_headers",
          "/*\n"
          "  X-Content-Type-Options: nosniff\n"
          "  Referrer-Policy: strict-origin-when-cross-origin\n"
          "  X-Frame-Options: DENY\n"
          "  Permissions-Policy: camera=(), microphone=(), geolocation=()\n"
          "  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; font-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'\n"
          "\n"
          "/assets/*\n"
          "  Cache-Control: public, max-age=31536000, immutable\n"
          "\n"
          "/favicon.svg\n"
          "  Cache-Control: public, max-age=86400\n")
    print("Built", len(PAGES) * 2, "pages into", OUT)


if __name__ == "__main__":
    main()
