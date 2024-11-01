set -e

echo "Starting tests..."

pytest -n auto -q -k "test_plugins" --reruns 2 --reruns-delay 3

echo "Tests completed."
