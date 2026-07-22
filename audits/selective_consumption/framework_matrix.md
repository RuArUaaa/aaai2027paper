# Selective-Consumption Framework Matrix

Date: 2026-07-22

Protocol: `audits/selective_consumption/protocol.md` at `74f9c1407735121837becb91169adddd4f94c16f`

Evidence: `raw_locators.json` and uninterpreted `results.json`

`null` counts below mean that no qualifying public runtime instance exists. They
must not be replaced by counts inferred from source topology or test code.

| Required field | Microsoft AutoGen | LangGraph | SWE-agent RetryAgent |
|---|---|---|---|
| 1. Framework/repository | `microsoft/autogen` | `langchain-ai/langgraph` | `SWE-agent/SWE-agent` |
| 2. Pinned commit | `027ecf0a379bcc1d09956d46d12d44a3ad9cee14` | `31f90df3e6b0268fa77fd2d118a917d420b84a68` | `3ea751c087f32b16e039a2233dd6eefecef325d5` |
| 3. Publication/project source | Pinned project repository and Core runtime | Pinned project repository and Graph/Pregel runtime | Pinned project repository and RetryAgent implementation |
| 4. Public trace/event source | Handoff history JSON plus runtime test source; neither is a delivery trace | Debug/map-reduce test expectations; neither is an archived run trace | 22 tracked `.traj` files; none is a RetryAgent/Reviewer/Chooser trace |
| 5. Producer artifact | `UserTask(context)` publish envelope | Checkpointed graph state and/or `Send(node,arg)` | One completed-attempt `ReviewSubmission` |
| 6. Stable artifact identity | Runtime UUID `message_id`; absent from public artifacts | Checkpoint/task identity exists; `Send` has no parent artifact ID and public fixtures replace task IDs | Problem ID + positional attempt index; no independent artifact UUID and no public RetryAgent instance |
| 7. Producer node | FastAPI chat endpoint or active handoff agent | StateGraph node/conditional branch | `RetryAgent.run` after attempt completion |
| 8. Downstream consumers | Triage, Sales, Issues/Repairs agent handlers | PUSH/PULL Pregel tasks; prebuilt ToolNode path | One configured Score Reviewer **or** a Chooser path; the native optional Preselector can consume submissions before a Chooser, although it is disabled in the shipped config |
| 9. Actual complete consumer input | Selected handler receives complete `UserTask`; its complete context enters the model call | PUSH gets `packet.arg`; PULL gets declared channels; prebuilt v2 ToolNode gets/hydrates full state | Reviewer prompt gets flattened info + text-formatted trajectory; Chooser prompt gets rendered info without trajectory |
| 10. Typed projection | No; topic routing is non-delivery | Framework supports custom `Send.arg` and PULL channel projection, but no qualifying same-parent/two-consumer instance survives the bypass and trace requirements | No; configurable Jinja/text prompt rendering is not a typed record projection |
| 11. Field/read access log | No | No; `versions_seen` is trigger bookkeeping | No |
| 12. Raw artifact bypass | `ABSENT` for nonmatching application agents; matching consumer receives raw input as primary delivery | `PRESENT_UNMODELLED`: every task config receives shared-channel `CONFIG_KEY_READ`; prebuilt ToolNode exposes/hydrates full state | `PRESENT_MODELLED`: controller retains full submissions/attempts, while audited model consumers have no native raw-artifact read route; no access log exists |
| 13. Load-bearing source locators | `_single_threaded_agent_runtime.py:57-67,387-428,557-609`; `logging.py:202-234`; sample `app.py:73-158`; `agent_base.py:47-54,82-104` | `types.py:664-752`; `_algo.py:188-224,961-1105`; `_read.py:25-91`; `debug.py:41-206`; `test_large_cases.py:3939-4168` | `agents.py:290-318,351-388,413-426`; `reviewer.py:30-56,180-237,242-449,499-658`; `250212_sweagent_heavy_sbl.yaml:6-7,135-188` |
| 14. Minimum public instance | Handoff history has 6 records but no envelope/message/recipient binding | Test source declares two full-state task inputs using `AnyStr()` IDs | Five-step DefaultAgent negative-control `.traj`; RetryAgent keys absent |
| 15. Repeated-consumer count | `null` | `null` | `null` |
| 16. Producer-artifact count | `null` | `null` | `null` |
| 17. Consumer-edge count | `null` | `null` | `null` |
| 18. Q level | **Q1** — native topic non-delivery | **Q0** — the concrete two-consumer fixture broadcasts identical full state; a single `Send` destination does not prove another real downstream consumer was denied that artifact | **Q1** — optional native Preselector consumes eligible submissions and the Chooser receives only its selected subset |
| 19. Evidence level | **CODE_ONLY_CANDIDATE** | **CODE_ONLY_CANDIDATE** | **CODE_ONLY_CANDIDATE** |
| 20. From-scratch/outcome oracle | From-scratch run possible; no native deterministic sample oracle | From-scratch thread possible; correctness is application-defined | SWE-bench outcome possible in principle; no matching RetryAgent trace/label |
| 21. Formal integration modification | Q1 telemetry capture needs no core modification but needs a new model run; Q2/Q3 would need changes | Strong qualification requires raw-read restriction/instrumentation and a qualifying trace | Native Preselector needs no framework-code modification, but trace confirmation requires a configuration change and new model-backed RetryAgent run |
| 22. Coarse integration cost | `MEDIUM` | `HIGH` | `HIGH` |
| 23. C6 relationship | Weak selective routing is possible; no receiver-conditioned or query-relative contract | Concrete public source evidence shows full-state fan-out; custom-state potential, unlogged bypass, and no qualifying trace prevent strong-testbed use | Optional record-level non-delivery supports only a weak code-level routing direction; no trace or typed projection |
| 24. C3 relationship | Delivery telemetry cannot attribute reuse damage | Task/checkpoint/error records cannot attribute reuse damage | LLM score/choice observes overall solution quality, not a reuse intervention; it is not a causal runtime certificate |
| 25. Main limits/gaps | No public OTEL process export; `MessageEvent` omits `message_id` and publish receiver | No concrete task-ID trace; no parent-to-projection link; raw shared-state reads unlogged; no frozen real nonrecipient consumer for a Q1 claim | No public RetryAgent trace; Preselector disabled in shipped config; text rendering; no read log |

## Decision-rule summary

| Test | AutoGen | LangGraph | SWE-agent |
|---|---:|---:|---:|
| At least Q2 | No | No | No |
| `TRACE_CONFIRMED` | No | No | No |
| Stable producer identity observed in public instance | No | No | No |
| Two real consumers independently reconstructable from public instance | No | No | No |
| No unmodelled raw bypass | Yes for Q1 route | No | Controller retention is described, but no public consumer-access trace exists; strong qualification already fails Q/evidence |
| Outcome oracle possible in principle | No native sample oracle | Yes, application-defined | Yes, SWE-bench-defined |
| Strong C6 testbed qualified | **No** | **No** | **No** |
| C3 directed verifier candidate | **No** | **No** | **No** |

The matrix supports `SELECTIVE_ROUTING_DIRECTION = POSSIBLE` through AutoGen's
topic route and SWE-agent's optional Preselector route at Q1/code-only. It does not support receiver-conditioned validity,
query-relative artifact reuse, Q2/Q3 measurement, or formal experiment launch.
