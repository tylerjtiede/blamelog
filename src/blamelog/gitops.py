import git
from git import Repo
from datetime import datetime, timezone, timedelta
from blamelog.models import Commit, BlameEntry

def open_repo(path: str) -> Repo:
    try:
        return git.Repo(path)
    except git.InvalidGitRepositoryError:
        raise ValueError(f"Invalid git repository: {path}")

def _build_commit(commit):
    return Commit(
        sha=commit.hexsha,
        author=commit.author.name,
        email=commit.author.email,
        timestamp=commit.authored_datetime,
        message=commit.message
    )

def get_blame(repo, filepath: str) -> list[BlameEntry]:
    blame_list = []
    blame = repo.blame(rev='HEAD', file=filepath)
    line_number = 1
    for block in blame:
        commit = block[0]
        lines = block[1]
        for line in lines:
            blame_list.append(BlameEntry(
                line_number=line_number,
                line_content = line,
                commit = _build_commit(commit)
            ))
            line_number += 1
    
    return blame_list

def get_commits(repo, filepath: str, since_days: int) -> list[Commit]:
    commit_list = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=since_days)
    for commit in repo.iter_commits(rev='HEAD', paths=filepath):
        built_commit = _build_commit(commit)
        if built_commit.timestamp > cutoff:
            commit_list.append(built_commit)
        else:
            break

    return commit_list
