# MSA Skeleton (Universal — Pro-Customer & Pro-Provider Variants Inherit)

> Universal 17-section frame for Master Services Agreements. Customer slots
> marked `{LIKE_THIS}`. Pro-customer vs pro-provider variants in `variants/`
> override 7 specific clauses (IP ownership, liability cap, change-order
> judgment authority, termination for convenience, indemnification scope,
> warranty disclaimer breadth, payment terms latitude).

---

# MASTER SERVICES AGREEMENT

**Effective Date:** {EFFECTIVE_DATE}

This Master Services Agreement ("Agreement") is entered into between:

**{PROVIDER_LEGAL_NAME}**, a {PROVIDER_ENTITY_TYPE} with principal place of business at {PROVIDER_ADDRESS} ("Provider"), and

**{CUSTOMER_LEGAL_NAME}**, a {CUSTOMER_ENTITY_TYPE} with principal place of business at {CUSTOMER_ADDRESS} ("Customer").

**Recitals:**
WHEREAS, Provider is engaged in the business of providing {SERVICES_DESCRIPTION}; and
WHEREAS, Customer wishes to engage Provider to perform such services from time to time pursuant to separately executed Statements of Work;
NOW THEREFORE, in consideration of the mutual covenants set forth herein, the parties agree as follows.

## 1. Definitions

For purposes of this Agreement, the following capitalized terms have the meanings set forth below:

- **"Acceptance"** has the meaning in Section 6.
- **"Acceptance Tests"** means tests conducted per a Statement of Work to determine whether a Deliverable meets its Specifications.
- **"Affiliate"** means any entity that directly or indirectly controls, is controlled by, or is under common control with a Party.
- **"Background Technology"** means all software, data, know-how, methodologies, specifications, libraries, tools, and other technology owned or licensed by Provider prior to or independent of this Agreement, including any improvements thereto developed during the Term that are general-purpose and not Customer-specific.
- **"Confidential Information"** means non-public information disclosed by a Party that is marked confidential or that a reasonable person would understand to be confidential, including business information, technical information, customer information, and the terms of this Agreement.
- **"Customer-Owned Work Product"** means all Deliverables created specifically for Customer under a Statement of Work, excluding Background Technology, Approved Open-Source Components, and Approved Third-Party Materials.
- **"Deliverables"** means all software, documents, work product, and other materials delivered to Customer under a Statement of Work.
- **"Documentation"** means user manuals, technical manuals, and other documentation that describes a Deliverable.
- **"Effective Date"** is the date first written above.
- **"Fees"** has the meaning in Section 7.
- **"Force Majeure"** has the meaning in Section 14.
- **"Harmful Code"** means viruses, trojans, worms, backdoors, time bombs, or any code designed to disable or interfere with software, hardware, or systems.
- **"Intellectual Property Rights"** means all patents, trademarks, copyrights, trade secrets, and other intellectual property rights worldwide.
- **"Services"** means the services described in a Statement of Work.
- **"Statement of Work" or "SOW"** means a written statement describing services, deliverables, fees, schedule, and acceptance criteria, executed by both Parties and incorporated by reference into this Agreement.

## 2. Services & Statements of Work

Provider shall perform Services for Customer pursuant to one or more Statements of Work executed by both Parties. Each SOW is incorporated into and governed by this Agreement. In the event of conflict between this Agreement and an SOW, the SOW controls only for terms expressly identified as overriding this Agreement.

## 3. Changes & Change Orders

Either Party may request changes to a Statement of Work via written Change Request describing the proposed change, rationale, and expected effect on schedule and Fees. {VARIANT_FLIP: pro-customer = "Provider shall provide a Change Proposal within 5 business days for Customer's approval. No change is effective until both Parties sign a Change Agreement." | pro-provider = "Provider shall assess the change and, at Provider's sole discretion, determine whether it requires schedule extension or additional Fees. No change is effective until both Parties sign a Change Agreement."}

## 4. Customer Responsibilities

Customer shall: (a) provide timely access to information, personnel, and systems required for Provider to perform Services; (b) designate a single point of contact with decision authority; (c) respond to Provider questions and Deliverable reviews within {RESPONSE_WINDOW — typical: "five (5) business days"}; (d) be responsible for the accuracy of all Customer-supplied data and content; (e) maintain its own systems and infrastructure unless explicitly contracted otherwise.

If Customer fails to meet its responsibilities and such failure delays Provider, Provider's timelines extend by the period of delay and Customer remains obligated to make payments on the original schedule.

## 5. Personnel & Subcontractors

Provider may use its employees, contractors, and approved subcontractors to perform Services. Provider remains responsible for the work product and compliance of all such personnel.

