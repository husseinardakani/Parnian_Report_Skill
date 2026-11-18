# Skill routing

Use the active Codex catalog to resolve existing skills by their actual metadata. Open the resolved SKILL.md only when that capability is needed. Prefer the existing copy when the same skill appears more than once. If an optional skill is absent, state that and use the applicable Parnian guidance.

| Task | Complementary skills |
| --- | --- |
| Blazor, ASP.NET Core, SPFx or SharePoint reports | Use the relevant PM skill for requirements and acceptance criteria, UI UX Pro Max for report UX, and an available SQL Server or data analysis skill for schema, query plans, and reconciliation. |
| Power BI model, DAX or M | Use `semantic-model-authoring` for model design, DAX and model performance. For M, select an available Power Query skill when applicable or follow the transformation and folding guidance in [Power BI](power-bi.md). |
| Power BI report pages | Use `powerbi-report-cli` for design and supported local PBIR/PBIP authoring. Select PM/UX or visualization support when needed. |
| Power BI audit | Use `powerbi-audit` if already available and the scope permits its local audit files. Otherwise use the validation checklist and, for model analysis, the relevant semantic model references. |
| PDF or print | Use the existing PDF skill for layout, generation, and rendering checks. |
| Excel or CSV | Use the existing spreadsheet skill for workbook construction, analysis, formulas, and validation. |
| Exploratory charts or statistical analysis | Select visualization or data analysis support if available. Confirm denominators, sampling, missingness, and uncertainty before drawing conclusions. |

Select UI UX Pro Max and PM skills by confirmed scope and availability. Their existing locations and versions vary by environment. For Linux or Windows without the cloud visualization tool, use an available local charting skill or the project's current plotting stack.

Confirm deployment compatibility before applying an upstream workflow. Apply the Parnian approval, read-only discovery, and cloud consent rules before any upstream command. Tool dependencies are conditional on the chosen workflow.
