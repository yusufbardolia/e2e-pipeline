import os
import re
import yaml

INPUT_DIR = 'tests/bug_reports'
OUTPUT_DIR = 'tests/generated_flows'

def extract_and_convert():
    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(INPUT_DIR, filename)

            # Read the bug report
            with open(filepath, 'r') as file:
                content = file.read()

            # Regex: Find everything between [YAML_START] and [YAML_END]
            match = re.search(r'\[YAML_START\](.*?)\[YAML_END\]', content, re.DOTALL)

            if match:
                yaml_content = match.group(1).strip()

                try:
                    # Validate that the extracted text is proper YAML
                    parsed_yaml = yaml.safe_load(yaml_content)

                    # Create the output filename
                    test_filename = f"{os.path.splitext(filename)[0]}_flow.yaml"
                    output_path = os.path.join(OUTPUT_DIR, test_filename)

                    # Write the executable Maestro flow
                    with open(output_path, 'w') as out_file:
                        yaml.dump(parsed_yaml, out_file, default_flow_style=False, sort_keys=False)

                    print(f"✅ Successfully generated test flow at: {output_path}")

                except yaml.YAMLError as exc:
                    print(f"❌ Error parsing YAML in {filename}: {exc}")
            else:
                print(f"⚠️ No YAML markers found in {filename}")

if __name__ == "__main__":
    extract_and_convert()