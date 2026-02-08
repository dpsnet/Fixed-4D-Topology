# Submission Guide (Format Reference Only)
## RMP Format Guidelines - NOT FOR ACTUAL SUBMISSION

> ⚠️ **IMPORTANT NOTICE**:
> This guide shows the format of *Reviews in Mathematical Physics* and the submission
> process, but the actual paper is **OPEN SOURCE on GitHub** and is **NOT formally
> submitted** to the journal. This document is provided for reference purposes only.

---

## Pre-Submission Preparation (Format Demonstration)

### Step 1: Compile the PDF

```bash
cd /path/to/paper

# Compile the LaTeX
pdflatex Dimensionics_Physics.tex
pdflatex Dimensionics_Physics.tex
pdflatex Dimensionics_Physics.tex
```

### Step 2: Verify Output

Check the generated PDF for:
- [ ] No compilation errors
- [ ] All 7 figures display correctly
- [ ] Page count: 50-60 pages
- [ ] All cross-references work (clickable links)
- [ ] Table of contents generated
- [ ] Abstract and keywords present

**Note**: This demonstrates that the paper follows RMP format guidelines. The actual paper is open source on GitHub.

---

## Online Submission Process

### 1. Register/Login

1. Go to: https://www.worldscientific.com/page/rmp/submission-guidelines
2. Click "Submit Online"
3. Register for an account or log in

### 2. Start New Submission

1. Select "Reviews in Mathematical Physics" as journal
2. Select article type: "Original Article"
3. Enter title: "Dimensionics-Physics: Spectral Dimension Flow and Quantum Gravity"

### 3. Author Information

Enter authors in order:
```
Author 1: [Name], [Affiliation], [Email], [ORCID]
Author 2: [Name], [Affiliation], [Email], [ORCID]
...
```

Corresponding author: Mark the contact author

### 4. Abstract and Keywords

**Abstract** (copy from ABSTRACT.md):
```
We present Dimensionics-Physics, a rigorous mathematical framework treating spacetime 
dimension as a dynamical variable that flows with energy scale. Building upon the 
Fixed-4D-Topology paradigm, we establish nine axioms defining the spectral dimension 
function d_s(μ): M × ℝ⁺ → [2,4] governed by the Master Equation μ ∂_μ d_s = β(d_s). 

Our main results include: (1) Rigorous proof of the UV fixed point lim_{μ → ∞} d_s = 2; 
(2) Modified relativity theory with effective metric g^{eff}_{μν} = (4/d_s)g_{μν} and 
deformed Lorentz group SO(3,1; d_s); (3) Black hole dimension compression d_s(r) = 4 - r_s/r; 
(4) Cosmic dimension evolution d_s(t) = 2 + 2/(1 + e^{-(t-t_c)/τ}).

We derive 11 experimental predictions, including: P1—CMB power spectrum modification 
testable by CMB-S4; and P2—gravitational wave dispersion accessible to LISA. 
Four predictions already agree with data.
```

**Keywords**:
```
spectral dimension, quantum gravity, renormalization group, CMB anisotropies, 
gravitational waves, dimensional reduction, black hole thermodynamics, holographic principle
```

### 5. Upload Files

**Main Document**:
- Upload `Dimensionics_Physics.tex` as "LaTeX Source File"
- Upload `Dimensionics_Physics.pdf` as "PDF Proof"

**Supplementary Files**:
- Upload all `chapters/*.tex` files
- Upload all `appendices/*.tex` files
- Upload all `figures/*.pdf` files

**Cover Letter**:
- Upload `COVER_LETTER.tex` or paste text in "Comments to Editor"

### 6. Additional Information

**Suggested Reviewers** (enter 3-5):
1. Expert in quantum gravity/spectral dimension
2. Expert in RG/asymptotic safety
3. Expert in CMB/cosmology
4. Expert in modified gravity/GWs

**Conflicts of Interest**: Declare none

**Funding**: State if applicable (or "No funding received")

### 7. Review and Submit

1. Review all entered information
2. Verify uploaded files
3. Check author order
4. Confirm corresponding author
5. Click "Submit"

---

## After Submission

### Immediate
- [ ] Save submission confirmation email
- [ ] Note manuscript number
- [ ] Add to calendar: Expected decision date (~3 months)

### During Review
- [ ] Check status periodically
- [ ] Respond promptly to editor queries
- [ ] Prepare for possible revision requests

### Upon Decision

**If Accepted**:
- [ ] Complete copyright forms
- [ ] Respond to any final queries
- [ ] Submit to arXiv

**If Revision Required**:
- [ ] Address all referee comments
- [ ] Prepare response letter
- [ ] Resubmit within deadline

**If Rejected**:
- [ ] Consider alternative journals (see below)
- [ ] Revise based on feedback
- [ ] Submit elsewhere

---

## Alternative Journals

If rejected from RMP, consider:

| Journal | Impact Factor | Website |
|---------|--------------|---------|
| Classical and Quantum Gravity | 3.5 | iopscience.org/cqg |
| Physical Review D | 5.0 | journals.aps.org/prd |
| Journal of Mathematical Physics | 1.3 | aip.org/jmp |
| Annals of Physics | 2.5 | elsevier.com/locate/aop |
| International J. of Modern Physics D | 2.0 | worldscientific.com/ijmpd |

---

## arXiv Submission (After Acceptance)

### Step 1: Prepare Files
```bash
# Create arXiv version (no line numbers, single column)
cp Dimensionics_Physics.tex arxiv_version.tex

# Modify for arXiv if needed
# - Remove cover page
# - Use single column format
```

### Step 2: Upload to arXiv
1. Go to: https://arxiv.org/submit
2. Select category: **gr-qc** (General Relativity and Quantum Cosmology)
3. Also consider: **hep-th**, **math-ph**
4. Upload source files
5. Enter metadata (title, authors, abstract)
6. Submit

### Step 3: Update
- Add arXiv ID to README
- Update citations if published

---

## Troubleshooting

### Compilation Errors

**Missing packages**:
```bash
# Install missing LaTeX packages
# On Ubuntu/Debian:
sudo apt-get install texlive-latex-extra texlive-science

# On macOS with MacTeX:
sudo tlmgr install <package-name>
```

**Figure not found**:
- Ensure figures are in correct directory
- Check file extensions (.pdf not .PDF)

**Cross-reference errors**:
- Run pdflatex 2-3 times
- Check label names match references

### Submission System Issues

**File upload fails**:
- Check file sizes (< 10 MB each)
- Try different browser
- Contact journal technical support

**Timeout**:
- Save work frequently
- Complete submission in stages
- Use stable internet connection

---

## Contact Information

**Journal**: Reviews in Mathematical Physics  
**Publisher**: World Scientific Publishing  
**Editorial Office**: rmp@wspc.com  
**Technical Support**: support@wspc.com

---

## Checklist Before Submitting

- [ ] PDF compiles without errors
- [ ] All figures display correctly
- [ ] Page count: 50-60 pages
- [ ] Abstract: 250 words
- [ ] Keywords: 5-8 terms
- [ ] All authors approved
- [ ] Corresponding author designated
- [ ] Suggested reviewers listed
- [ ] No conflicts of interest
- [ ] Cover letter prepared

---

**Good luck with your submission!**
