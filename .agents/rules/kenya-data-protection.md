# Kenya data protection (ODPC) check

Use this when a task touches personal data of people in Kenya: a product, feature, codebase, privacy notice, marketing list, data breach, or a question about registering with the Office of the Data Protection Commissioner (ODPC). It applies even when the user doesn't name the law.

The rules come from the official texts as revised to 31 December 2022: the Data Protection Act 2019 ("the Act"), the Registration Regulations 2021 and the General Regulations 2021. Check for later changes before relying on a figure. This is not legal advice; say so once, at the end.

The full rules, with every section number, are in `skills/kenya-data-protection/references/law.md` of https://github.com/jaysonmulwa/kenya-data-protection. Read them when you need more than this summary.

## How to run a check

1. **Get the facts that change the answer:** who decides how data is used (controller) and who acts on instructions (processors such as hosting, payments, email, analytics); last year's revenue and number of employees; the sector; each kind of data and whether it's sensitive; any children; where data is stored or sent; how long it's kept. For a codebase, read the data model, sign-up and payment flows, privacy notice and hosting config instead of asking.
2. **Decide on registration** (below). Then check the duties either way: they apply to everyone.
3. **Report**, verdict first:
   - **Verdict.** Register: yes / no / ask the ODPC, why, and the fee. One sentence saying the duties apply whether or not registration is required. The two or three biggest risks.
   - **Gaps.** A table: requirement, law, now, fix.
   - **Do next.** Numbered actions, each small enough to start today.
   - **Check with the ODPC or a lawyer.** Anything borderline, with the question to ask.

Write each gap so the reader can act without looking up the law: spell out what a rule requires, not just its number; call sensitive data "sensitive personal data" by name, even when also asking whether it's needed; cite the right instrument.

## Registration

- **Exempt only if all three hold** (Registration Regulations reg 13): revenue (or a non-profit's turnover) **below KES 5 million**, **and fewer than 10 employees**, **and** no processing for a mandatory purpose. 12 employees with KES 3 million revenue must register.
- **Mandatory purposes, whatever the size** (Third Schedule of the Registration Regulations, not the Act): political canvassing; crime prevention, including a security CCTV system; gambling; operating an educational institution; health administration and patient care; hospitality (not tour guides); property management, including selling land; financial services; telecoms; businesses wholly or mainly in direct marketing; transport, including ride-hailing apps; genetic data.
- **Fees** (Second Schedule): micro and small (1–50 staff, up to KES 5M) KES 4,000, renewal 2,000; medium (51–99 staff, KES 5–50M) 16,000, renewal 9,000; large (over 99 staff, over KES 50M) 40,000, renewal 25,000; public bodies, charities and religious bodies 4,000, renewal 2,000.
- **Certificates last 24 months.** Apply online on Form DPR1, renew on DPR2. Report changes of particulars within 14 days. Processing unregistered, or after expiry, is an offence.

## Duties that apply to everyone

- **Lawful basis (Act s.30)** for each purpose: consent, contract, legal obligation, vital interests, public interest, legitimate interests, or research. Consent must be provable and as easy to withdraw as to give (s.32).
- **Tell people before collecting (s.29):** what is collected and why, who receives it and the safeguards, their rights and how to use them, who to contact, the security measures, whether giving it is required, and what happens if they don't.
- **Publish a data protection policy (General Regulations reg 23)**, and keep it updated. Required even for organisations exempt from registering.
- **Children are under 18 (s.33):** a parent's or guardian's consent, and an age check proportionate to the risk.
- **Retention (s.39; reg 19):** keep data only as long as needed, with a written retention schedule, then delete or anonymise it.
- **Processors (reg 24):** a written contract with each one, covering instructions, confidentiality, security, sub-processors, deletion and audits.
- **Security by design (s.41):** collect only what each purpose needs, encrypt, limit access, test backups and safeguards.

## Sensitive personal data (s.2, 44–46)

- **Kenya's list is wide:** race, health, ethnic social origin, conscience, belief, genetic and biometric data, property details, marital status, family details including the names of a person's children, parents or spouse, sex, and sexual orientation. A next-of-kin field is sensitive when it names a child, parent or spouse.
- **It needs its own ground (s.45),** beyond a lawful basis: a not-for-profit body's own members; data the person made public; or necessity for a legal claim, legal obligations or rights, or vital interests. Neither legitimate interests nor consent is on that list, so a face-scan watchlist can't rest on legitimate interests. Flag consent-only cases for the ODPC or a lawyer.
- **Health data (s.46)** is processed by or under a health care provider, or someone with a legal duty of secrecy or confidentiality.

## Marketing (s.37; General Regulations reg 14–18)

- Commercial use needs **express consent**.
- **No sensitive data in direct marketing, even with consent** (reg 15(1)).
- Every message says how to opt out free of charge (reg 15–17).
- Stop sharing data with a third party for its marketing **within 7 days** of a request (reg 18).
- Commercial use without consent: fine up to KES 20,000 or 6 months' jail, or both (reg 15(4)).

## People's requests (General Regulations)

| Request | Deadline |
|---|---|
| Access | 7 days, free of charge |
| Rectification | 14 days; a refusal in writing with reasons within 7 days |
| Erasure | respond within 14 days |
| Objection | 14 days, free |
| Restriction | 14 days, free |
| Portability | 30 days, at reasonable cost |
| Stop sharing for a third party's direct marketing | 7 days |
| Data collected from someone else: tell the person | 14 days |

## Impact assessments (DPIA) (s.31; General Regulations reg 49–51)

- **Required before high-risk processing,** including: sensitive data; children's or vulnerable people's data; biometric or genetic data; automated decisions with significant effect; combining datasets; large-scale processing; **large-scale systematic monitoring of a public area** (CCTV, facial recognition); new technology; a change that raises the risk.
- **Two ODPC steps.** The report goes to the ODPC 60 days before processing starts (s.31(5)). If it shows high risk, that is also a prior consultation (s.31(3)): the ODPC has 60 days to reply, and silence after 60 days lets processing begin (reg 51).

## Breaches (s.43; General Regulations reg 37)

- Notify the ODPC **within 72 hours** of becoming aware, where there's a real risk of harm. Tell affected people in writing within a reasonably practical time. A processor tells the controller without delay, within 48 hours where practicable.
- **Notifiable by definition (reg 37):** a full name or ID number together with one of the listed kinds of data; or an account identifier together with a password, PIN, security answer or other access credential.

## Transfers outside Kenya and local hosting (s.48–50; reg 26)

- Hosting or analytics abroad is a transfer. It needs proof of safeguards, or a necessity, or consent. **Sensitive data abroad needs the person's consent** and safeguards (s.49).
- **Must keep a server, or at least one serving copy, in Kenya (reg 26):** civil registration and legal identity; elections; public finance systems; protected computer systems; **early childhood and basic education**; **primary or secondary health care**.

## Penalties

- ODPC administrative fine: up to **KES 5 million or 1% of the previous year's turnover, whichever is lower** (s.63).
- Offences with no specific penalty: fine up to KES 3 million, up to 10 years' jail, or both (s.73).
- People can claim compensation, including for non-financial damage (s.65).

## Sources

- Data Protection Act 2019: https://new.kenyalaw.org/akn/ke/act/2019/24/eng@2022-12-31
- Registration Regulations 2021: https://new.kenyalaw.org/akn/ke/act/ln/2021/265/eng@2022-12-31
- General Regulations 2021: https://new.kenyalaw.org/akn/ke/act/ln/2021/263/eng@2022-12-31
- ODPC: https://www.odpc.go.ke
