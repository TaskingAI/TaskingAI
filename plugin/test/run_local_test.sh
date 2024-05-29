set -e
parent_dir="$(dirname "$(pwd)")"
export PYTHONPATH="${PYTHONPATH}:${parent_dir}"

echo "Starting tests..."

pytest  -q  --tb=no -k "test_generate_image_local"

echo "Tests completed."

