---
name: kenya-data-protection
description: Check a product, business or feature against Kenya's Data Protection Act 2019 and the ODPC (Office of the Data Protection Commissioner) regulations, and say what to do. Covers whether the organisation must register as a data controller or processor (thresholds, mandatory sectors, fees, renewal), privacy notices, lawful basis and consent, children's data, data subjects' requests and their deadlines, impact assessments (DPIA), breach notification, transfers outside Kenya and local hosting, retention, processor contracts, data protection officers and penalties. Use it whenever someone mentions ODPC, the Kenya Data Protection Act or DPA 2019, "do we need to register with the Data Commissioner", a privacy policy or notice for Kenyan users, a data breach affecting Kenyans, collecting data from Kenyan children or students, storing Kenyan users' data abroad, or launching an app, payments, analytics or marketing feature in Kenya, even if they don't name the law.
---

# Kenya data protection (ODPC)

Kenya's Data Protection Act 2019 applies to anyone processing personal data of people in Kenya. The Office of the Data Protection Commissioner (ODPC) enforces it. Most of its duties apply whether or not the organisation has to register, so a "we're too small to register" answer is never the end of the check.

The legal facts, with section numbers and sources, are in `references/law.md`. The working checklists are in `references/checklists.md`. Read `law.md` before giving any figure, deadline or threshold; don't quote them from memory, because the details (both conditions for the exemption, Kenya's wide definition of sensitive data) are easy to get wrong.

## How to run a check

### 1. Get the facts

Ask for, or find in the project, only what changes the answer:

- **Who decides why and how data is used** (the data controller) and who only acts on instructions (data processors: hosting, payment providers, email, analytics).
- **Size:** last year's revenue (or a non-profit's used budget) and number of employees.
- **Purpose and sector:** compare with the 12 mandatory purposes in `law.md` (financial services, education, health, transport, direct marketing and others).
- **Data collected:** each category, and whether any is *sensitive* under Kenyan law. Kenya's list is wider than GDPR's: it includes property details, marital status and family details such as the names of children, parents and spouses.
- **Children:** anyone under 18.
- **Where data is stored or sent:** servers, backups and every provider outside Kenya.
- **Retention:** how long each kind of data is kept, and what happens after.

For a codebase, start by running the scanner, which needs only Python:

```
python <skill-dir>/scripts/scan_repo.py <repo-path>
```

It lists personal data fields by name (flagging Kenyan sensitive data and signs of children), third-party services that act as processors, hosting regions and any privacy notice file. It matches names only, so treat it as a map: then read the data model, the sign-up and payment flows, the privacy notice and the hosting setup it points to, rather than asking what the code already answers. If Python isn't available, do the same search by hand.

### 2. Decide on registration

