# Lab 5 – Reflection

NOTE: the handout text I received does not list the four reflection questions. These are the standard ones for this lab; match them to the exact wording in your handout.

**1. Which tool was most useful, and why?**
Bandit found the most serious problems: `shell=True` (command injection) and `mktemp` (race condition) are real vulnerabilities that Pylint and Flake8 do not report. Pylint gave the biggest quality gain (score 4.91 -> 10.00) because it caught the mutable default argument, the broad `except`, naming and missing docstrings. Flake8 was the quickest to fix, as it only reports formatting.

**2. Did any report contain false positives or items you disagreed with?**
B404 (importing `subprocess`) is only informational: the module is needed. I kept it and annotated `# nosec B404`, and also `# nosec B603 B607` on the ping call, because the address is validated and `shell=False` is used. A `nosec` should always carry a reason, or it just hides a real problem.

**3. How does static analysis fit into a development workflow?**
It runs without executing the code, so it can run in an editor, as a pre-commit hook or in CI on every push. Problems are caught while they are cheap to fix, reviewers spend time on design instead of style, and security mistakes are caught before release. It does not replace tests: the program output was identical before and after, which I checked by running it.

**4. What did you learn?**
Code that "works" can still be unsafe or fragile: a shared mutable default, a predictable OTP, an unsafe temp file and an injectable shell command all ran fine in the demo. Fixing issues by severity (Bandit High/Medium first) and committing one tool at a time made each change easy to verify by re-running that tool.
