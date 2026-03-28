import click
from blamelog.gitops import open_repo, get_blame, get_commits
from blamelog.models import FileReport

@click.group()
def main():
    pass

@main.command()
@click.argument('path')
@click.option('--days', default=30, help='number of days to look back')
def report(path, days):
    
    repo = open_repo(".")

    blame_list = get_blame(repo, path)
    commit_list = get_commits(repo, path, days)

    print(blame_list, commit_list)
