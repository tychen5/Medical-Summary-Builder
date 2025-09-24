# Custom Table: Timeline of Medical Events

Generate a table summarizing the claimant's medical history. Each row should represent a distinct medical event, consultation, or procedure.

## Table Columns

1.  **DATE**: The date of the medical event in `MM/DD/YYYY` format. Use the treatment or service date.
2.  **PROVIDER**: The name of the medical facility, clinic, or physician (e.g., "Willow Creek Med Ctr").
3.  **REASON**: A concise summary of the reason for the visit, diagnosis, or procedure (e.g., "Hip pain, X-ray arthritis", "Right total hip replacement").
4.  **REF**: The page number from the source PDF where the event is documented. Format it as "Pg X", where X is the actual page number of the PDF document.

## Extraction Criteria

- Focus on significant medical encounters, such as specialist consultations, hospitalizations, surgical procedures, imaging results, and new diagnoses.
- Exclude routine administrative entries or non-substantive follow-ups unless they indicate a change in condition.
- Ensure events are listed in chronological order.

## Example Row

| DATE       | PROVIDER               | REASON                        | REF   |
|------------|------------------------|-------------------------------|-------|
| 09/15/2022 | Willow Creek Med Ctr   | Hip pain, X-ray arthritis     | Pg 19 |
