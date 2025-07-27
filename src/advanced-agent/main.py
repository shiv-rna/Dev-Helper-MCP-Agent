import io
import sys
import json
from dotenv import load_dotenv
from datetime import datetime
from src.workflow import Workflow

load_dotenv()

def save_output_to_file(content: str, extension="txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"developer_tools_output_{timestamp}.{extension}"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n📝 Output saved to {filename}")

def main():
    workflow = Workflow()
    print("🐧 Developer Tools Agent 🐧")

    while True:
        query = input("\n✒️  Developer Tools Query: ").strip()
        if query.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        if query:
            buffer = io.StringIO()
            sys.stdout = buffer  # Redirect stdout

            result = workflow.run(query)
            print(f"\n📊 Results for : {query}")
            print("=" * 60)

            for i, company in enumerate(result.companies, start=1):
                print(f"\n{i}. 🏢 {company.name}")
                print(f"   🌐 Website: {company.website}")
                print(f"   💰 Pricing: {company.pricing_model}")
                print(f"   📖 Open Source: {company.is_open_source}")

                if company.tech_stack:
                    print(f"   🛠️  Tech Stack: {', '.join(company.tech_stack[:5])}")

                if company.language_support:
                    print(
                        f"   💻 Language Support: {', '.join(company.language_support[:5])}"
                    )

                if company.api_available is not None:
                    api_status = (
                        "✅ Available" if company.api_available else "❌ Not Available"
                    )
                    print(f"   🔌 API: {api_status}")

                if company.integration_capabilities:
                    print(
                        f"   🔗 Integrations: {', '.join(company.integration_capabilities[:4])}"
                    )

                if company.description and company.description != "Analysis failed":
                    print(f"   📝 Description: {company.description}")

                print()

            if result.analysis:
                print(f"Developer Recommendations:")
                print("-" * 40)
                print(result.analysis)

            sys.stdout = sys.__stdout__  # Reset stdout
            output = buffer.getvalue()
            save_output_to_file(output)  # Save to file
            print(output)  # Also print to console

if __name__ == "__main__":
    main()
