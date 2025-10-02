R1 = "R1 – Identity & Registry: Required: UEI (12 chars), DUNS (9 digits), and active SAM.gov registration. Primary contact must have valid email and phone."
R2 = "R2 – NAICS & SIN Mapping (subset for test): 541511 → 54151S; 541512 → 54151S; 541611 → 541611; 518210 → 518210C"
R3 = "R3 – Past Performance: At least 1 past performance ≥ $25,000 within last 36 months. Must include customer name, value, period, and contact email."
R4 = "R4 – Pricing & Catalog (starter rules): Provide labor categories and rates in a structured sheet. If missing rate basis or units, flag “pricing_incomplete”."
R5 = "R5 – Submission Hygiene: All personally identifiable info must be stored in redacted form; only derived fields and hashes are stored by default."

RULES = {"R1": R1, "R2": R2, "R3": R3, "R4": R4, "R5": R5}
