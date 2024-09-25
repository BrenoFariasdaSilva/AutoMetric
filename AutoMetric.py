import argparse # Import the argparse module
import gitlab # Import the gitlab module
import json # Import the json module
import os # Import the os module
import sys # Import the sys module
from datetime import datetime # Import the datetime class from the datetime module
from dotenv import load_dotenv # For loading environment variables from .env file
from github import Github # Import the Github class from the github package
from urllib import parse # Import the parse module from the urllib package

# Global variables
INPUT_FILE = "input.txt" # The input file with repository URLs
OUTPUT_FILE = "output.json" # The output file with repository metadata

# .Env Constants:
ENV_PATH = "./.env" # The path to the .env file
ENV_VARIABLE = "GITHUB_TOKEN" # The environment variable to load

def verify_env_file(env_path=ENV_PATH, key=ENV_VARIABLE):
   """
   Verify if the .env file exists and if the desired key is present.

   :param env_path: Path to the .env file.
   :param key: The key to get in the .env file.
   :return: The value of the key if it exists.
   """

   # Verify if the .env file exists
   if not os.path.exists(env_path):
      print(f"The {env_path} file does not exist.") # Print an error message
      sys.exit(1) # Exit the program

   load_dotenv(env_path) # Load the .env file
   api_key = os.getenv(key) # Get the value of the key

   if not api_key: # If the key does not exist
      print(f"The {key} key does not exist in the {env_path} file.") # Print an error message
      sys.exit(1) # Exit the program

   return api_key # Return the value of the key

def read_input_file(file_path):
   """
   Reads input from a file and returns a list of repository URLs.
   
   :param file_path: Path to the input file
   :return: List of repository URLs
   """

   with open(file_path, "r") as file: # Open the input
      return [line.strip() for line in file if line.strip()] # Return the list of repository URLs

def process_repository(prj_repo, githubToken=verify_env_file()):
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
   prj_org = query.split("/")[-2]
   prj_name = query.split("/")[-1]

   parse_url = parse.quote(prj_repo, safe="")

   now = datetime.now()

   if domain == "github.com":
      g = Github(githubToken)

      try:
         gitRepo = g.get_repo(query)

         # Get contributors
         contributors = gitRepo.get_contributors()

         # Mean Time to Update (MTTU)
         try:
            releases = gitRepo.get_releases()
            if releases.totalCount == 0:
               MU = "n/a"
            else:
               last_release_page_number = (releases.totalCount - 1) // 30
               last_release_page = releases.get_page(last_release_page_number)
               first_release = last_release_page[-1]
               first_release_to_now = now - first_release.created_at
               MU = first_release_to_now.days / releases.totalCount
         except:
               MU = "n/a"

         # Mean Time to Commit (MTTC)
         try:
            commits = gitRepo.get_commits()
            if commits.totalCount == 0:
               MC = "n/a"
            else:
               last_commit_page_number = (commits.totalCount - 1) // 30
               last_commit_page = commits.get_page(last_commit_page_number)
               first_commit = last_commit_page[-1]
               first_commit_to_now = now - first_commit.commit.author.date
               MC = first_commit_to_now.days / commits.totalCount
         except:
            MC = "n/a"

         # Number of Contributors (NC)
         try:
            NC = contributors.totalCount + 1  # +1 to count the owner
         except:
            NC = "n/a"

         # Branch Protection (BP)
         try:
            default_branch = gitRepo.default_branch
            branch = gitRepo.get_branch(default_branch)
            BP = branch.protected
         except:
            BP = "n/a"

         # Inactive Period (IP)
         try:
            commit = branch.commit
            latestCommit = commit.commit.author.date
            howLong = now - latestCommit
            IP = howLong.days
         except:
            IP = "n/a"

      except Exception as e:
         print(f"Error processing GitHub repository: {e}")
         return None

   elif domain in ["salsa.debian.org", "gitlab.freedesktop.org"]:
      try:
         salsa = gitlab.Gitlab("https://" + domain)
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
         latestCommit = datetime.strptime(commit_info["authored_date"], "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=None)
         howLong = now - latestCommit
         IP = howLong.days

      except Exception as e:
         print(f"Error processing GitLab repository: {e}")
         return None
   else:
      print(f"Unsupported domain: {domain}")
      return None

   # Store the metrics in a dictionary
   output["name"] = prj_name
   output["Number of Contributors"] = str(NC)
   output["Inactive Period"] = str(IP)
   output["MTTU"] = str(MU)
   output["MTTC"] = str(MC)
   output["Branch Protection"] = BP

   return output

def process_repositories(repo_urls, githubToken=verify_env_file()):
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

def main(repo_urls=None):
   """
   Main function.

   :param repo_urls: list - Optional list of repository URLs passed as arguments.
   :return: None
   """

   print(f"Welcome to the AutoMetric program!") # Output the welcome message

   if repo_urls:
      print(f"Processing the provided list of repositories...")
      print(f"The output will contain the following metrics: Number of Contributors, Mean Time to Update (MTTU), Mean Time to Commit (MTTC), Branch Protection, and Inactive Period.")
   else:
      print(f"Processing repositories from the input file {INPUT_FILE} and writing output to {OUTPUT_FILE}.")
      print(f"The output will contain the following metrics: Number of Contributors, Mean Time to Update (MTTU), Mean Time to Commit (MTTC), Branch Protection, and Inactive Period.")
      repo_urls = read_input_file(INPUT_FILE) # Read repository URLs from input file if no args

   githubToken = verify_env_file()

   output = [] # Initialize the output list
   for repo_url in repo_urls: # Iterate over the repository URLs
      repo_data = process_repository(repo_url, githubToken) # Process the repository
      if repo_data: # If the repository data is not None
         repo_name = repo_url.split("/")[-1] # Get the repository name from the URL
         repo_data["name"] = repo_name # Add the repository name to the data
         output.append(repo_data) # Append the repository data to the output list

   # Write the output to the file
   with open(OUTPUT_FILE, "w") as outputFile:
      outputFile.write(json.dumps(output, indent=4))
   print(f"Output written to {OUTPUT_FILE}")

   print(f"\nProgram finished.") # Output the end of the program message

if __name__ == "__main__":
   """
   This is the standard boilerplate that calls the main() function.

   :return: None
   """

   parser = argparse.ArgumentParser(description="AutoMetric - Analyze repository metrics")
   parser.add_argument("repo_urls", nargs="*", help="List of repository URLs to process", default=None)

   args = parser.parse_args() # Parse arguments

   if args.repo_urls: # If repository URLs are provided as arguments
      main(args.repo_urls) # Pass the list of repo URLs to main
   else: # If no arguments
      main() # Run without arguments, fall back to input file processing