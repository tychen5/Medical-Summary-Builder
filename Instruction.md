# **Developer Test: Medical Summary Builder**

## **Objective**

Using any Large Language Model (LLM), build a pipeline that ingests a disability/medical case file (sample provided: *Medical File.pdf*) and produces a **completed medical summary** that follows the format in *Medical Summary.docx*.

## **Bonus**

At times attorneys will want to customize their own tables, for example, they provide 5 columns of Data, Facility, Physician, Summary and Ref or other layout they like. Think about how you can take a plain text instruction from a user and create the report on different layout they would request.

---

## **Inputs**

1. **Template:** *Medical Summary.docx* — shows the required structure and fields.

2. **Source Data:** *Medical File.pdf* — synthetic claimant record with medical history, impairments, treatments, and SSA determinations.

---

## **Expected Output**

* A filled-in **Medical Summary** in the same format as the template, with key fields completed:

  1. Claimant name, SSN, DOB, AOD, DLI, Age, Education, etc.

  2. Alleged impairments (from case record).

  3. Timeline of medical events: Date | Provider | Reason | REF (use the **page number** from the PDF).

* Deliverables: **Text document** (Word or PDF) that mirrors the template but populated with extracted details.

---

## **Example (abbreviated)**

**Text version (based on template):**

MEDICAL SUMMARY

RE: Arthur Miller    SSN: 456-12-7890    Title: T16    DLI: 07/14/2022  
AOD: 07/01/2022      Date of Birth: 05/21/1965    Age at AOD: 57    Current Age: 59  
Last Grade Completed: 12     Attended Special Ed Classes: No

Last Updated: Thursday, September 11, 2025 – COMPLETED THROUGH F

DATE          PROVIDER                   REASON                          REF  
09/15/2022    Willow Creek Med Ctr        Hip pain, X-ray arthritis       Pg 19  
01/27/2023    Central Plains Med Ctr      R hip pain, arthroplasty eval   Pg 91  
02/08/2023    Central Plains Med Ctr      Right total hip replacement     Pg 91  
04/13/2023    Metro Health & Wellness     Post-op follow-up, stable       Pg 14  
07/06/2023    Sterling Health Clinic      Breast lump, hypertension       Pg 16

---

## **Deliverables**

1. **Source code** in a GitHub repo (or zip) including:

2. **README.md** with instructions to run locally.

3. **Sample Report** using the provided *Medical File.pdf*.

---

## **Notes**

### Q&A

* Q: In "Medical File.pdf," it seems the table of contents (“Pg” column) at the front of the pdf doesn’t precisely match all the actual pages in the PDF. Is the expectation to align the page numbers with the table of contents at the front of the PDF, or should they reference the true PDF page sequence?
  * A: We usually do not utilize any table of contents from the source file "Medical File.pdf" because the table of content might not be reliable. The expectation would be the page number of the source file.
* Q: For the “Timeline of Medical Events” table, should the “REF” page number refer to the table of contents (“Pg” column) at the front of the pdf, or to the true PDF page number (out of 504)?
  * A: Correct, a good REF example can be "Medical File.pdf (12/504), which is the actual page 12 of the file
* Q: For populating the “Timeline of Medical Events” dates, should I mainly use the start date of Treatment Date from "F. Medical Records" in the table of contents at the front of the pdf, or should I search through the full PDF for other service of dates? Since I don’t have a medical background, could you suggest criteria, similar to those for a doctor/lawyer, for which dates/events are worth including in the timeline?
  * A: The treatment start date will be the great, usually we base on the 3 factors, (Date/Physician) would be the unique attribute for medical visit, for example:
    2025-08-01 Dr Smith: .......
    2025-08-01 Dr Walker: .......
    2025-08-03 Dr Smith: .......