"""Optional English-first starter; develop one ticket application across three days."""

from collections import deque

from TicketData import TICKETS, SUPPORTED_CATEGORIES
from Ticket_Display import display_state, display_tickets

# ======================================================================
# MONDAY - Find, update, and select
# Begin after Monday's instruction. Work in this same file all week.
# ======================================================================

def build_registry(records):
    """Return independent ticket records indexed by unique ID."""
    # Begin with an empty dictionary and visit each supplied record.
    # If its ID is already present, raise ValueError rather than overwrite it.
    # Otherwise, store a flat copy of the record under that ID.
    # Return the dictionary; leave the supplied records unchanged.
    ticket_registry = {}
    for record in records:
        ticket_id = record.get("id")
        if ticket_id in ticket_registry:
            raise ValueError("Duplicate ticket ID: " + ticket_id)
        ticket_registry[ticket_id] = record.copy()
    return ticket_registry


def scan_lookup(records, ticket_id):
    """Return the first matching ticket, or None when absent."""
    # Visit the records in order, comparing each ID with the requested ID.
    # Return the first match; return None if no record matches.
    for record in records:
        if record.get("id") == ticket_id:
            return record
    return None


def indexed_lookup(registry, ticket_id):
    """Return the matching live ticket, or None when absent."""
    # Check whether the requested ID is a key in the existing registry.
    # Return its record when present, or None when missing. Do not rebuild it.
    return registry.get(ticket_id)


def update_priority(registry, ticket_id, priority):
    """Update one existing ticket's priority and report whether it was found."""
    # First check whether the ticket exists; if missing, return False unchanged.
    # Change only its priority field, then return True.
    ticket = registry.get(ticket_id)
    if not ticket:
        return False
    ticket["priority"] = priority
    return True


def filter_by_category(registry, category):
    """Return independent copies of tickets matching the selected category."""
    # Start an empty result list and visit the live records in registry order.
    # For each matching category, append a flat record copy, not the live record.
    # Return the list; no matches means an empty list.
    result = []
    for ticket in registry.values():
        if ticket.get("category") == category:
            result.append(ticket.copy())
    return result


# ======================================================================
# TUESDAY - Process in order and undo one action
# Wait until Tuesday's instruction before beginning this stage.
# ======================================================================

def enqueue_ticket(state, ticket_id):
    """Queue a known open ticket once, returning whether it was accepted."""
    # Check that the ID exists, its ticket is open, and it is not already waiting.
    # If any check fails, return False without changing any part of state.
    # Otherwise, add the ID at the back of pending and return True.
    registry = state["registry"]
    pending = state["pending"]
    if ticket_id not in registry:
        return False
    if registry[ticket_id].get("status") != "open" or ticket_id in pending:
        return False
    pending.append(ticket_id)
    return True


def process_next(state):
    """Complete the oldest waiting ticket and remember its previous status."""
    # If pending is empty, return None without changing state.
    # Take the oldest ID from the front of pending and find its live ticket.
    # Append a history record with named ticket_id and previous_status fields.
    # Mark the ticket completed and return its ID.
    registry = state["registry"]
    pending = state["pending"]
    undo = state["undo"]
    if not pending:
        return None
    ticket_id = pending.popleft()
    ticket = registry[ticket_id]
    previous_status = ticket["status"]
    change = {
        "ticket_id": ticket_id,
        "previous_status": previous_status,
    }
    undo.append(change)
    ticket["status"] = "completed"
    return ticket_id


def undo_process(state):
    """Restore the latest processed ticket and return it to the queue front."""
    # If history is empty, return None without changing state.
    # Remove the newest history record and use its named fields to find the ticket.
    # Restore only its prior status; keep unrelated priority changes.
    # Return the ID to the front of pending, then return that ID to the caller.
    registry = state["registry"]
    pending = state["pending"]
    undo = state["undo"]
    if not undo:
        return None
    change = undo.pop()
    ticket_id = change["ticket_id"]
    registry[ticket_id]["status"] = change["previous_status"]
    pending.appendleft(ticket_id)
    return ticket_id


# ======================================================================
# THURSDAY - Cancel consistently and preserve snapshots
# Wait until Thursday's instruction before beginning this stage.
# ======================================================================

def repair_queue(registry, pending):
    """Return a new queue of known IDs and a list of removed missing IDs."""
    # Prepare a new empty deque and a list for removed IDs.
    # Visit pending in order: keep known IDs in the new queue, collect missing IDs.
    # Return both collections without changing registry or the original pending.
    # The owning application must install the returned queue into its state.
    repaired_queue = deque()
    removed = []
    for ticket_id in pending:
        if ticket_id in registry:
            repaired_queue.append(ticket_id)
        else:
            removed.append(ticket_id)
    return repaired_queue, removed


