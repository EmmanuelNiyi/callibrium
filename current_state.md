# 📌 Current Progress on the Modular Schedule Generator (Pre-PoC / Early Development)

I’ve developed the earliest version of the **modular roster generator** as a pre–proof-of-concept using **Google OR-Tools**. This version builds on the original 7-day prototype to handle multiple shifts, weekend-specific rules, and configurable constraints, while preserving the core principle of **modularity**—allowing constraints to be plug-and-play.

---

## **Scope of This Version**

- **Timeframe:** Configurable via `start_date` and `end_date` (full month support).
- **Shifts:** Multiple shift types per day (e.g., `"Ward"` and `"Emergency"`).
- **Users:** Multiple assignees can be scheduled dynamically.
- **Weekends:** Weekend detection built-in, with optional weekend-specific coverage and fairness rules.

---

## **Constraints Implemented**

1. **Coverage Constraint** – enforces minimum and maximum assignees per shift, configurable by:
    - Weekday vs weekend
    - Shift type (e.g., Ward vs Emergency)
2. **Fairness Constraint (Soft)** – balances total shifts per assignee; can be configured as `tight`, `medium`, `loose`, or `soft`.
    - Weekend fairness can be applied separately to ensure fair distribution of weekend shifts.
3. **No-Consecutive Constraint** – ensures minimum spacing between assignments, preventing back-to-back shifts or consecutive-day scheduling.
4. **Unavailability / Optional Extension** – supports preventing assignments for unavailable assignees (ready for integration).

---

## **Outputs**

- Schedule by **date and shift**, highlighting weekends.
- Total shifts per assignee, including breakdown of weekday vs weekend shifts.
- **Export Options:**
    - **CSV** – for spreadsheet or data analysis.
    - **HTML** – easy-to-read, human-friendly schedule visualization.

---

## **Design Principles Preserved**

- **Modularity:** Each constraint is implemented independently and can be toggled or extended.
- **Scalability:** The architecture supports:
    - More days (monthly schedules).
    - Multiple shifts per day.
    - Additional rules, e.g., preferences, roles, weighted fairness.
- **Flexibility:** Shift labels are configurable; weekend and weekday rules can differ without changing code.

---

## **Next Steps / Future Enhancements**

- Weighted fairness to prioritize certain shift types.
- Preference-based assignment per assignee.
- Soft constraints for coverage to allow slight deviations when perfect coverage is impossible.
- Additional export formats (PDF/Excel) and integrations.

---

✅ **Current Status:**

The foundation is fully functional — schedules can be generated for a configurable date range, multiple shifts per day, with coverage, fairness, no-consecutive, and weekend rules applied. Exports to CSV and HTML are operational.

---