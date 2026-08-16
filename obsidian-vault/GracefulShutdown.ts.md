---
source_file: "src/process-manager/GracefulShutdown.ts"
type: "code"
community: "Community 5"
location: "L1"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Community_5
---

# GracefulShutdown.ts

## Connections
- [[CloseableResource]] - `contains` [EXTRACTED]
- [[GracefulShutdownConfig]] - `contains` [EXTRACTED]
- [[IMPORTANT On Windows, we must kill all child processes before exiting]] - `rationale_for` [EXTRACTED]
- [[Logger]] - `imports` [EXTRACTED]
- [[ProcessManager.ts]] - `imports_from` [EXTRACTED]
- [[ShutdownableService]] - `contains` [EXTRACTED]
- [[arra-oracle-v3ref_http]] - `imports_from` [EXTRACTED]
- [[closeHttpServer()]] - `contains` [EXTRACTED]
- [[createShutdownHandler()]] - `contains` [EXTRACTED]
- [[forceKillProcess()]] - `imports` [EXTRACTED]
- [[getChildProcesses()]] - `imports` [EXTRACTED]
- [[logger.ts]] - `imports_from` [EXTRACTED]
- [[performGracefulShutdown()]] - `contains` [EXTRACTED]
- [[process-managerindex.ts]] - `re_exports` [EXTRACTED]
- [[removePidFile()]] - `imports` [EXTRACTED]
- [[waitForProcessesExit()]] - `imports` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/Community_5