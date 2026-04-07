import subprocess
import re


def parse_output(output: str):
    lines = output.strip().splitlines()

    start_found = False
    steps = []
    score = None
    total_steps = None

    for line in lines:
        line = line.strip()

        # START
        if line.startswith("[START]"):
            start_found = True

        # STEP
        elif line.startswith("[STEP]"):
            step_match = re.search(r"step=(\d+)\s+reward=([0-9.]+)", line)
            if step_match:
                steps.append({
                    "step": int(step_match.group(1)),
                    "reward": float(step_match.group(2))
                })

        # END
        elif line.startswith("[END]"):
            end_match = re.search(r"score=([0-9.]+)\s+steps=(\d+)", line)
            if end_match:
                score = float(end_match.group(1))
                total_steps = int(end_match.group(2))

    # VALIDATION
    if not start_found or score is None or total_steps is None:
        return None

    return {
        "score": score,
        "steps": total_steps,
        "step_details": steps
    }


def run_once():
    result = subprocess.run(
        ["python", "inference.py"],
        capture_output=True,
        text=True
    )

    output = result.stdout

    parsed = parse_output(output)

    if parsed:
        return parsed["score"], parsed["steps"], output
    else:
        return None, None, output


def run_simulation(n=5):
    scores = []
    steps_list = []

    print("Running Simulation...\n")

    for i in range(n):
        print(f"Run {i+1}:")

        score, steps, output = run_once()

        if score is None:
            print("❌ Failed to parse output")
            print(output)
        else:
            print(f"Score: {score}, Steps: {steps}")
            scores.append(score)
            steps_list.append(steps)

        print("-" * 40)

    if scores:
        print("\n📊 Summary:")
        print(f"Average Score: {sum(scores)/len(scores):.2f}")
        print(f"Min Score: {min(scores)}")
        print(f"Max Score: {max(scores)}")
        print(f"All Scores: {scores}")

        if min(scores) >= 2.5:
            print("\n✅ Stable performance — Ready to submit")
        else:
            print("\n⚠️ Performance unstable — Review logic")


if __name__ == "__main__":
    run_simulation()