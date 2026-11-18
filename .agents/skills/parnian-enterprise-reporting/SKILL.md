---
name: parnian-enterprise-reporting
description: Plan, design, implement, or validate Parnian enterprise analytics, BI dashboards, KPIs, SQL Server reports, Blazor and SharePoint reporting, Power BI Desktop or Report Server models and reports, and Persian RTL PDF, Excel, CSV, and printable exports. Use for reporting requirements, report architecture, data analysis, export consistency, and reporting audits.
---

# Parnian Enterprise Reporting

Select complementary skills using [routing](references/routing.md). State the skills selected and the reason for each. Load only the references needed for the current stage and target.
Track deliverables in the [workflow record](assets/workflow.md).

1. **Discover requirements.** Record users, roles, decisions, KPIs, data sources, grain, filters, access rules, cadence, volume, and exports in the [requirements template](assets/requirements.md). Leave missing business definitions open and seek resolution when they affect the result.
2. **Analyze data.** Prefer read-only schema and sample inspection. Establish fact and dimension grain, keys, joins, nulls, duplicates, aggregation behavior, freshness, and performance constraints. Keep production data unchanged.
3. **Define KPIs.** Fill in the [KPI template](assets/kpi.md) for every KPI. Share definitions across web, Power BI, Excel, and PDF. Keep missing data distinct from zero.
4. **Propose architecture.** Choose the reporting pattern and explain the source, semantic layer, authorization, delivery target, and export approach. Read [architecture and UX](references/architecture.md).
5. **Plan the UX and acceptance criteria.** Default to Persian RTL and Jalali dates for all user-facing reporting surfaces. Document interaction and accessibility with the [acceptance template](assets/acceptance.md).
6. **Implement after approval.** Obtain approval for requirements, architecture, UX, and acceptance criteria before implementation. Use the approved target and its verified feature set. Keep cloud publication and production actions within the explicit authorization. Read [Power BI](references/power-bi.md) or [exports](references/exports.md) when relevant.
7. **Validate.** Use the [validation checklist](assets/validation.md). Where feasible, reconcile outputs against independently computed SQL or fixtures. Report test evidence and unresolved limitations.
