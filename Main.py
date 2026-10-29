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
    ticketsdict = {}
    for record in records:
        ticket_id = record.get("id")
        if ticket_id in ticketsdict:
            raise ValueError("Duplicate ticket ID: " + ticket_id)
        ticketsdict[ticket_id] = record.copy()
    return ticketsdict


def scan_lookup(records, ticket_id):
    """Return the first matching ticket, or None when absent."""
    for record in records:
        if record.get("id") == ticket_id:
            return record
    return None


def indexed_lookup(registry, ticket_id):
    """Return the matching live ticket, or None when absent."""
    return registry.get(ticket_id)


def update_priority(registry, ticket_id, priority):
    """Update one existing ticket's priority and report whether it was found."""
    ticket = registry.get(ticket_id)
    if not ticket:
        return False
    ticket["priority"] = priority
    return True


def filter_by_category(registry, category):
    """Return independent copies of tickets matching the selected category."""
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

def stale_ids(registry, pending):
    missing = []
    for ticket_id in pending:
        if ticket_id not in registry:
            missing.append(ticket_id)
    return missing

def repair_queue(registry, pending):
    """Return a new queue of known IDs and a list of removed missing IDs."""
    new_queue = deque()
    removed = []
    for ticket_id in pending:
        if ticket_id in registry:
            new_queue.append(ticket_id)
        else:
            removed.append(ticket_id)
    return new_queue, removed



def cancel_ticket(state, ticket_id):
    """Remove an open ticket and any waiting request, leaving history unchanged."""
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
    display_state("After undoing T302", state)
    print("T301 status remains:", state["registry"]["T301"]["status"])
    print("T302 priority remains:", state["registry"]["T302"]["priority"])

    print("Undo earlier process:", undo_process(state))
    print("Undo with empty history:", undo_process(state))
    print("Process restored queue item:", process_next(state))
    print("Process restored queue item:", process_next(state))
    print("Process with empty queue:", process_next(state))
    
    # THURSDAY: demonstrate stale-queue repair and ticket cancellation
    print("\n Thursday Assignment - Stale Queue Repair")
    new_queue, removed = repair_queue(state["registry"], state["pending"])
    state["pending"] = new_queue
    print("Repair stale queue:", new_queue)
    print("Removed from stale queue:", removed)

if __name__ == "__main__":
    main()
