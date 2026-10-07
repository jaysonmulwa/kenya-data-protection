# Checklists

Use only the sections that apply. Each item names the law in `law.md`.

## Data inventory (do this first)

For each kind of personal data, record:
- what it is;
- whether it's sensitive (`law.md` §5);
- whose it is (players, customers, staff, children);
- why it's collected and on what lawful basis (§2), and for sensitive data, which s.45 ground applies (§5);
- where it's stored, and every processor that touches it;
- whether any of it leaves Kenya (§12);
- how long it's kept, and what happens then (§8).

A codebase's data model, forms and third-party services usually answer most of this.

## Privacy notice (s.29)

The notice, shown before collection, says:
- [ ] people's rights (access, object, correct, delete, portability), and how to use them;
- [ ] that personal data is being collected, and what;
- [ ] the purpose of each kind;
- [ ] each third party or processor it goes to (payments, hosting, email, analytics), with the safeguards;
- [ ] who the controller is and how to contact them (and the DPO, if one is appointed);
- [ ] the security measures, in general terms;
- [ ] whether giving each item is voluntary or required, and under which law if any;
- [ ] what happens if someone doesn't give it;
- [ ] where data is stored, including any country outside Kenya;
- [ ] how long data is kept;
- [ ] how to complain to the ODPC.

## Data protection policy (reg 23)

- [ ] A written policy on how personal data is handled, published (usually on the website) and reviewed regularly. Required for everyone, registered or not.
- [ ] It covers: data held, how to use rights, complaints, purposes, transfers abroad and to third parties, retention, and children's data.

## Sensitive data (s.44–46)

- [ ] Each use of sensitive data has a s.45 ground named: a not-for-profit body's own members, data the person made public, or necessity for a legal claim, legal obligations or rights, or vital interests (`law.md` §5).
- [ ] Nothing sensitive rests on legitimate interests alone. Where only consent fits, it's flagged for the ODPC or a lawyer.
- [ ] Health data is handled by or under a health care provider, or someone with a legal duty of secrecy or confidentiality (s.46).

## Consent, where it's the lawful basis (s.32, 33, 37)

- [ ] It's specific to a purpose, not bundled with what the service needs.
- [ ] It's recorded, with who, when and what was agreed, so it can be proven.
- [ ] Withdrawing is as easy as giving it, and is honoured.
- [ ] Marketing and other commercial use has separate, express consent, and an opt-out on every message (reg 15–17).
- [ ] No sensitive data is used for direct marketing, even with consent (reg 15(1)). Strip fields such as marital status, family details and health from marketing lists and targeting.
- [ ] Requests to stop sharing data with third parties for their marketing are acted on within 7 days (reg 18).
- [ ] Children: a parent's or guardian's consent, and an age check proportionate to the risk.

## Requests from data subjects (Act s.26, 38, 40; deadlines in `law.md` §6)

- [ ] There's a channel (an email address or in-app action) and someone who owns it.
- [ ] Identity is checked before releasing or changing data.
- [ ] Deadlines are tracked: access 7 days; rectification, erasure, objection and restriction 14 days; portability 30 days.
- [ ] Refusals go out in writing, with reasons and the right to complain to the ODPC.
- [ ] Changes and deletions reach the processors that hold copies.
- [ ] An export exists in a machine-readable format (portability).

## Retention schedule (reg 19)

| Data | Purpose | Kept for | Then | Reviewed |
|---|---|---|---|---|

Include backups and logs: they hold the same data.

## Processors (reg 24)

For each processor (hosting, payments, email, SMS, analytics, support tools):
- [ ] a written contract or data processing terms with the particulars in reg 24;
- [ ] where it stores data (a transfer if outside Kenya);
- [ ] it will notify you of breaches within 48 hours;
- [ ] it uses sub-processors only with your authority;
- [ ] it deletes or returns data at the end.

## DPIA screening (s.31; high-risk list in `law.md` §10)

Do a DPIA before launch if any apply:
- [ ] children's or vulnerable people's data;
- [ ] sensitive data (Kenya's wide list);
- [ ] biometric or genetic data;
- [ ] automated decisions or profiling with significant effect;
- [ ] combining datasets from different sources or purposes;
- [ ] large-scale processing, or a new purpose for existing data;
- [ ] a change that raises the risk of an existing service;
- [ ] large-scale systematic monitoring of a public area (CCTV, facial recognition, tracking of shoppers or passengers);
- [ ] new technology used in a new way;
- [ ] processing that stops people using a right.

Submit the DPIA report to the ODPC at least 60 days before processing starts (s.31(5)), so build that into the launch date. If it finds high risk that safeguards don't reduce, that submission is also the prior consultation: the ODPC has 60 days to respond, and silence after 60 days lets processing begin (reg 51).

## Breach readiness (s.43; reg 37–38)

- [ ] A written runbook: who decides, who notifies, and the evidence to keep.
- [ ] The 72-hour clock to the ODPC starts at awareness. Know in advance how to file.
- [ ] Notifiable breaches recognised: a name or ID number with other personal data, or an account identifier with a password or access code.
- [ ] A template for telling affected people what happened and how to protect themselves.
- [ ] Processors bound to tell you within 48 hours.
- [ ] A breach log, including breaches not notified, with the reasons.

## Transfers and hosting (s.48–50; reg 26)

- [ ] Every country where data is stored or processed is listed, including providers' regions and backups.
- [ ] Each transfer has a basis: proof of safeguards, necessity or consent. Sensitive data abroad has consent.
- [ ] Not a reg 26 purpose (education, health care, civil registration and others), or a serving copy is kept in Kenya.

## Security by design (s.41)

- [ ] Collect only what each purpose needs, by default.
- [ ] Encryption in transit and at rest, and pseudonymisation where useful.
- [ ] Access limited to those who need it, and logged.
- [ ] Backups restorable, and restores tested.
- [ ] Safeguards tested periodically.
