import subprocess

def main():
    print("=== Industrial Scale Data Poisoning CLI ===")

    poisons = {
        "1": "gradient-matching",
        "2": "poison-frogs",
        "3": "bullseye",
        "4": "metapoison",
        "5": "hidden-trigger",
        "6": "convex-polytope",
        "7": "patch",
        "8": "watermark"
    }

    defenses = {
        "1": ("--filter_defense", "spectral_signatures"),
        "2": ("--filter_defense", "deepknn"),
        "3": ("--filter_defense", "activation_clustering"),
        "4": ("--mixing_method", "Mixup"),
        "5": ("--gradient_noise", "1", "--gradient_clip", "1"),
        "6": ("--optimization", "defensive", "--defense_type", "adversarial-wb-recombine"),
        "7": None  # No defense
    }

    print("\nSelect a poisoning recipe:")
    for k, v in poisons.items():
        print(f"{k}. {v.replace('-', ' ').title()}")

    poison_choice = input("Enter choice (1-8): ").strip()
    poison = poisons.get(poison_choice)

    if not poison:
        print("❌ Invalid poison choice.")
        return

    print("\nSelect a defense technique:")
    for k, v in defenses.items():
        label = "None" if v is None else v[1].replace('-', ' ').title() if "filter_defense" in v else v[-1].replace('-', ' ').title()
        print(f"{k}. {label}")

    defense_choice = input("Enter choice (1-7): ").strip()
    defense_args = defenses.get(defense_choice)

    if defense_choice not in defenses:
        print("❌ Invalid defense choice.")
        return

    # Construct base command
    cmd = [
        "python", "brew_poison.py",
        "--net", "ResNet18",
        "--dataset", "CIFAR10",
        "--recipe", poison,
        "--restarts", "1"
    ]

    if defense_args:
        cmd.extend(defense_args)

    print("\n🚀 Running command:")
    print(" ".join(cmd))
    print()

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Command failed with exit code {e.returncode}")
    except FileNotFoundError:
        print("\n❌ Python script not found. Make sure 'brew_poison.py' is in the same directory.")

if __name__ == "__main__":
    main()
