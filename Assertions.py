from Main import (
    deque,
    repair_queue,
    stale_ids,
)

def self_check():
    """Check stale-ticket detection and queue repair."""
    registry = {"T301": {}, "T302": {}}
    # Pending queue contains both valid and missing ticket IDs.
    
    pending = deque(["T301", "T999", "T302"])
    # Repair the queue and check the results.
    
    repaired, removed = repair_queue(registry, pending)
    # Check that the repaired queue contains only valid tickets and that the removed list contains missing tickets.
    
    assert list(repaired) == ["T301", "T302"]
    # Ensure that the original pending queue remains unchanged after repair.
    
    assert removed == ["T999"]
    # Check that the removed list contains the missing ticket ID.
    
    assert list(pending) == ["T301", "T999", "T302"]
    # Check that the original pending queue still contains the missing ticket ID.
    
    assert stale_ids(registry, pending) == ["T999"]
    # Check that stale_ids correctly identifies missing tickets in the original and repaired queues.
    
    assert stale_ids(registry, repaired) == []
    # Check that stale_ids returns an empty list for the repaired queue, indicating no missing tickets.

    all_missing = deque(["T999", "T998"])
    # Attempt to repair a queue when the registry is empty and all tickets are missing.
    
    empty, missing = repair_queue({}, all_missing)
    # Check that the repaired queue is empty and all tickets are reported as missing.
    
    assert list(empty) == []
    # Ensure that the original all_missing queue remains unchanged after repair.
    
    assert missing == ["T999", "T998"]
    # Check that repair_queue correctly handles a non-empty registry with a previously repaired queue.
    
    assert list(all_missing) == ["T999", "T998"]
    # Attempt to repair the previously repaired queue with the same registry.
    
    assert list(repair_queue(registry, repaired)[0]) == ["T301", "T302"]
    # Check that the repaired queue still contains only valid tickets after a second repair attempt.


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Run verification without Python optimization (-O).")
    self_check()
    print("Checks passed.")