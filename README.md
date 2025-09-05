# Traditional RCM
=================

Eligibility → Prior-auth approval → Clinical documentation → 

Medical coding → Claims scrubbing → Claims submission → 

Remittance tracking → Denial management → Claims resubmission → Remittance tracking → Reconciliation.


# Architecture
=================

A. Microservices
================
- Agents are individual or grouped together according to their responsibilities.
- Each exists in its own docker container, grouped by a single docker compose file.

AGENTS
================
1. Eligibility Agent
- It prequalifies patients for insurance coverage.
- A patient is required to upload their medical insurance card.
- It then uses a combination of 1) OCR and 2)an LLM to extract info from the card.
- And looks this information up against known records.
- If the patient is eligible; it sends a request to the next step.
- If the patient is ineligible it flags them as ineligible.

2. Prior-auth Approval Agent

3. Clinical documentation Agent

B. Persistence
================
- Redis key-value store for overall system state.
- Redis Queues for message passing between services/ asynchronous processing.
- LangGraph checkpointing for agent / workflow state.