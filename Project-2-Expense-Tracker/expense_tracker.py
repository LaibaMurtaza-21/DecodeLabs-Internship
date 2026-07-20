def track_expenses():
    # --- PHASE 1: INITIALIZATION (State / Memory) ---
    # 'total' must live OUTSIDE the loop, or it would reset to 0
    # every single iteration (the "Amnesia" trap from the slides).
    total = 0.0
    transaction_count = 0

    print("=" * 45)
    print("        DECODELABS EXPENSE TRACKER")
    print("=" * 45)
    print("Enter an expense amount and press Enter.")
    print("Type 'quit' at any time to stop and see your total.\n")

    # --- PHASE 2: PROCESSING (The Engine) ---
    # The continuous audit loop.
    while True:
        user_input = input("Enter expense amount (or 'quit' to stop): ").strip()

        # --- Kill Switch: Sentinel Value Check ---
        if user_input.lower() == "quit":
            print("\nShutting down tracker... finalizing your report.")
            break

        # --- Defensive Coding: The Gatekeeper ---
        # Guard against non-numeric input crashing the program.
        try:
            expense = float(user_input)

            # Optional but sensible guard: reject negative expenses
            if expense < 0:
                print("⚠️  Invalid Data: Expense cannot be negative. Try again.\n")
                continue

        except ValueError:
            print("⚠️  Invalid Data: Please enter a numeric value.\n")
            continue

        # --- The Accumulator Pattern (Heartbeat of the Ledger) ---
        # State(new) = State(old) + Input
        total += expense
        transaction_count += 1
        print(f"✔ Added ${expense:.2f}  |  Running Total: ${total:.2f}\n")

    # --- PHASE 3: OUTPUT (Decoupled Display / Final Report) ---
    print("=" * 45)
    print(f"Transactions recorded : {transaction_count}")
    print(f"FINAL TOTAL SPENT     : ${total:.2f}")
    print("=" * 45)


if __name__ == "__main__":
    track_expenses()
