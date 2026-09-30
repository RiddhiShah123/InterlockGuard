from pathlib import Path

TEST_DATA = Path(__file__).resolve().parents[1] / "test_data"

def create_dummy_files(count=15):
    TEST_DATA.mkdir(exist_ok=True)
    for i in range(1, count + 1):
        (TEST_DATA / f"dummy_{i}.txt").write_text(
            "Harmless InterlockGuard demonstration file.\n", encoding="utf-8"
        )

def simulate_modifications(count=15):
    for p in list(TEST_DATA.glob("*.txt"))[:count]:
        p.write_text(p.read_text(encoding="utf-8") + "Simulated activity.\n",
                     encoding="utf-8")

def simulate_renames(count=5):
    for p in list(TEST_DATA.glob("*.txt"))[:count]:
        target = p.with_suffix(".test")
        if not target.exists():
            p.rename(target)

if __name__ == "__main__":
    print("INTERLOCKGUARD HARMLESS SIMULATOR")
    print("Only dummy files in test_data/ are used.")
    create_dummy_files()
    print("Created dummy files.")
    simulate_modifications()
    print("Modified dummy files.")
    simulate_renames()
    print("Renamed dummy files.")
    print("Simulation completed safely. No encryption was performed.")
