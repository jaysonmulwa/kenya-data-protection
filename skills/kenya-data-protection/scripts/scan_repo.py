"""Scan a codebase for what a Kenya data protection check needs to know.

Finds personal data fields (flagging the ones that are sensitive under
s.2 of the Act, or point to children), third-party services that act as
processors, hosting regions, and whether a privacy notice exists.

It is a starting point for the data inventory, not a verdict: matches are
by name, so confirm each one in the code.

Usage: python scan_repo.py [path]    (prints a Markdown report)
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "vendor", "venv", ".venv", "dist", "build",
             ".next", "__pycache__", "target", ".gradle", "Pods", "coverage"}
TEXT_EXT = {".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".rb", ".go", ".java",
            ".kt", ".swift", ".dart", ".php", ".cs", ".sql", ".prisma", ".graphql", ".gql",
            ".proto", ".json", ".yaml", ".yml", ".toml", ".tf", ".env", ".example", ".html",
            ".vue", ".svelte", ".xml", ".gradle", ".lock", ".cfg", ".ini"}
MAX_BYTES = 1_000_000

# Field-name parts, matched against snake_case parts of identifiers.
# A tuple means all those parts must appear in the identifier.
FIELDS = {
    "sensitive: health": ["health", "medical", "diagnosis", "allergy", "allergies",
                          "disability", "blood", "illness", ("chronic",),
                          "medication", "hiv", "prescription"],
    # "parent" and "children" alone are tree and UI words in code, so need a person part.
    "sensitive: family details": ["spouse", "wife", "husband", "kin", "guardian",
                                  "father", "mother", "sibling", "siblings",
                                  ("parent", "name"), ("parent", "phone"), ("parent", "email"),
                                  ("children", "names"), ("child", "name"), ("children", "count")],
    "sensitive: marital status": [("marital",), ("married",)],
    "sensitive: religion or belief": ["religion", "religious", "church", "mosque", "faith",
                                      "denomination", "belief"],
    "sensitive: race or ethnicity": ["race", "ethnicity", "ethnic", "tribe", "tribal"],
    "sensitive: sex or orientation": ["gender", "sex", "orientation"],
    "sensitive: biometric or genetic": ["biometric", "biometrics", "fingerprint",
                                        "faceid", "dna", "genetic", "genome", "selfie"],
    "sensitive: property details": [("title", "deed"), ("land",), ("plot", "number"),
                                    ("property", "details")],
    "children": ["dob", ("date", "birth"), ("birth", "date"), ("birthday",), "student",
                 "pupil", "learner", "school", "admission"],
    "identity numbers": [("national", "id"), ("id", "number"), ("idno",), "passport",
                         ("kra", "pin"), "nhif", "shif", "nssf", "huduma", ("birth", "cert")],
    "contact and location": ["phone", "msisdn", ("mobile", "number"), "email", "address",
                             "latitude", "longitude", "gps", "geolocation"],
    "financial": ["mpesa", "salary", "income", "iban", "loan",
                  ("account", "number"), ("card", "number")],
    "credentials": ["password", "passcode", "otp", ("security", "answer"), ("pin", "hash")],
}

# Third parties: name -> (regex, role). Most store data outside Kenya; check each.
SERVICES = {
    "Firebase / Google Cloud": (r"firebase|@google-cloud|google-cloud-|googleapis\.com|provider\s+\"google\"", "Google services: check which (push, auth, database, analytics)"),
    "Google Analytics / Tag Manager": (r"google-analytics|gtag\(|googletagmanager|react-ga", "analytics"),
    "Meta Pixel / Facebook SDK": (r"connect\.facebook\.net|fbq\(|facebook-sdk|react-native-fbsdk", "advertising"),
    "Mixpanel": (r"mixpanel", "analytics"), "Amplitude": (r"amplitude", "analytics"),
    "Segment": (r"@segment/|analytics-node|segment\.com", "analytics"),
    "PostHog": (r"posthog", "analytics"), "Hotjar": (r"hotjar", "session recording"),
    "Microsoft Clarity": (r"clarity\.ms", "session recording"),
    "Sentry": (r"@sentry/|sentry-sdk|sentry\.io", "error tracking"),
    "Datadog": (r"datadog|dd-trace", "monitoring"), "LogRocket": (r"logrocket", "session recording"),
    "Intercom": (r"intercom", "support chat"), "Zendesk": (r"zendesk", "support"),
    "Stripe": (r"stripe", "payments"), "Paystack": (r"paystack", "payments"),
    "Flutterwave": (r"flutterwave", "payments"), "Pesapal": (r"pesapal", "payments"),
    "M-Pesa Daraja (Safaricom)": (r"daraja|safaricom\.co\.ke|mpesa-?api|stkpush", "payments"),
    "Africa's Talking": (r"africastalking|africas-talking", "SMS"),
    "Twilio": (r"twilio", "SMS, calls"), "SendGrid": (r"sendgrid", "email"),
    "Mailgun": (r"mailgun", "email"), "Mailchimp": (r"mailchimp", "email marketing"),
    "Postmark": (r"postmark", "email"), "Resend": (r"\bresend\b", "email"),
    "AWS": (r"aws-sdk|@aws-sdk/|boto3|amazonaws\.com|provider\s+\"aws\"", "hosting, storage"),
    "Azure": (r"@azure/|azure-|\.azure\.com|windows\.net|provider\s+\"azurerm\"", "hosting, storage"),
    "Supabase": (r"supabase", "database, auth"), "MongoDB Atlas": (r"mongodb\+srv|mongodb\.net", "database"),
    "Auth0": (r"auth0", "authentication"), "Clerk": (r"@clerk/", "authentication"),
    "OneSignal": (r"onesignal", "push notifications"), "Cloudinary": (r"cloudinary", "media storage"),
    "OpenAI": (r"\bopenai\b", "AI processing"), "Anthropic": (r"@anthropic-ai|\banthropic\b", "AI processing"),
    "Vercel": (r"vercel", "hosting"), "Netlify": (r"netlify", "hosting"),
    "Heroku": (r"heroku", "hosting"), "Render": (r"render\.yaml|onrender\.com", "hosting"),
    "Fly.io": (r"fly\.toml|fly\.dev", "hosting"),
}

REGION_PATTERNS = [
    r"\b(?:us|eu|ap|af|ca|me|sa|il|mx)-(?:north|south|east|west|central|northeast|southeast|southwest|northwest)-\d\b",
    r"\b(?:us|europe|asia|africa|me|northamerica|southamerica|australia)-(?:central|east|west|north|south|northeast|southeast|southwest|northwest)\d\b",
    r"""\b(?:region|location|primary_region)\s*[:=]\s*["']?([A-Za-z][\w-]{1,30})""",
]


