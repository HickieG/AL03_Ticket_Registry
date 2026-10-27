# AL 02 Shared README

$ Monday Tasks $
1. Create the fresh shared AL03 project and import TICKETS and SUPPORTED_CATEGORIES. Inspect the six records together before building.
2. Implement build_registry, copying each flat record. Check that a separate duplicate-ID example is rejected rather than replacing an earlier ticket. Do not add a duplicate to the supplied TICKETS itself.
3. Implement list-scan and indexed lookup. Show the same found ticket through both approaches and a clear missing-ticket message. Compare before updates: the supplied list intentionally does not follow later registry changes.
4. Implement update_priority. For example, change T301 from normal to high. Show the updated ticket and check that the supplied record is unchanged. A missing ID must not create a ticket.
5. Use the supported-category set to check a category, then implement and show filter_by_category. For example, account selects T301 and T304 in the starting registry; classroom is supported but currently has no tickets. An unsupported category such as parking should receive a clear message.
6. Check found/missing lookup, empty input, duplicate IDs, priority updates, category selection, and independent copies. Save a filtered selection now so that you can revisit its independence on Thursday.
7. Begin the README’s three-row lookup/update/filter comparison. Explain which representation fits each operation and why; do not build six parallel implementations or memorize an exhaustive cost table. Commit the baseline.

 Stop here on Monday. Queues, processing, undo, and cancellation come after their instruction. Use display_tickets to show lookup/category results; no state summary is needed until Tuesday.

$ Tuesday Tasks $ 
1. Continue the same project. Add the state dictionary, an empty pending deque, and an empty undo list. Keep the registry as the single live ticket store.

2. Implement enqueue_ticket. Queue T301 and then T302. Reject a repeated T301, unknown T999, and already-completed T306 without changing any state.

3. Implement process_next. Process those two requests, one at a time. The results must be T301 and then T302, regardless of their priority labels. Record only successful processing actions in undo history.

4. Implement undo_process. Undo once: T302 becomes open and returns to the front of pending; T301 remains completed. The T302 history entry is removed. Show enough information to make the processing/restoration understandable.

5. Check empty queue/history behavior, rejected requests, two processing actions, and successive undo behavior. Also change a processed ticket’s priority before undoing it: undo must restore status without erasing that priority edit.

6. Add one brief README observation about the process/process/undo sequence. Run the earlier Monday checks again and commit progress. No trace essay or separate evidence document is required.

 Your ticket-enqueue rule is stricter than the equipment demo: reject completed tickets before they enter pending. Do not copy the demo’s unavailable-item request behavior into this application.