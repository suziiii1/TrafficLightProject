from z3 import *

class TrafficLight:
    def __init__(self):
        # Initial state
        self.state = "Red"

    def next_state(self):
        # Transition logic
        if self.state == "Red":
            self.state = "Green"
        elif self.state == "Green":
            self.state = "Yellow"
        elif self.state == "Yellow":
            self.state = "Red"
        else:
            raise ValueError("Invalid state")

    def get_state(self):
        return self.state


# Z3 Formal Verification

def verify_traffic_light():
    # Declare state variables (each light is either on or off)
    red = Bool('red')
    green = Bool('green')
    yellow = Bool('yellow')

    # Create a solver
    solver = Solver()

    # Add constraints to ensure only one state is active at a time
    solver.add(And(
        # Only one light can be on at a time
        Or(red, green, yellow),  # At least one light should be on
        Not(And(red, green)),    # Red and Green can't be on together
        Not(And(green, yellow)), # Green and Yellow can't be on together
        Not(And(yellow, red)),   # Yellow and Red can't be on at the same time

        # Simple model to make sure Z3 solver can find a valid state for transitions
        # Red -> Green -> Yellow -> Red
        Or(And(red, Not(green), Not(yellow)),   # Red only
           And(green, Not(red), Not(yellow)),   # Green only
           And(yellow, Not(red), Not(green))),  # Yellow only
    ))

    # Check satisfiability of the model
    if solver.check() == sat:
        print("Traffic light model is valid!")
        model = solver.model()
        print(f"Red: {model[red]}, Green: {model[green]}, Yellow: {model[yellow]}")
    else:
        print("Traffic light model is not valid!")

# Unit Testing
def test_traffic_light():
    light = TrafficLight()

    # Test initial state
    assert light.get_state() == "Red", "Initial state should be Red"
    print("Test 1 Passed: Initial state is Red.")

    # Test transitions
    light.next_state()
    assert light.get_state() == "Green", "After Red, state should be Green"
    print("Test 2 Passed: State after Red is Green.")

    light.next_state()
    assert light.get_state() == "Yellow", "After Green, state should be Yellow"
    print("Test 3 Passed: State after Green is Yellow.")

    light.next_state()
    assert light.get_state() == "Red", "After Yellow, state should return to Red"
    print("Test 4 Passed: State after Yellow is Red.")

    print("\nAll tests passed!")


if __name__ == "__main__":
    # Main program to demonstrate transitions
    print("Traffic Light State Transitions:")
    light = TrafficLight()
    for _ in range(6):  # Cycle through states twice
        print(f"Current State: {light.get_state()}")
        light.next_state()

    # Run unit tests
    test_traffic_light()

    # Perform Z3 formal verification
    print("\nRunning Z3 Formal Verification:")
    verify_traffic_light()