An organisation is exempt from registering **only if all three hold**:
1. annual revenue (or a non-profit's turnover) **below KES 5 million**, **and**
2. **fewer than 10 employees**, **and**
3. **none** of its processing is for a purpose in the Third Schedule of the Registration Regulations 2021 (the 12 mandatory purposes; the Act itself has no such list).

If any one fails, it must register before processing. Give the fee band from `law.md`, the 24-month validity and the renewal fee. Point to the ODPC's online registration. Say plainly when a purpose is borderline, for example an app that collects payments through a licensed provider: is that "provision of financial services"? Recommend asking the ODPC or a lawyer rather than guessing, and note that registering costs little compared with the offence of processing unregistered.

An exempt organisation still has to follow Part IV (principles and obligations) and Part VI (transfers outside Kenya) of the Act. Go on to step 3 either way.

### 3. Check the duties

Work through `references/checklists.md`, and only the parts that apply:

- lawful basis for each purpose, and consent done properly where it's the basis;
- the privacy notice against the eight items in section 29, and a published data protection policy (reg 23), which everyone needs, registered or not;
- children's data: parental consent and age checks;
- commercial use and direct marketing, including the ban on using sensitive data for it;
- data subjects' requests and their deadlines (7, 14 or 30 days);
- retention schedule;
- written contracts with every processor;
- DPIA screening against the high-risk list;
- breach readiness (72 hours to the ODPC);
- transfers outside Kenya, and whether local hosting is required;
- whether a data protection officer is needed or wise;
- security by design.

### 4. Report

Use this structure, in plain language:

```
# Kenya data protection check: [product or organisation]

## Verdict
Register: yes / no / ask the ODPC — why, in one or two sentences, and the fee if yes.
Duties: one sentence saying the Act's duties apply whether or not registration is required.
Biggest risks: the two or three gaps that matter most.

## Gaps
| Requirement | Law | Now | Fix |
|---|---|---|---|
(one row per gap; leave out what already complies, or list it briefly at the end)

## Do next
Numbered actions in order, each small enough to start today.

## Check with the ODPC or a lawyer
Anything borderline, with the question to ask.

Based on the Act and regulations as revised to 31 December 2022 (see references/law.md). Not legal advice.
```

Keep the verdict first. Say "not legal advice" once, at the end, not throughout.

Write each gap so the reader can act on it without looking up the law:

- **Spell out what a rule requires, not just its number.** "Add a notice covering s.29's eight items" sends the reader off to find them. Say what the notice must tell people: what is collected and why, who receives it, their rights and how to use them, and who to contact.
- **Call sensitive data sensitive, by name.** When a field such as marital status, a parent's name or a medical note is in the data, say it is sensitive personal data under s.2, even if you also question whether it's needed. The label is what triggers the extra rules (consent for transfers abroad, no direct marketing, a DPIA), so a reader who only hears "you don't need this field" misses them.
- **For a DPIA, give both ODPC steps.** The report goes to the ODPC 60 days before processing starts (s.31(5)). If it shows high risk, that is also a prior consultation (s.31(3), reg 51): the ODPC has 60 days to reply and may ask for changes before go-live.

## Things that catch people out

- **The exemption needs both numbers below the line.** KES 3 million revenue with 12 employees must register.
- **The mandatory purposes override size.** A one-person startup doing transport, education, health, lending or payments, or mainly direct marketing, must register.
- **Registration ends.** Certificates last 24 months. Processing after expiry without renewing is an offence, and changes of particulars must be reported within 14 days.
- **Sensitive data is broad.** Names of a person's children, parents or spouse are sensitive data in Kenya, and so is marital status. A next-of-kin field usually holds one of these, so treat it as sensitive.
- **No sensitive data in direct marketing.** Reg 15(1) allows direct marketing only with non-sensitive data, so consent doesn't make it lawful to target people by marital status, family details, health or religion.
- **Everyone needs a published policy.** Reg 23 requires a data protection policy, published and kept up to date, even from organisations exempt from registering.
- **A DPIA adds 60 days to a launch.** Reports are submitted 60 days before processing (s.31(5)), so a DPIA done the week before go-live is too late. Where it shows high risk, the ODPC must be consulted before processing (s.31(3)), and it has those 60 days to reply.
- **Public monitoring needs a DPIA.** Large-scale CCTV or facial recognition of a public area is on the high-risk list, and a security CCTV system also makes registration mandatory.
- **"Children" means under 18.** Youth sports, schools and family apps need parental consent and an age check, and a DPIA (children's data is on the high-risk list).
- **Hosting abroad is a transfer.** A server or analytics service outside Kenya needs a lawful transfer basis and safeguards. Sensitive data abroad also needs the person's consent.
- **Some processing must stay in Kenya.** For example, basic and early-childhood education and primary or secondary health care need a server or at least one copy in Kenya.
- **Processors need written contracts** with the particulars in regulation 24.
- **Breach clock:** 72 hours to the ODPC, from becoming aware. A processor must tell the controller within 48 hours.

## Sources

Link these in any answer that relies on them, and say the law may have changed since:

- Data Protection Act 2019: https://new.kenyalaw.org/akn/ke/act/2019/24/eng@2022-12-31
- Registration Regulations 2021 (Legal Notice 265): https://new.kenyalaw.org/akn/ke/act/ln/2021/265/eng@2022-12-31
- General Regulations 2021 (Legal Notice 263): https://new.kenyalaw.org/akn/ke/act/ln/2021/263/eng@2022-12-31
- ODPC: https://www.odpc.go.ke (registration portal, forms, current notices)

Kenya Law blocks some automated fetching. If a check needs the current text, open it in a browser tool.