## 6. Acceptance & Testing

Customer shall test each Deliverable per the Acceptance Tests specified in the applicable SOW. Customer shall notify Provider of any non-conformity in writing within {ACCEPTANCE_WINDOW — typical: "ten (10) business days"} of delivery. If Customer fails to provide written notice within such period, the Deliverable is deemed Accepted.

If Customer identifies non-conformity, Provider shall make reasonable efforts to correct it. Upon correction, the acceptance procedure repeats.

## 7. Fees, Expenses & Invoicing

Customer shall pay Provider Fees as specified in each SOW. Unless an SOW states otherwise:

(a) Invoices are due **Net {PAYMENT_TERMS — typical: "fifteen (15)"} days** from receipt.

(b) Late payments accrue interest at **1.5% per month** or the maximum permitted by law, whichever is lower.

(c) Provider may **suspend Services with seven (7) days' written notice** if invoices remain unpaid past their due date.

(d) Customer shall reimburse Provider for reasonable out-of-pocket expenses (travel, lodging, third-party software licenses) pre-approved in writing.

## 8. Taxes

All Fees are exclusive of taxes. Customer is responsible for all sales, use, value-added, and similar taxes arising from this Agreement, except taxes on Provider's net income.

## 9. Intellectual Property & License

(a) **Customer-Owned Work Product.** {VARIANT_FLIP: pro-customer = "All Customer-Owned Work Product is deemed a 'work made for hire' for Customer. To the extent it is not, Provider hereby irrevocably assigns to Customer all right, title, and interest in such Work Product, including all Intellectual Property Rights therein." | pro-provider = "Customer is granted a perpetual, non-exclusive, royalty-free license to use the Customer-Owned Work Product for its internal business purposes. Provider retains all underlying Intellectual Property Rights."}

(b) **Background Technology.** Provider retains all rights in Background Technology. Provider grants Customer a non-exclusive, non-transferable license to use Background Technology solely as embedded in or necessary for the use of Customer-Owned Work Product.

(c) **Approved Open-Source / Third-Party Materials.** Any open-source or third-party components included in a Deliverable must be disclosed in the SOW and approved by Customer. Customer's rights in such components are subject to the applicable third-party license terms.

(d) **Restrictions.** Customer shall not (i) reverse engineer Background Technology, (ii) remove Provider's proprietary notices, or (iii) sublicense Background Technology to third parties without Provider's written consent.

## 10. Confidentiality

Each Party shall hold the other's Confidential Information in confidence and use it only for purposes of this Agreement. Confidentiality obligations survive termination for **three (3) years**.

Standard carve-outs apply: Confidential Information does not include information that (a) is or becomes public through no breach, (b) was already in the Receiving Party's possession, (c) is independently developed without reference to Disclosing Party's information, or (d) is received from a third party without confidentiality obligation.

## 11. Warranties

Provider warrants that: (a) Services will be performed in a professional and workmanlike manner by appropriately qualified personnel; (b) Deliverables will materially conform to their Specifications for **{WARRANTY_PERIOD — typical: "ninety (90) days"}** following Acceptance; (c) Deliverables do not contain Harmful Code; (d) Deliverables do not, to Provider's knowledge, infringe third-party Intellectual Property Rights.

EXCEPT AS EXPRESSLY SET FORTH HEREIN, PROVIDER MAKES NO WARRANTIES, EXPRESS OR IMPLIED, INCLUDING ANY WARRANTY OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.

## 12. Indemnification

(a) **Provider Indemnity.** Provider shall defend and indemnify Customer against third-party claims that a Deliverable infringes a U.S. patent, copyright, or trade secret, except claims arising from (i) Customer's modifications, (ii) combination with materials not provided by Provider, or (iii) Customer's use outside the scope of the license granted.

(b) **Customer Indemnity.** Customer shall defend and indemnify Provider against third-party claims arising from Customer-supplied content, data, or specifications, including claims of intellectual property infringement related thereto.

## 13. Limitation of Liability

EXCEPT FOR (i) BREACH OF CONFIDENTIALITY OBLIGATIONS, (ii) INDEMNIFICATION OBLIGATIONS, OR (iii) GROSS NEGLIGENCE OR WILLFUL MISCONDUCT:

(a) Neither Party shall be liable for any indirect, incidental, special, consequential, or punitive damages, including lost profits or lost data.

(b) Each Party's aggregate liability under this Agreement is limited to {LIABILITY_CAP — pro-customer: "ten times (10x)" / pro-provider: "one times (1x)"} the Fees paid by Customer to Provider during the **twelve (12) months preceding the event giving rise to the claim**.

## 14. Force Majeure