def parts(identifier):
    """camelCase / kebab / snake -> lowercase parts."""
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", identifier)
    return [p for p in re.split(r"[_\-]+", s.lower()) if p]


def field_category(identifier):
    ps = parts(identifier)
    for cat, terms in FIELDS.items():
        for t in terms:
            need = t if isinstance(t, tuple) else (t,)
            if all(n in ps for n in need):
                return cat
    return None


def files(root):
    for p in root.rglob("*"):
        if any(d in SKIP_DIRS for d in p.parts) or not p.is_file():
            continue
        if (p.suffix.lower() in TEXT_EXT or p.name.startswith((".env", "Dockerfile"))) \
                and p.stat().st_size <= MAX_BYTES:
            yield p


def scan(root):
    root = Path(root)
    fields = defaultdict(lambda: defaultdict(set))   # cat -> name -> {file}
    services = defaultdict(set)                       # name -> {file}
    regions = defaultdict(set)                        # region -> {file}
    notices = []
    for p in files(root):
        rel = p.relative_to(root).as_posix()
        if re.search(r"privacy|data[-_ ]?protection|cookie[-_ ]?policy", p.name, re.I):
            notices.append(rel)
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if p.name.endswith(".lock") or p.name == "package-lock.json":
            text = text[:200_000]  # ponytail: lockfiles only for service names, cap the scan
        else:
            for ident in set(re.findall(r"[A-Za-z_][A-Za-z0-9_\-]{1,40}", text)):
                cat = field_category(ident)
                if cat:
                    fields[cat][ident].add(rel)
        low = text.lower()
        for name, (rx, _) in SERVICES.items():
            if re.search(rx, low):
                services[name].add(rel)
        for rx in REGION_PATTERNS:
            for m in re.finditer(rx, text, re.I):
                regions[(m.group(1) if m.groups() else m.group(0)).lower()].add(rel)
    return fields, services, regions, notices


def sample(paths, n=3):
    paths = sorted(paths)
    return ", ".join(f"`{p}`" for p in paths[:n]) + (f" (+{len(paths) - n} more)" if len(paths) > n else "")


def report(root):
    fields, services, regions, notices = scan(root)
    out = [f"# Data inventory scan: {Path(root).resolve().name}", "",
           "Matches are by name. Confirm each in the code before relying on it.", ""]
    out += ["## Personal data fields", ""]
    if not fields:
        out.append("None found by name.")
    order = sorted(fields, key=lambda c: (not c.startswith("sensitive"), c != "children", c))
    for cat in order:
        names = fields[cat]
        out.append(f"- **{cat}**: " + ", ".join(f"`{k}`" for k in sorted(names)[:12])
                   + f" — in {sample(set().union(*names.values()))}")
    out += ["", "## Third-party services (likely processors)", ""]
    if not services:
        out.append("None found.")
    for name in sorted(services):
        out.append(f"- **{name}** ({SERVICES[name][1]}) — in {sample(services[name])}")
    out += ["", "## Hosting regions mentioned", ""]
    out += [f"- `{r}` — in {sample(f)}" for r, f in sorted(regions.items())] or ["None found."]
    out += ["", "## Privacy notice or policy files", ""]
    out += [f"- `{n}`" for n in sorted(notices)] or ["None found by file name."]
    return "\n".join(out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(report(sys.argv[1] if len(sys.argv) > 1 else "."))
