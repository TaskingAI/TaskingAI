set -e

echo "Starting tests..."

pytest -n auto -q

echo "Tests completed."
