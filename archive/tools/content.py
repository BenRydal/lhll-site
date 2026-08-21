# Content map for learninghowtolookandlisten.com rebuild.
# Pairings verified against document order in the scraped Squarespace HTML.

FOOTER_CREDIT = True

SESSIONS = [
    ("d8_pRUR-hmg", "1505739795377-image-asset.jpeg", "“Matter Occupies Space” Video", "source"),
    ("bOT48kMRL1g", "1503327359692-rogoffDayton.png", "Barbara Rogoff & Andy Dayton", ""),
    ("HjBvwRSG_jY", "1503327298512-image-asset.png", "Shirin Vossoughi", ""),
    ("skD6LTPNxYk", "1503349514503-image-asset.png", "Kris Gutiérrez", ""),
    ("9Qa1T4pwUYo", "1503364582971-sherin.png", "Miriam Sherin", ""),
    ("NvW6zcL4WNU", "1503327419147-image-asset.png", "John Haviland & Chuck Goodwin (Part 1)", ""),
    ("9ZvNlWDnznQ", "1503327441010-goodwinHaviland.png", "John Haviland & Chuck Goodwin (Part 2)", ""),
    ("tU4_af2KOnk", "1503361965728-image-asset.png", "Mark Sicoli", ""),
    ("agUUzmtjsR0", "1503404304779-image-asset.png", "Rogers Hall & Ben Rydal Shapiro", ""),
    ("FWXVeVu00bY", "1503349549360-image-asset.png", "Joel Kuipers", ""),
    ("0gjYb3N8E4A", "1503362038059-image-asset.png", "Susan Jurow", ""),
    ("x1nWTkViM7Q", "1503326938822-sicoli.png", "Sarah Johnson", ""),
    ("3E32hLmm6PA", "1503327273253-shirin.png", "Wolff-Michael Roth", ""),
    ("2uRcwN2igVE", "1503327214336-image-asset.png", "Jason Duque", ""),
    ("gPde5f5kZtA", "1503330213916-jewitt.png", "Carey Jewitt", ""),
    ("S8IJKA7t9cE", "1503349456079-image-asset.png", "Jürgen Streeck", ""),
    ("OD49l0BF3BU", "1503362175344-image-asset.png", "Jasmine Ma", ""),
    ("7rlNjkSLcQ8", "1518268708086-AdamKendon.png", "Adam Kendon", ""),
    ("vhthoOHXMSI", "1519755428833-FredErickson.png", "Frederick Erickson", ""),
]

PRESENTATIONS = [
    ("TyFl4l1Ecms", "1645802778090-image-asset.jpeg", "Chuck Goodwin", ""),
    ("zWraBg0vT4Y", "1645802848293-image-asset.jpeg", "Barbara Rogoff", ""),
    ("ZVzlZeR7zcw", "1645818555092-image-asset.jpeg", "Joel Kuipers", ""),
    ("odgZ2HcOH7g", "1645818679066-image-asset.jpeg", "Miriam Sherin", ""),
    ("upKPiJwm7Yc", "1645818719754-image-asset.jpeg", "Susan Jurow", ""),
    ("QBVViMbB2To", "1502921672059-image-asset.jpeg", "Jason Duque", ""),
    ("4MiCvY0xxvk", "1502921696499-image-asset.jpeg", "Sarah Jean Johnson", ""),
    ("eQ3gIQBmv-4", "1649252089835-image-asset.jpeg", "Shirin Vossoughi", ""),
    ("i4mYHGMQba0", "1502921745439-image-asset.jpeg", "Mark Sicoli", ""),
    ("Nyf2DOTlbco", "1502921772675-image-asset.jpeg", "John Haviland", ""),
    ("KqU9xUGTVw4", "1502921839486-image-asset.jpeg", "Kris Gutiérrez", ""),
    ("qqBSgf_l-y8", "1502921951351-image-asset.jpeg", "Jürgen Streeck", ""),
    ("DACtFpyu6Ds", "1502921893308-image-asset.jpeg", "Carey Jewitt", ""),
    ("nIadvkWfonU", "1502921918760-image-asset.jpeg", "Rogers Hall", ""),
]

GROUP_VIDEO = "U-17pqdXHwg"
COVER = "1506709090583-coverPageUpdate.png"


def slug(name):
    import re, unicodedata
    s = name.lower()
    s = s.replace("“", "").replace("”", "")
    s = s.replace("&", "and")
    # strip accents so filenames stay ascii: gutiérrez -> gutierrez
    s = "".join(c for c in unicodedata.normalize("NFD", s)
                if unicodedata.category(c) != "Mn")
    s = re.sub(r"\(part (\d)\)", r"pt\1", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")
