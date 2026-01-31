#!/usr/bin/env python3
"""
Example usage of CRUCIBLE for various startup concepts
"""

from crucible import CrucibleEvaluator, format_output


def evaluate_examples():
    """Run CRUCIBLE on several example startup concepts"""
    
    evaluator = CrucibleEvaluator()
    
    examples = [
        {
            "name": "SaaS Platform",
            "concept": (
                "B2B SaaS platform for project management with subscription model, "
                "targeting enterprise customers. Proven revenue of $50K MRR, "
                "automated workflows, and integration with existing tools."
            )
        },
        {
            "name": "Marketplace",
            "concept": (
                "Two-sided marketplace connecting independent consultants with "
                "mid-size companies. Building network effects through reputation "
                "system and integrated payments."
            )
        },
        {
            "name": "AI Product",
            "concept": (
                "AI-powered code review tool using machine learning to detect bugs "
                "and security vulnerabilities before deployment."
            )
        },
        {
            "name": "Consumer App",
            "concept": (
                "Free mobile app for meditation and mindfulness with ad-supported "
                "model and optional premium subscriptions."
            )
        },
        {
            "name": "Hardware + Software",
            "concept": (
                "IoT device for home energy monitoring with companion app, "
                "requiring hardware manufacturing and complex installation."
            )
        }
    ]
    
    for example in examples:
        print("\n" + "=" * 70)
        print(f"Example: {example['name']}")
        print("=" * 70)
        
        result = evaluator.evaluate(example['concept'])
        print(format_output(result))
        
        # Save individual results
        import json
        from dataclasses import asdict
        
        filename = f"example_{example['name'].lower().replace(' ', '_')}.json"
        with open(filename, 'w') as f:
            result_dict = asdict(result)
            result_dict['decision'] = result.decision.value
            json.dump(result_dict, f, indent=2)
        
        print(f"\n📄 Saved to: {filename}\n")
        
        input("Press Enter to continue to next example...")


if __name__ == "__main__":
    print("🔥 CRUCIBLE - Example Evaluations")
    print("=" * 70)
    print("\nThis script demonstrates CRUCIBLE evaluating 5 different")
    print("startup concepts across various categories.")
    print("\nPress Ctrl+C at any time to exit.\n")
    
    try:
        evaluate_examples()
    except KeyboardInterrupt:
        print("\n\nExiting...")
