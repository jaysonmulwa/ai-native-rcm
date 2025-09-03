pip install -r requirements.txt

Traditional RCM
=================

Eligibility → Prior-auth approval → Clinical documentation → 

Medical coding → Claims scrubbing → Claims submission → 

Remittance tracking → Denial management → Claims resubmission → Remittance tracking → Reconciliation.


Architecture
=================

A. Microservices
================
- Agents are individual or grouped together according to their responsibilities.
- Each exists in its own docker container, grouped by a single docker compose file.

B. Persistence
================
- Redis key-value store for overall system state.
- Redis Queues for message passing between services/ asynchronous processing.
- LangGraph checkpointing for agent / workflow state.