#!/bin/bash

echo "--- Starting Pipeline Orchestration ---"

# Step 1: Run Python parsing script (using python3 for Mac)
echo "Extracting acceptance criteria and generating tests..."
python3 scripts/parse_criteria.py

# Step 2: Iterate through generated tests and execute them
echo "Executing E2E regression tests..."
TEST_DIR="tests/generated_flows"
FAILED_TESTS=0

for flow in "$TEST_DIR"/*.yaml; do
    if [ -f "$flow" ]; then
        echo "Preparing to run: $flow"
        
        # In production, this would be: maestro test "$flow"
        echo "[MOCK] Executing maestro test on: $(basename "$flow")"
        
        # Simulating a successful test run (Exit code 0)
        MOCK_EXIT_CODE=0
        
        if [ $MOCK_EXIT_CODE -ne 0 ]; then
            echo "❌ Test Failed: $flow"
            FAILED_TESTS=$((FAILED_TESTS+1))
        else
            echo "✅ Test Passed: $flow"
        fi
    fi
done

# Step 3: Report and determine pipeline success
if [ $FAILED_TESTS -gt 0 ]; then
    echo "Pipeline Failed: $FAILED_TESTS tests did not pass."
    exit 1 # Exit code 1 tells CI/CD pipelines (like GitHub Actions) to halt
else
    echo "Pipeline Succeeded: All tests passed."
    exit 0 # Exit code 0 tells CI/CD pipelines to proceed
fi
