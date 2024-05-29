set -e

echo "Starting tests..."

# Get the list of files modified in PR
changed_files=$(cat /tmp/changed_files.txt)

# Define directories and files that require full testing
declare -a full_test_triggers=("app/" ".github/" "test/" "bundle_dependency/" "requirements.txt" "Dockerfile" "config.py")

run_full_tests=false
declare -A modified_bundles

# Check whether the modified file triggers full testing
for file in $changed_files; do
    for trigger in "${full_test_triggers[@]}"; do
        if [[ "$file" == "$trigger"* ]]; then
            run_full_tests=true
            break 2
        fi
    done

    # Collect the bundles directory names involved in the modification
    if [[ "$file" =~ ^bundles/([^/]+)/ ]]; then
        modified_bundles[${BASH_REMATCH[1]}]=1
    fi
done

if $run_full_tests; then
    echo "Running full tests..."
    pytest -n auto -q -k "test_plugins"
else
    set +e
    # For each bundle directory involved in the modification, execute a test
    for bundle_name in "${!modified_bundles[@]}"; do
        echo "Running tests for bundle: $bundle_name"
        pytest -n auto -q -k "$bundle_name"
        exit_code=$?

        if [ $exit_code -eq 5 ]; then
            echo "No tests found for $provider_name, skipping..."
        elif [ $exit_code -ne 0 ]; then
            echo "Error running tests for $provider_name"
            exit $exit_code
        fi
    done
fi



echo "Tests completed."
