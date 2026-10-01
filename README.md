# RxGuard

## Evidence-Proven Prescription Review for Pharmacists

RxGuard is a pharmacist-facing prescription review system designed to identify medication-safety concerns and provide evidence-backed explanations while keeping the final clinical decision with the pharmacist.

RxGuard combines deterministic safety checks, structured drug-interaction data, clinical evidence retrieval, AI-assisted explanations, claim verification, and pharmacist review into a single workflow.

---

## Core Principle

> The LLM handles language. Tools handle facts, math, and decisions.

RxGuard does not rely on an LLM alone for medication-safety decisions.

Structured databases and deterministic tools handle factual checks. Retrieval tools provide supporting clinical evidence. The LLM is used primarily for language understanding and explanation.

---

## Problem

Prescription review can require pharmacists to manually verify information across multiple sources.

A prescription may contain:

- Multiple medications
- Brand names or ambiguous drug names
- Potential drug-drug interactions
- Duplicate active ingredients
- Safety-critical situations
- Questions requiring clinical guideline evidence

Traditional rule-based systems can identify structured problems but may provide limited explanations.

General-purpose AI systems can explain medical information but may generate unsupported claims, misinterpret missing information, or provide inappropriate clinical recommendations.

RxGuard combines deterministic verification with evidence-grounded AI while maintaining pharmacist oversight.

---

## Solution

RxGuard follows a deterministic-first architecture.

```text
Prescription
     |
     v
Drug Identification
     |
     v
Deterministic Safety Checks
     |
     v
Structured Interaction Lookup
     |
     v
Clinical Evidence Retrieval
     |
     v
AI Explanation
     |
     v
Claim Verification
     |
     v
Pharmacist Review
     |
     v
Tamper-Evident Audit
```

The system is designed so that every important safety-related claim can be traced back to structured data or supporting evidence.

---

## Key Features

### Deterministic Drug Interaction Checking

Prescription drug pairs are checked against a structured and versioned interaction database.

The system evaluates all relevant drug pairs rather than relying on an LLM to determine whether an interaction exists.

### Drug Normalization

RxGuard resolves prescription entries to canonical drug identities using:

- Exact alias matching
- Longest-match resolution
- Fuzzy matching
- Candidate generation
- Controlled LLM-assisted selection
- Pharmacist confirmation for unresolved cases

The LLM is not allowed to invent a drug identity.

### Duplicate Ingredient Detection

The system detects duplicate active ingredients