def cancel_ticket(state, ticket_id):
    """Remove an open ticket and any waiting request, leaving history unchanged."""
    # Check existence and open status before making any changes.
    # Return False unchanged for a missing or completed ticket.
    # Remove the eligible ticket from the registry and remove its pending reference.
    # You may reuse repair_queue, installing its returned queue into state.
    # Leave other requests in order and history unchanged; return True.
    if ticket_id not in state["registry"]:
        return False
    if state["registry"][ticket_id]["status"] != "open":
        return False
    del state["registry"][ticket_id]
    new_queue, _ = repair_queue(state["registry"], state["pending"])
    state["pending"] = new_queue
    return True


def main():
    """Show only the daily stages whose operations you have completed."""
    # MONDAY: build a fresh registry from TICKETS.
    # Compare scan/index answers before edits; display a found or missing result.
    # Update one priority. Check a category using SUPPORTED_CATEGORIES membership.
    # Select copied category records and show them using display_tickets.
    # Keep a selection to revisit later; do not call unfinished later-day functions.

    # TUESDAY: add a state dictionary with registry, pending deque, and undo list.
    # Queue two open IDs; process both in arrival order; undo the last processing.
    # Print the ticket status and waiting queue after each action.
    # Reject unknown, completed, and duplicate pending requests without changes.

    # THURSDAY: use a separate stale-queue example and install its repaired queue.
    # Demonstrate open-ticket cancellation and unchanged state for rejected actions.
    # Compare a saved selection with the tickets after an update and cancellation.
    # Run all tests, add brief personal README notes, and commit progress.
    # Each partner tests a full personal copy and submits their own repository URL.

    registry = build_registry(TICKETS)
    state = {
        "registry": registry,
        "pending": deque(),
        "undo": [],
    }

    print("\nTUESDAY - Queue, process, and undo")
    print("Queue T301:", enqueue_ticket(state, "T301"))
    print("Queue T302:", enqueue_ticket(state, "T302"))
    print("Reject duplicate T301:", enqueue_ticket(state, "T301"))
    print("Reject unknown T999:", enqueue_ticket(state, "T999"))
    print("Reject completed T306:", enqueue_ticket(state, "T306"))
    display_state("After queue requests", state)

    print("Process next:", process_next(state))
    print("Process next:", process_next(state))
    state["registry"]["T302"]["priority"] = "urgent"
    print("Updated T302 priority before undo:", state["registry"]["T302"]["priority"])
    display_state("After processing T301 and T302", state)

    print("Undo latest process:", undo_process(state))
    print("T301 status remains:", state["registry"]["T301"]["status"])
    print("T302 priority remains:", state["registry"]["T302"]["priority"])
    display_state("After undoing T302", state)

    print("Undo earlier process:", undo_process(state))
    print("Undo with empty history:", undo_process(state))
    print("Process restored queue item:", process_next(state))
    print("Process restored queue item:", process_next(state))
    print("Process with empty queue:", process_next(state))
    display_state("End of Tuesday", state)

    # THURSDAY: demonstrate stale-queue repair and ticket cancellation
    print("\nTHURSDAY - Stale queue repair and cancellation")
    thursday_state = {
        "registry": build_registry(TICKETS),
        "pending": deque(["T301", "T999", "T304", "T302"]),
        "undo": [],
    }
    saved_selection = filter_by_category(thursday_state["registry"], "account")
    stale_queue = deque(thursday_state["pending"])
    new_queue, removed = repair_queue(
        thursday_state["registry"], thursday_state["pending"]
    )
    thursday_state["pending"] = new_queue
    print("Repair stale queue:", list(thursday_state["pending"]))
    print("Removed from stale queue:", removed)
    print("Original queue is unchanged:", stale_queue)

    update_priority(thursday_state["registry"], "T301", "urgent")
    print("Cancel open T304:", cancel_ticket(thursday_state, "T304"))

    before_rejections = {
        "registry": {},
        "pending": deque(thursday_state["pending"]),
        "undo": thursday_state["undo"].copy(),
    }
    for current_id in thursday_state["registry"]:
        before_rejections["registry"][current_id] = (
            thursday_state["registry"][current_id].copy()
        )

    print("Reject missing T999:", cancel_ticket(thursday_state, "T999"))
    print("Reject completed T306:", cancel_ticket(thursday_state, "T306"))
    print("Rejected cancellations leave state unchanged:",
        thursday_state == before_rejections)

    display_tickets("Saved account tickets (original copies)", saved_selection)
    display_state("Current tickets after update and cancellation", thursday_state)


if __name__ == "__main__":
    main()
