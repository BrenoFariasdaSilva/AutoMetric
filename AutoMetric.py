from urllib import parse
import json
from github import Github
import gitlab
from datetime import datetime
import argparse

# Global variables
INPUT_FILE = "input.txt" # The input file with repository URLs
OUTPUT_FILE = "output.json" # The output file with repository metadata

def process_repository(prj_repo, githubToken=''):
   """
   Function to process a single repository and extract its metrics.
   :param prj_repo: str - The repository URL.
   :param githubToken: str - The GitHub token.
   :return: dict - The repository metrics.
   """

   output = {}
   query = parse.urlparse(prj_repo)[2][1:]
   print(f"Processing repository: {query}")
   domain = parse.urlparse(prj_repo)[1]
   prj_org = query.split('/')[-2]
   prj_name = query.split('/')[-1]

   parse_url = parse.quote(prj_repo, safe='')

   now = datetime.now()

   if domain == 'github.com':
      g = Github(githubToken)

      try:
         gitRepo = g.get_repo(query)

         # Get contributors
         contributors = gitRepo.get_contributors()

         # Mean Time to Update (MTTU)
         try:
            releases = gitRepo.get_releases()
            if releases.totalCount == 0:
               MU = 'n/a'
            else:
               last_release_page_number = (releases.totalCount - 1) // 30
               last_release_page = releases.get_page(last_release_page_number)
               first_release = last_release_page[-1]
               first_release_to_now = now - first_release.created_at
               MU = first_release_to_now.days / releases.totalCount
         except:
               MU = 'n/a'

         # Mean Time to Commit (MTTC)
         try:
            commits = gitRepo.get_commits()
            if commits.totalCount == 0:
               MC = 'n/a'
            else:
               last_commit_page_number = (commits.totalCount - 1) // 30
               last_commit_page = commits.get_page(last_commit_page_number)
               first_commit = last_commit_page[-1]
               first_commit_to_now = now - first_commit.commit.author.date
               MC = first_commit_to_now.days / commits.totalCount
         except:
            MC = 'n/a'

         # Number of Contributors (NC)
         try:
            NC = contributors.totalCount + 1  # +1 to count the owner
         except:
            NC = 'n/a'

         # Branch Protection (BP)
         try:
            default_branch = gitRepo.default_branch
            branch = gitRepo.get_branch(default_branch)
            BP = branch.protected
         except:
            BP = 'n/a'

         # Inactive Period (IP)
         try:
            commit = branch.commit
            latestCommit = commit.commit.author.date
            howLong = now - latestCommit
            IP = howLong.days
         except:
            IP = 'n/a'

      except Exception as e:
         print(f"Error processing GitHub repository: {e}")
         return None

   elif domain in ['salsa.debian.org', 'gitlab.freedesktop.org']:
      try:
         salsa = gitlab.Gitlab('https://' + domain)
         project = salsa.projects.get(query)

         # Get default branch
         branches = project.branches.list()
         default_branch = next((branch for branch in branches if branch.default), None)
         
         # Number of Contributors (NC)
         contributors = project.repository_contributors(get_all=True)
         NC = len(contributors)

         # Branch Protection (BP)
         BP = default_branch.protected

         # Inactive Period (IP)
         commit_info = default_branch.commit
         latestCommit = datetime.strptime(commit_info['authored_date'], '%Y-%m-%dT%H:%M:%S.%f%z').replace(tzinfo=None)
         howLong = now - latestCommit
         IP = howLong.days

      except Exception as e:
         print(f"Error processing GitLab repository: {e}")
         return None
   else:
      print(f"Unsupported domain: {domain}")
      return None

   # Store the metrics in a dictionary
   output['name'] = prj_name
   output['Number of Contributors'] = str(NC)
   output['Inactive Period'] = str(IP)
   output['MTTU'] = str(MU)
   output['MTTC'] = str(MC)
   output['Branch Protection'] = BP

   return output

def process_repositories(repo_urls, githubToken=''):
   """
   Process a list of repository URLs.
   :param repo_urls: list - List of repository URLs.
   :param githubToken: str - GitHub token.
   :return: list - List of repository metrics.
   """

   output = []
   for repo_url in repo_urls:
      repo_data = process_repository(repo_url, githubToken)
      if repo_data:
         output.append(repo_data)
   return output

def main(repo_urls=None, githubToken=''):
   """
   Main function.
   :param repo_urls: list - List of repository URLs.
   :param githubToken: str - GitHub token.
   :return: None
   """

   if not repo_urls:
      # Fallback to reading from the input file if no URLs are provided
      with open(INPUT_FILE, 'r') as f:
         repo_urls = [line.strip() for line in f if line.strip()]

   # Process the repositories and get the output
   output = process_repositories(repo_urls, githubToken)

   # Write the output to the file
   with open(OUTPUT_FILE, 'w') as outputFile:
      outputFile.write(json.dumps(output, indent=4))

   print(f"Output written to {OUTPUT_FILE}")

if __name__ == "__main__":
   # Argument parser to handle command-line inputs
   parser = argparse.ArgumentParser(description="Process repository URLs for metrics extraction")
   parser.add_argument(
      'repo_urls', nargs='*', help="List of repository URLs to process", default=None
   )
   parser.add_argument(
      '--githubToken', help="GitHub token for authentication", default=''
   )

   args = parser.parse_args()

   # If repository URLs are passed as arguments, use them. Otherwise, fallback to input file.
   if args.repo_urls:
      main(repo_urls=args.repo_urls, githubToken=args.githubToken)
   else:
      main(githubToken=args.githubToken)
