export TEST_MODE=TASKINGAI_API_TEST

set -e
parent_dir="$(dirname "$(pwd)")"
export PYTHONPATH="${PYTHONPATH}:${parent_dir}"

echo "Starting tests..."
pytest   ./tests/services_tests  ./tests/client_tests  -m "api_test"  -q  --tb=no  --reruns 3 --reruns-delay 2
echo "Tests completed."