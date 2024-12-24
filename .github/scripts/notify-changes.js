// .github/scripts/notify-changes.js

module.exports = async ({ github, context, core }) => {
  const fs = require("fs");
  const { execSync } = require("child_process");

  function patternToRegex(pattern) {
    pattern = pattern.replace(/^\//, "");
    pattern = pattern.replace(/[.+?^${}()|[\]\\]/g, "\\$&");
    pattern = pattern.replace(/\*/g, ".*");
    return new RegExp(`^${pattern}$`);
  }

  try {
    // 获取当前提交者
    const pusher = context.payload.pusher.name;
    console.log("Current pusher:", pusher);

    const changedFiles = execSync("git diff --name-only HEAD^ HEAD")
      .toString()
      .trim()
      .split("\n")
      .filter((file) => file.startsWith("backend/api/"));

    console.log("Changed files:", changedFiles);

    if (changedFiles.length === 0) {
      console.log("No relevant files changed");
      return;
    }

    // 获取每个文件的详细变更
    const fileDetails = changedFiles.map((file) => {
      try {
        const diff = execSync(`git diff HEAD^ HEAD -- "${file}"`)
          .toString()
          .trim();
        return {
          file,
          diff,
        };
      } catch (error) {
        console.error(`Error getting diff for ${file}:`, error);
        return {
          file,
          diff: "Error getting diff content",
        };
      }
    });

    const codeownersContent = fs.readFileSync(".github/CODEOWNERS", "utf8");
    console.log("CODEOWNERS content:", codeownersContent);

    const codeowners = codeownersContent
      .split("\n")
      .filter((line) => line && !line.startsWith("#"))
      .map((line) => {
        const [pattern, ...owners] = line.trim().split(/\s+/);
        return {
          pattern: pattern,
          regex: patternToRegex(pattern),
          owners: owners.map((o) => o.replace("@", "")),
        };
      });

    console.log("Parsed CODEOWNERS:", codeowners);

    const usersToNotify = new Set();
    changedFiles.forEach((file) => {
      codeowners.forEach(({ pattern, regex, owners }) => {
        console.log(`Checking if ${file} matches pattern ${pattern}`);
        if (regex.test(file)) {
          owners
            .filter((owner) => owner.toLowerCase() !== pusher.toLowerCase())
            .forEach((owner) => usersToNotify.add(owner));
          //   owners.forEach((owner) => usersToNotify.add(owner));
        }
      });
    });

    console.log("Users to notify:", Array.from(usersToNotify));

    if (usersToNotify.size === 0) {
      console.log("No users to notify");
      return;
    }

    const { owner, repo } = context.repo;
    const commitUrl = context.payload.head_commit.url;
    const commitMessage = context.payload.head_commit.message;

    // 获取短 commit hash 用于标题
    const shortCommitHash = context.payload.head_commit.id.substring(0, 7);

    const issueBody =
      `### New changes detected\n\n` +
      `Changes by: @${pusher}\n` +
      `Commit: ${commitUrl}\n` +
      `Message: ${commitMessage}\n\n` +
      `Users to notify: ${Array.from(usersToNotify)
        .map((u) => "@" + u)
        .join(" ")}\n\n` +
      `Changed files:\n${changedFiles
        .map((f) => "- `" + f + "`")
        .join("\n")}\n\n` +
      `### Detailed changes\n\n` +
      fileDetails
        .map(
          ({ file, diff }) =>
            `<details>
          <summary><code>${file}</code></summary>
  
  \`\`\`diff
  ${diff}
  \`\`\`
  
  </details>\n`
        )
        .join("\n") +
      "\n\n---\n" +
      "Please review the changes and close this issue when done.";

    console.log("Creating a new notification issue");
    await github.rest.issues.create({
      owner,
      repo,
      title: `Code Changes Notification [${shortCommitHash}]`,
      body: issueBody,
      labels: ["notification"],
    });
  } catch (error) {
    console.error("Error in Notify File Changes workflow:", error);
    throw error;
  }
};
