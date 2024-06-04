set -e

echo "Starting tests..."

# Get the list of files modified in PR
changed_files=$(cat /tmp/changed_files.txt)

changed_files=$(echo "$changed_files" | sed 's|inference/||')

# Debug: print changed files
echo "Changed files:"
echo "$changed_files"
# Define directories and files that require full testing
declare -a full_test_triggers=("app/" ".github/" "test/" "provider_dependency/" "requirements.txt" "Dockerfile" "config.py")

run_full_tests=false
declare -A modified_providers

# Check whether the modified file triggers full testing
for file in $changed_files; do
    for trigger in "${full_test_triggers[@]}"; do
        if [[ "$file" == "$trigger"* ]]; then
            run_full_tests=true
            break 2
        fi
    done

    # Collect the provider directory names involved in the modification
    if [[ "$file" =~ ^providers/([^/]+)/ ]]; then
        modified_providers[${BASH_REMATCH[1]}]=1
    fi
done

echo "Modified providers: ${!modified_providers[@]}"

if $run_full_tests; then
    echo "Running full tests..."
    pytest -n auto -v --reruns 2 --reruns-delay 1 test/
else
    set +e
    echo "Running tests for modified providers..."
    # For each provider directory involved in the modification, execute a test
    for provider_name in "${!modified_providers[@]}"; do
        echo "Running tests for provider: $provider_name"
        pytest -n auto -v -k "$provider_name" --reruns 3 --reruns-delay 2 test/
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
