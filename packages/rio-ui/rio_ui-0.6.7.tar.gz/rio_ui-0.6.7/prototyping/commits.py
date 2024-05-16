import asyncio
import json
from datetime import datetime


async def main() -> None:
    # Run the command and fetch its output
    process = await asyncio.create_subprocess_shell(
        """git log --pretty=format:'{"commit": "%H", "author": "%aN <%aE>", "date": "%ad", "message": "%f"}'""",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    # Decode the output
    stdout, stderr = await process.communicate()
    output = stdout.decode().strip()
    lines = output.split("\n")

    for line in lines:
        entry = json.loads(line)
        commit_hash = entry["commit"]
        author = entry["author"]
        date = datetime.strptime(entry["date"], "%a %b %d %H:%M:%S %Y %z")
        message = entry["message"]

        # Filter the commits
        if date.weekday() not in {0, 1, 2, 3}:
            continue

        if date.hour < 8 or date.hour > 16:
            continue

        if "aran" in author.lower():
            continue

        # Display matches
        print(f"{commit_hash} - {author} - {date} - {message}")


if __name__ == "__main__":
    asyncio.run(main())
