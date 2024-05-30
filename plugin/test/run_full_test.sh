set -e

echo "Starting tests..."

pytest -n auto -q -k "test_plugins"

echo "Tests completed."
