"""Optional English-first starter; develop one ticket application across three days."""

from collections import deque

from TicketData import TICKETS, SUPPORTED_CATEGORIES
from Ticket_Display import display_state, display_tickets



def build_registry(records):
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

    return registry.get(ticket_id)


def update_priority(registry, ticket_id, priority):

    ticket = registry.get(ticket_id)
    if not ticket:
        return False
    ticket["priority"] = priority
    return True


def filter_by_category(registry, category):

    result = []
    for ticket in registry.values():
        if ticket.get("category") == category:
            result.append(ticket.copy())
    return result



def enqueue_ticket(state, ticket_id):

    registry = state["registry"]
    pending = state["pending"]
    if ticket_id not in registry:
        return False
    if registry[ticket_id].get("status") != "open" or ticket_id in pending:
        return False
    pending.append(ticket_id)
    return True


def process_next(state):

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


def stale_ids(registry, pending):
    missing = []
    for ticket_id in pending:
        if ticket_id not in registry:
            missing.append(ticket_id)
    return missing

def repair_queue(registry, pending):
    new_queue = deque()
    repaired_queue = deque()
    removed = []
    for ticket_id in pending:
        if ticket_id in registry:
            new_queue.append(ticket_id)
            repaired_queue.append(ticket_id)
        else:
            removed.append(ticket_id)
    return new_queue, removed



def cancel_ticket(state, ticket_id):    
    if ticket_id not in state["registry"]:
        return False
    if state["registry"][ticket_id]["status"] != "open":
        return False
    del state["registry"][ticket_id]
    new_queue, _ = repair_queue(state["registry"], state["pending"])
    state["pending"] = new_queue
    return True


def main():
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
    display_state("After undoing T302", state)

    print("Undo earlier process:", undo_process(state))
    print("Undo with empty history:", undo_process(state))
    print("Process restored queue item:", process_next(state))
    print("Process restored queue item:", process_next(state))
    print("Process with empty queue:", process_next(state))
    
    display_state("End of Tuesday", state)

    # THURSDAY: demonstrate stale-queue repair and ticket cancellation
    print("\n Thursday Assignment - Stale Queue Repair")
    new_queue, removed = repair_queue(state["registry"], state["pending"])
    state["pending"] = new_queue
    print("Repair stale queue:", new_queue)
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