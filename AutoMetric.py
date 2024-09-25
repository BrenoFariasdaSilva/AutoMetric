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

def parse_repository_url(repo_url):
   """
   Parses the repository URL to extract domain, organization, and project name.
   
   :param repo_url: The full repository URL
   :return: Tuple containing (domain, organization, project name, repository path)
   """

   parsed_url = parse.urlparse(repo_url) # Parse the repository URL
   repo_path = parsed_url.path[1:] # Remove leading slash
   domain = parsed_url.netloc # Get the domain
   org_name = repo_path.split("/")[-2] # Get the organization name
   project_name = repo_path.split("/")[-1] # Get the project name
   return domain, org_name, project_name, repo_path # Return the domain, organization, project name, and repository path

def process_github_repository(repo_path, githubToken):
   """
   Processes a GitHub repository to extract its metadata.
   
   :param repo_path: GitHub repository path (org/repo)
   :param githubToken: GitHub token for API access
   :return: Dictionary with repository metadata
   """

   github = Github(githubToken) # Create a GitHub instance
   try: # Try to process the GitHub repository
      repo = github.get_repo(repo_path) # Get the GitHub repository
      now = datetime.now() # Get the current date and time

      # Number of contributors (NC)
      contributors = repo.get_contributors() # Get the contributors
      nc = contributors.totalCount # Get the total number of contributors

      # Mean Time to Update (MTTU)
      releases = repo.get_releases() # Get the releases
      if releases.totalCount > 0: # If there are releases
         first_release = releases.get_page(releases.totalCount // 30)[-1] # Get the first release
         days_since_first_release = (now - first_release.created_at).days # Calculate the days since the first release
         mttu = days_since_first_release / releases.totalCount # Calculate the mean time to update
      else: # If there are no releases
         mttu = "n/a" # Set the mean time to update to "n/a"

      # Mean Time to Commit (MTTC)
      commits = repo.get_commits() # Get the commits
      if commits.totalCount > 0: # If there are commits
         first_commit = commits.get_page(commits.totalCount // 30)[-1] # Get the first commit
         days_since_first_commit = (now - first_commit.commit.author.date).days # Calculate the days since the first commit
         mttc = days_since_first_commit / commits.totalCount # Calculate the mean time to commit
      else: # If there are no commits
         mttc = "n/a" # Set the mean time to commit to "n/a"

      # Branch protection (BP)
      try: # Try to get the branch protection
         default_branch = repo.get_branch(repo.default_branch) # Get the default branch
         branch_protection = default_branch.protected # Get the branch protection status
      except: # If an exception occurs
         branch_protection = "n/a" # Set the branch protection status to "n/a"

      # Inactive Period (IP)
      try: # Try to get the inactive period
         latest_commit_date = repo.get_branch(repo.default_branch).commit.commit.author.date # Get the latest commit date
         ip = (now - latest_commit_date).days # Calculate the inactive period
      except: # If an exception occurs
         ip = "n/a" # Set the inactive period to "n/a"

      return { # Return the repository metadata dictionary
         "Number of Contributors": nc, # Return the number of contributors
         "MTTU": mttu, # Return the mean time to update
         "MTTC": mttc, # Return the mean time to commit
         "Branch Protection": branch_protection, # Return the branch protection status
         "Inactive Period": ip # Return the inactive period
      }
   except Exception as e: # If an exception occurs
      print(f"Error processing GitHub repository {repo_path}: {e}") # Output the error message
      return None # Return None

def process_gitlab_repository(domain, repo_path):
   """
   Processes a GitLab repository to extract its metadata.
   
   :param domain: The GitLab domain (e.g., gitlab.com)
   :param repo_path: The repository path (org/repo)
   :return: Dictionary with repository metadata
   """

   try: # Try to process the GitLab repository
      gitlab_instance = gitlab.Gitlab(f"https://{domain}") # Create a GitLab instance
      project = gitlab_instance.projects.get(repo_path) # Get the GitLab project
      default_branch = next((branch for branch in project.branches.list() if branch.default), None) # Get the default branch

      if not default_branch: # If the default branch is not found
         return None # Return None

      # Number of contributors (NC)
      nc = len(project.repository_contributors(get_all=True))

      # Branch protection (BP)
      branch_protection = default_branch.protected

      # Inactive Period (IP)
      now = datetime.now() # Get the current date and time
      latest_commit_date = datetime.strptime( # Get the latest commit date
         default_branch.commit["authored_date"], "%Y-%m-%dT%H:%M:%S.%f%z"
      ).replace(tzinfo=None)
      ip = (now - latest_commit_date).days # Calculate the inactive period

      return {
         "Number of Contributors": nc, # Return the number of contributors
         "MTTU": "n/a", # GitLab doesn't support releases as in GitHub
         "MTTC": "n/a", # GitLab doesn't directly provide this info
         "Branch Protection": branch_protection, # Return the branch protection status
         "Inactive Period": ip # Return the inactive period
      }
   except Exception as e: # If an exception occurs
      print(f"Error processing GitLab repository {repo_path}: {e}") # Output the error message
      return None # Return None

def process_repository(repo_url, githubToken):
   """
   Determines the repository hosting service (GitHub or GitLab) and processes the repository accordingly.
   
   :param repo_url: Full repository URL
   :param githubToken: GitHub token for API access
   :return: Dictionary containing processed repository metadata
   """

   domain, org, project_name, repo_path = parse_repository_url(repo_url) # Parse the repository URL
   print(f"Processing {domain}/{repo_path}...") # Output the processing message

   if domain == "github.com": # If the domain is GitHub
      return process_github_repository(repo_path, githubToken) # Process the GitHub repository
   elif domain in ["salsa.debian.org", "gitlab.freedesktop.org"]: # If the domain is GitLab
      return process_gitlab_repository(domain, repo_path) # Process the GitLab repository
   else: # If the domain is not supported
      print(f"Unsupported domain: {domain}") # Output the unsupported domain message
      return None # Return None

def write_output(output_data, file_path):
   """
   Writes the output data to a JSON file.
   
   :param output_data: List of dictionaries containing repository metadata
   :param file_path: Path to the output JSON file
   """

   with open(file_path, "w") as file: # Open the output file
      json.dump(output_data, file, indent=4) # Write the output data to the file

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

   githubToken = verify_env_file() # Verify the .env file and get the GitHub token

   output = [] # Initialize the output list
   for repo_url in repo_urls: # Iterate over the repository URLs
      repo_data = process_repository(repo_url, githubToken) # Process the repository
      if repo_data: # If the repository data is not None
         repo_name = repo_url.split("/")[-1] # Get the repository name from the URL
         repo_data["name"] = repo_name # Add the repository name to the data
         output.append(repo_data) # Append the repository data to the output list

   write_output(output, OUTPUT_FILE) # Write the output to a file
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