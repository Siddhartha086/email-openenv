import subprocess
import re

NUM_RUNS = 5

scores = []
steps_list = []

pattern = r"\[END\].*score=([0-9.]+).*steps=([0-9]+)"


def run_once():
    result = subprocess.run(
        ["python", "inference.py"],
        capture_output=True,
        text=True
    )

    output = result.stdout

    match = re.search(pattern, output)

    if match:
        score = float(match.group(1))
        steps = int(match.group(2))
        return score, steps, output
    else:
        return None, None, output


def main():
    print("🔍 Running Simulation...\n")

    for i in range(NUM_RUNS):
        score, steps, output = run_once()

        print(f"Run {i+1}:")

        if score is not None:
            print(f"  Score: {score}, Steps: {steps}")
            scores.append(score)
            steps_list.append(steps)
        else:
            print("  ❌ Failed to parse output")
            print(output)

        print("-" * 40)

    if scores:
        print("\n📊 Summary:")
        print(f"Average Score: {sum(scores)/len(scores):.2f}")
        print(f"Min Score: {min(scores)}")
        print(f"Max Score: {max(scores)}")
        print(f"All Scores: {scores}")

        if min(scores) < 2.0:
            print("\n⚠️ WARNING: Some runs have low scores")
        else:
            print("\n✅ Stable performance — Ready to submit")


if __name__ == "__main__":
    main()