set -e

echo "Starting tests..."

pytest -n auto -v --reruns 3 --reruns-delay 2 test/

echo "Tests completed."
