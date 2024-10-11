import argparse
import json
import os
import re
import subprocess

plugins_json_path = "plugins.json"


def commit_update_changes(plugin_name, new_version):
    subprocess.run(["git", "add", "."])
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            f":tada: chore({plugin_name}): Update version to {new_version}",
        ]
    )


def get_changed_files(commit_hash: str = "HEAD"):
    # 获取当前分支与主分支的差异文件列表
    changed_files = (
        subprocess.check_output(
            ["git", "diff-tree", "--name-only", "--no-commit-id", "-r", commit_hash]
        )
        .decode()
        .split()
    )
    return changed_files


def update_version_in_init(file_path, current_version, commit_hash):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    new_version = f"{current_version}-{commit_hash}"
    if old_version_match := re.search(r'version\s*=\s*"(.*?)"', content):
        old_version = old_version_match[1]
        old_version = old_version.split("-")[0]
        if old_version != current_version:
            return old_version

        new_content = re.sub(
            r'version\s*=\s*"(.*?)"', f'version="{new_version}"', content
        )

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(new_content)

        return new_version
    return current_version


def process_plugins(commit_hash: str, plugins: dict, changed_files: list):
    commit_hash = commit_hash[:7]

    for plugin_name, plugin_info in plugins.items():
        module_path = plugin_info["module_path"].replace(".", "/")
        is_dir = plugin_info["is_dir"]
        current_version = plugin_info["version"]
        current_version = current_version.split("-")[0]

        if is_dir:
            for changed_file in changed_files:
                if changed_file.startswith(module_path):
                    init_path = os.path.join(module_path, "__init__.py")
                    if os.path.exists(init_path):
                        new_version = update_version_in_init(
                            init_path, current_version, commit_hash
                        )
                        plugin_info["version"] = new_version
        else:
            file_path = f"{module_path}.py"
            if file_path in changed_files:
                new_version = update_version_in_init(
                    file_path, current_version, commit_hash
                )
                plugin_info["version"] = new_version
        if plugin_info["version"] != current_version:
            save_plugins_json(plugins)
            commit_update_changes(plugin_name, plugin_info["version"])


def save_plugins_json(plugins: dict):
    with open(plugins_json_path, "w", encoding="utf-8") as file:
        json.dump(plugins, file, indent=4, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser()
    parser.description = "Update version in plugins.json"
    parser.add_argument(
        "-c",
        "--commit_hash",
        help="The commit hash to get the changed files from. Defaults to HEAD.",
        dest="commit_hash",
        type=str,
        default="HEAD",
    )
    args = parser.parse_args()
    with open(plugins_json_path, "r", encoding="utf-8") as file:
        plugins = json.load(file)

    changed_files = get_changed_files(args.commit_hash)
    process_plugins(args.commit_hash, plugins, changed_files)


if __name__ == "__main__":
    main()
