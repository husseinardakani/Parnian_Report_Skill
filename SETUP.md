# Setup audit and validation

The initial Cloud workspace audit found PDF, spreadsheets, documents, and presentations under the Codex built-in skills directory, plus a cloud visualization skill. The runtime also ships internal or plugin copies of the built-ins. UI UX Pro Max and PM Skills were absent from the inspected scopes. The routing rules preserve and use those skills when available elsewhere. The target repository initially held only its MIT license.

| Source | Reviewed capabilities and decision |
| --- | --- |
| Microsoft Fabric skills | Install the pinned MIT semantic model and report authoring skills with their shared references. The model skill covers DAX and model optimization. The report skill covers planning, design, PBIR/PBIP authoring and Fabric management. The upstream has overlapping plugin and root layouts. Use only the pinned root copies. Skip unrelated Fabric CLI skills, plugins, services and retired bundles. |
| Power BI community skills | The pinned tree contains local Power BI guidance and a PBIP/TMDL audit skill that writes tracking Markdown. No license was located at the reviewed revision. Defer installation and reuse a pre-existing authorized copy where available. |
| Anthropic skills | The pinned PDF and XLSX folders include Apache-2.0 license files. Existing Codex skills cover the same tasks in this environment. Skip installation. |
| Microsoft Power BI Modeling MCP | Evaluate separately. The pinned MIT repository documents a local stdio server, Node.js for NPX, and an IDE extension path. It can query and modify models with the connected identity's privileges. Desktop access depends on the supported host and model connection. Fabric access depends on authenticated model and XMLA permissions. Metadata and data may enter client context and logs. For approved read-only discovery, review the documented `--readonly` option and limit access at the source. Hosted Fabric MCP is a separate cloud workflow. No MCP registration or runtime installation is included. |

All four reviewed main branches had November 2026 commits at audit time. Exact commit pins and requirements are in [dependencies.json](dependencies.json). The installer reads known directories from the pinned Git tree. It does not run upstream installers, register servers, or add credentials.

## Synthetic reporting example

Use four synthetic fact rows with one row per order. Three belong to the synthetic Jalali month 1404-01, including one restricted row. A fourth belongs to the following month. The visible month contains orders worth 100 and 50 for the restricted test identity. The expected filtered order count is 2 and sum is 150. An unmatched period represents missing data for the sum.

| Prompt | Expected routing and result |
| --- | --- |
| Plan a Blazor dashboard for this reporting month | Central skill plus available PM, UX and SQL support. Ask for the exact business grain when unspecified. Use the same server-side role and month constraints for aggregates and exports. |
| Model the same report for Power BI Report Server | Central plus semantic-model-authoring. Use order and date dimensions as appropriate to the confirmed grain, a one-to-many date relationship, explicit measures, and RLS. Verify the exact Report Server release before choosing a storage mode or project format. Add report authoring only if report pages are in scope. |
| Produce a Persian printable export for the same selection | Central plus PDF. Inspect embedded fonts, RTL shaping, Jalali month, repeating headers, page numbering, and totals. |
| Produce a filtered Excel export for the same selection | Central plus spreadsheets. Validate typed amounts, table filters, frozen headers, formula totals, and the two authorized detail rows. |

The guidance scenarios use synthetic rows and do not need a production connection. App-server discovery checks metadata and catalog availability. Model-driven implicit routing and rendering or deployment in the actual Power BI, Blazor, and VS Code clients require those environments.
