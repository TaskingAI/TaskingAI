set -e

echo "Starting tests..."

# Debug: Check if the file exists and print its content
if [ ! -f /tmp/changed_files.txt ]; then
    echo "/tmp/changed_files.txt does not exist!"
    exit 1
fi

echo "Contents of /tmp/changed_files.txt:"
cat /tmp/changed_files.txt

# Get the list of files modified in PR
changed_files=$(cat /tmp/changed_files.txt)

# Debug: print changed files
echo "Changed files:"
echo "$changed_files"

# Define directories and files that require full testing
declare -a full_test_triggers=("app/" ".github/" "test/" "bundle_dependency/" "requirements.txt" "Dockerfile" "config.py")

run_full_tests=false
declare -A modified_bundles

# Check whether the modified file triggers full testing
for file in $changed_files; do
    echo "Processing file: $file"  # Debugging line

    for trigger in "${full_test_triggers[@]}"; do
        if [[ "$file" == "$trigger"* ]]; then
            run_full_tests=true
            break 2
        fi
    done

    # Collect the bundles directory names involved in the modification
    if [[ "$file" =~ ^plugin/bundles/([^/]+)/ ]]; then
        modified_bundles[${BASH_REMATCH[1]}]=1
    fi
done

echo "Modified bundles: ${!modified_bundles[@]}"

if $run_full_tests; then
    echo "Running full tests..."
    pytest -n auto -q -k "test_plugins"
else
    set +e
    echo "Running tests for modified bundles..."
    # For each bundle directory involved in the modification, execute a test
    for bundle_name in "${!modified_bundles[@]}"; do
        echo "Running tests for bundle: $bundle_name"
        pytest -n auto -q -k "$bundle_name"
        exit_code=$?

        if [ $exit_code -eq 5 ]; then
            echo "No tests found for $bundle_name, skipping..."
        elif [ $exit_code -ne 0 ]; then
            echo "Error running tests for $bundle_name"
            exit $exit_code
        fi
    done
fi

echo "Tests completed."