Neither Party is liable for delays or failures caused by events beyond its reasonable control, including acts of God, war, terrorism, pandemic, governmental action, strikes, power or network outages, third-party software failures, AI provider outages, or AI model deprecation. The affected Party shall notify the other promptly and resume performance as soon as reasonably practicable.

## 15. Term & Termination

(a) This Agreement begins on the Effective Date and continues until terminated.

(b) Either Party may terminate this Agreement for material breach if the breach is not cured within **thirty (30) days** of written notice.

(c) {VARIANT_FLIP: pro-customer = "Customer may terminate for convenience with sixty (60) days' written notice." | pro-provider = "Neither Party may terminate for convenience; termination requires breach or mutual agreement."}

(d) Upon termination, Customer shall pay all Fees earned through the effective date of termination. Confidentiality, IP, indemnification, and limitation of liability survive termination.

## 16. Governing Law & Venue

This Agreement is governed by the laws of the State of **{GOVERNING_LAW_STATE — default for this system: Tennessee}** without regard to its conflicts-of-law principles. The Parties consent to the exclusive jurisdiction of the federal and state courts located in {COUNTY}, {GOVERNING_LAW_STATE}. In any action arising hereunder, the prevailing Party is entitled to recover reasonable attorneys' fees and costs.

## 17. Miscellaneous

(a) **Entire Agreement.** This Agreement (together with all executed SOWs) is the entire agreement between the Parties regarding its subject matter.

(b) **Notices.** Notices shall be in writing to the addresses above or as updated by written notice.

(c) **Assignment.** Neither Party may assign without the other's prior written consent, except in connection with a merger or sale of substantially all assets.

(d) **Severability.** If any provision is held unenforceable, the rest of the Agreement remains in effect.

(e) **Waiver.** No waiver is effective unless in writing.

(f) **Counterparts.** This Agreement may be executed in counterparts, including electronic signatures.

---

# Sign-Off

**{PROVIDER_LEGAL_NAME}:**

___________________________
{PROVIDER_SIGNATORY_NAME}, {PROVIDER_TITLE}
Date: ___________

**{CUSTOMER_LEGAL_NAME}:**

___________________________
{CUSTOMER_SIGNATORY_NAME}, {CUSTOMER_TITLE}
Date: ___________

---

## The Seven Variant Flips (Pro-Customer vs Pro-Provider)

Where the skeleton has `{VARIANT_FLIP: ...}`, the variant file determines which side:

| Clause | Pro-Customer (default for enterprise customers) | Pro-Provider (default for this system-authored MSAs) |
|---|---|---|
| § 3 Change-order judgment | Both Parties must agree before change is effective | Provider has sole discretion to assess schedule/cost impact |
| § 9(a) IP ownership | Work-for-hire / full assignment to Customer | License to Customer / Provider retains underlying rights |
| § 11 Warranty disclaimer | Narrower disclaimer, more carve-outs preserved | Broader disclaimer of implied warranties |
| § 12(a) Provider indemnity scope | Broader — includes "to Provider's knowledge" + active duty to investigate | Narrower — limited to U.S. registered IP, not trade secrets |
| § 13(b) Liability cap | 10x fees paid | 1x fees paid |
| § 15(c) Termination for convenience | Customer may terminate with 60 days' notice | No termination for convenience |
| § 7 Payment latitude | Net 30, late fee 1% | Net 15, late fee 1.5%, suspension rights |

Variant files at `variants/pro-customer.md` and `variants/pro-provider.md`
contain these 7 clause overrides.

## Slot Glossary

| Slot | Description | Default for this system |
|---|---|---|
| `{PROVIDER_LEGAL_NAME}` | "this system LLC" or similar | TBD on incorporation |
| `{PROVIDER_ENTITY_TYPE}` | "a Tennessee limited liability company" | LLC, Tennessee |
| `{PROVIDER_ADDRESS}` | Business address | your city |
| `{CUSTOMER_LEGAL_NAME}` | Customer's legal entity name | per customer |
| `{SERVICES_DESCRIPTION}` | "AI infrastructure services and the this system" | locked |
| `{RESPONSE_WINDOW}` | Customer response time SLA | 5 business days |
| `{ACCEPTANCE_WINDOW}` | Acceptance review period | 10 business days |
| `{PAYMENT_TERMS}` | Net N days | 15 (pro-provider) / 30 (pro-customer) |
| `{WARRANTY_PERIOD}` | Workmanship warranty | 90 days |
| `{LIABILITY_CAP}` | Multiplier | 1x (pro-provider) / 10x (pro-customer) |
| `{GOVERNING_LAW_STATE}` | State law | Tennessee |
| `{COUNTY}` | Jurisdiction county | Davidson County |
