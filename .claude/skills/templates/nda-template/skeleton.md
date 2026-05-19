# NDA Skeleton (Universal — All Variants Inherit)

> Universal 10-section frame for Non-Disclosure Agreements. Variants in `variants/`
> fill in directionality (one-way / mutual / multi-party) and tone. Customer slots
> marked `{LIKE_THIS}`.

---

# NON-DISCLOSURE AGREEMENT

**Effective Date:** {EFFECTIVE_DATE}

## 1. Parties

This Non-Disclosure Agreement ("Agreement") is entered into by:

**{PARTY_A_LEGAL_NAME}**, {PARTY_A_ENTITY_TYPE} with principal place of business at {PARTY_A_ADDRESS} ("{PARTY_A_SHORT_NAME}")

{IF_MUTUAL: AND}
{IF_MULTI_PARTY: AND}

**{PARTY_B_LEGAL_NAME}**, {PARTY_B_ENTITY_TYPE} with principal place of business at {PARTY_B_ADDRESS} ("{PARTY_B_SHORT_NAME}")

{IF_MULTI_PARTY: AND additional parties — repeat block per signer}

Collectively the "Parties," individually a "Party."

## 2. Recitals

WHEREAS, the Parties wish to discuss {PURPOSE_OF_DISCLOSURE — e.g., "a potential business relationship regarding this system deployment for {PARTY_B_SHORT_NAME}'s operations"}, and in connection with such discussions one or both Parties may disclose confidential information; and

WHEREAS, the Parties wish to protect such confidential information from unauthorized disclosure;

NOW THEREFORE, in consideration of the mutual promises and covenants set forth herein, the Parties agree as follows:

## 3. Definition of Confidential Information

"Confidential Information" means any non-public information disclosed by one Party (the "Disclosing Party") to the other Party (the "Receiving Party") in connection with the discussions described above, including but not limited to:

(a) **Technical information** — product know-how, formulas, designs, software code, test results, processes, inventions, research projects, technical correspondence;

(b) **Business information** — cost data, profits, sales information, accounting, business plans, markets and marketing methods, customer lists, purchasing techniques, supplier lists, advertising strategies;

(c) **Personnel information** — employee names, salaries, skills, organizational structure;

(d) **Third-party information** — information submitted to the Disclosing Party by customers, suppliers, contractors, or partners that the Disclosing Party is obligated to keep confidential; and

(e) **Other information** — any information not generally known to the public which, if misused or disclosed, could reasonably be expected to adversely affect the Disclosing Party's business.

Confidential Information may be disclosed in tangible, oral, visual, or any other form, and includes "Confidential Materials" — the physical or digital embodiments thereof.

## 4. Confidentiality Obligations

The Receiving Party shall:

(a) Not disclose Confidential Information to any third party except to the Receiving Party's directors, officers, employees, and contractors who have a need to know for the purposes of this Agreement and are bound by written confidentiality obligations at least as restrictive as those herein ("Representatives");

(b) Use at least the same degree of care to safeguard Confidential Information as it uses to protect its own confidential information, and in any event not less than reasonable care;

(c) Make copies of Confidential Materials only as needed for the purposes of this Agreement;

(d) Be responsible for any breach of this Agreement by its Representatives.

## 5. Carve-Outs (Information NOT Covered)

Confidential Information does NOT include information that:

(a) Was in the public domain at the time of disclosure;

(b) Becomes public after disclosure other than through a breach of this Agreement;

(c) Was already in the Receiving Party's possession prior to disclosure, demonstrated by written records;

(d) Is independently developed by the Receiving Party without use of or reference to Confidential Information, demonstrated by written records;

(e) Is received from a third party who did not acquire it under any confidentiality obligation to the Disclosing Party.

## 6. Compelled Disclosure

If the Receiving Party is required by legal process or governmental authority to disclose Confidential Information, the Receiving Party shall (where legally permitted) give prompt notice to the Disclosing Party so it may seek a protective order. Receiving Party shall disclose only the portion legally required and shall cooperate to minimize the scope and effects of such disclosure.

## 7. Term & Survival

This Agreement is effective as of the Effective Date and continues until {TERM_LENGTH — typical: "two (2) years from the Effective Date"}. The obligations of confidentiality with respect to Confidential Information disclosed during the term shall survive for {SURVIVAL_PERIOD — typical: "three (3) years from the date of disclosure"}, except for trade secrets which shall remain protected until they enter the public domain through no fault of the Receiving Party.

## 8. Remedies

The Parties acknowledge that breach of this Agreement may cause irreparable harm for which monetary damages are inadequate. The Disclosing Party shall be entitled, without prejudice to other available remedies, to seek immediate injunctive or equitable relief. The Receiving Party hereby waives any requirement that the Disclosing Party post a bond as a condition to obtaining such relief.

## 9. Governing Law & Venue

This Agreement is governed by the laws of the State of {GOVERNING_LAW_STATE} without regard to its conflicts-of-law principles. The Parties consent to the exclusive jurisdiction of the federal and state courts located in {COUNTY}, {GOVERNING_LAW_STATE} for any dispute arising hereunder.

In any action arising under this Agreement, the prevailing Party shall be entitled to recover its reasonable attorneys' fees and costs.

## 10. Miscellaneous

(a) **Entire Agreement.** This Agreement constitutes the entire agreement between the Parties regarding its subject matter and supersedes all prior negotiations.

(b) **No Other Rights.** Nothing in this Agreement grants any Party a license under any patent, copyright, trade secret, or other intellectual property right of the other Party, except the limited right to review Confidential Information for the purpose of evaluating the contemplated relationship.

(c) **No Obligation to Proceed.** Nothing in this Agreement obligates any Party to enter into any further business relationship.

(d) **Assignment.** No Party shall assign this Agreement without prior written consent of the other Parties.

(e) **Notices.** Notices shall be in writing and delivered to the addresses listed in Section 1.

(f) **Severability.** If any provision is held unenforceable, the remainder of this Agreement shall remain in effect.

(g) **Modification.** No modification is valid unless in writing and signed by all Parties.

---

# Sign-Off

**{PARTY_A_LEGAL_NAME}:**

___________________________
{PARTY_A_SIGNATORY_NAME}, {PARTY_A_TITLE}
Date: ___________

**{PARTY_B_LEGAL_NAME}:**

___________________________
{PARTY_B_SIGNATORY_NAME}, {PARTY_B_TITLE}
Date: ___________

{IF_MULTI_PARTY: Repeat signer block per additional party}

---

## Slot Glossary

| Slot | Description |
|---|---|
| `{PARTY_A_LEGAL_NAME}` / `{PARTY_B_LEGAL_NAME}` | Registered legal entity name |
| `{PARTY_A_ENTITY_TYPE}` | "a Delaware corporation" / "an LLC" / "an individual" |
| `{PARTY_A_ADDRESS}` | Registered business address |
| `{PARTY_A_SHORT_NAME}` | Defined term used elsewhere in doc (e.g., "this system") |
| `{PURPOSE_OF_DISCLOSURE}` | Why the parties are talking (specific is better than generic) |
| `{EFFECTIVE_DATE}` | When the NDA starts |
| `{TERM_LENGTH}` | How long the NDA is active (typical: 2 years) |
| `{SURVIVAL_PERIOD}` | How long confidentiality survives termination (typical: 3 years) |
| `{GOVERNING_LAW_STATE}` | State law governing (typical for this system: Tennessee) |
| `{COUNTY}` | County for jurisdiction |
