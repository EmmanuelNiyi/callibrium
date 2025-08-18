# 📌 Current Progress on the Modular Schedule Generator (Pre-PoC)

I’ve built the earliest version of the modular roster generator as a **pre–proof of concept** using Google OR-Tools. The focus at this stage was to keep the setup extremely small and simple while still capturing the **core principle of modularity** — making constraints plug-and-play.  

---

## Scope of This Version
- **Timeframe:** 7 days (1 week).  
- **Shifts:** Only **one shift per day** (no multiple shifts yet).  
- **Users:** Multiple assignees can be scheduled.   

---

## Constraints Implemented
1. **Coverage constraint** – each day has a required number of assignees.  
2. **Rest constraint** – ensures minimum spacing between assignments (no back-to-back scheduling if rest is required).  
3. **Unavailability constraint** – prevents assigning a person on days they are marked as unavailable.  
4. **Fairness (soft)** – balances the total number of shifts per person so workloads are distributed as evenly as possible.  

---

## Outputs
- A valid schedule assigning people to shifts across 7 days.  
- For each person, the total number of shifts assigned is also returned.  
- If perfect fairness isn’t possible, the solver minimizes the imbalance (soft constraint).  

---

## Design Principles Preserved
- **Modularity:** Each constraint was added in a way that it can be toggled or extended later.  
- **Scalability Ready:** The structure can naturally expand to:  
  - More days (e.g., a full month).  
  - Multiple shifts per day.  
  - Additional rules such as weekend fairness, role types, or individual preferences.  

---

👉 This means the **foundation is working**: we already have a functioning modular scheduler for a 7-day, 1-shift-per-day setup, with core coverage, rest, availability, and fairness rules in place.

