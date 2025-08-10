# Legal Fact Checker Research Plan

## Documentation Needed for Legal Fact Checker Implementation

### 1. Official ADA Documentation (Priority: HIGH)
**Use LocalDocs for these - they're reference materials we'll use repeatedly**

- **ADA.gov Service Animals**
  - https://www.ada.gov/resources/service-animals-2010-requirements/
  - https://www.ada.gov/resources/service-animals-faqs/
  - https://www.ada.gov/topics/service-animals/

- **Federal Regulations**
  - https://www.ecfr.gov/current/title-28/chapter-I/part-35/subpart-B/section-35.136 (Title II)
  - https://www.ecfr.gov/current/title-28/chapter-I/part-36/subpart-C/section-36.302 (Title III)

- **DOJ Guidance**
  - https://www.justice.gov/crt/disability-rights-section
  - https://www.justice.gov/crt/animals-service

### 2. State Law Variations (Priority: MEDIUM)
**Use Jina for deep research on state-specific laws**

- California service dog laws
- New York service dog laws
- Texas service dog laws
- Florida service dog laws

### 3. Fact-Checking APIs & Services (Priority: HIGH)
**Use LocalDocs for API documentation**

- **Google Fact Check Tools API**
  - https://developers.google.com/fact-check/tools/api/reference
  
- **Claim Review Schema**
  - https://schema.org/ClaimReview
  
- **Legal Citation Formats**
  - https://www.law.cornell.edu/citation/

### 4. Common Misconceptions Database (Priority: MEDIUM)
**Create our own from research**

- Registration/certification myths
- Emotional support vs service animals
- Handler rights and responsibilities
- Business owner obligations

### 5. Legal Databases & APIs (Priority: LOW - for future enhancement)
- Justia API
- CourtListener API
- Legal Information Institute (Cornell)

## Recommended Collection Strategy

### Step 1: LocalDocs Collection (Reusable References)
```bash
# Collect official ADA documentation
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs add \
  https://www.ada.gov/resources/service-animals-2010-requirements/ \
  https://www.ada.gov/resources/service-animals-faqs/ \
  https://www.ada.gov/topics/service-animals/ \
  https://www.ecfr.gov/current/title-28/chapter-I/part-35/subpart-B/section-35.136 \
  https://www.ecfr.gov/current/title-28/chapter-I/part-36/subpart-C/section-36.302

# Tag and organize
localdocs set [hash] -n "ADA Service Animal Regulations" -d "Official ADA and DOJ guidance on service animals" -t "ada,legal,service-dogs,regulations"

# Export for Claude
localdocs export ada-service-animals --format claude --output docs/legal-references/
```

### Step 2: Jina Research (Deep Analysis)
```bash
# For state-specific variations and edge cases
curl "https://r.jina.ai/https://www.nolo.com/legal-encyclopedia/california-laws-psychiatric-service-dogs-emotional-support-animals-public-places.html" \
  -H "Authorization: Bearer $JINA_API_KEY" > research/legal/california-service-dog-laws.md
```

### Step 3: Build Fact Database
- Create JSON/YAML file with common claims and their verification
- Map claims to authoritative sources
- Include correction templates

## Implementation Approach

### Phase 1: Static Fact Checking
- Hardcoded database of common ADA facts
- Pre-verified claims and corrections
- Citation templates

### Phase 2: Dynamic Verification
- Real-time web scraping of official sources
- Citation validation against ecfr.gov
- Date checking for regulation updates

### Phase 3: AI-Enhanced Checking
- Use LLM to identify claims in content
- Cross-reference with fact database
- Generate correction suggestions

## Key Legal Facts to Verify

1. **Registration/Certification**
   - Claim: "Service dogs must be registered"
   - Truth: No registration or certification required by ADA
   - Source: 28 CFR 35.136(a)

2. **Business Questions**
   - Claim: Various questions businesses can ask
   - Truth: Only 2 questions allowed
   - Source: 28 CFR 36.302(c)(6)

3. **Animal Types**
   - Claim: Various animals as service animals
   - Truth: Only dogs (and miniature horses in some cases)
   - Source: 28 CFR 35.136(a)

4. **Access Rights**
   - Where service dogs are allowed
   - Exceptions (sterile environments, etc.)
   - Handler responsibilities

## Next Steps

1. Run LocalDocs collection for official sources
2. Create `agents/legal_fact_checker.py` with proper structure
3. Build fact verification database
4. Implement claim extraction logic
5. Add citation validation
6. Create correction suggestion system