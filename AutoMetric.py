import argparse # Import the argparse module
import atexit # For playing a sound when the program finishes
import gitlab # Import the gitlab module
import json # Import the json module
import os # For running a command in the terminal
import platform # For getting the operating system name
import sys # Import the sys module
from colorama import Style # For coloring the terminal
from datetime import datetime, timezone # Import the datetime class from the datetime module
from dotenv import load_dotenv # For loading environment variables from .env file
from github import Github # Import the Github class from the github package
from urllib import parse # Import the parse module from the urllib package

# Global variables
INPUT_FILE = "input.txt" # The input file with repository URLs
OUTPUT_DIR = "output/" # The output directory

# .Env Constants:
ENV_PATH = "./.env" # The path to the .env file
ENV_VARIABLE = "GITHUB_TOKEN" # The environment variable to load

# Macros:
class BackgroundColors: # Colors for the terminal
   CYAN = "\033[96m" # Cyan
   GREEN = "\033[92m" # Green
   YELLOW = "\033[93m" # Yellow
   RED = "\033[91m" # Red
   BOLD = "\033[1m" # Bold
   UNDERLINE = "\033[4m" # Underline
   CLEAR_TERMINAL = "\033[H\033[J" # Clear the terminal

# Sound Constants:
SOUND_COMMANDS = {"Darwin": "afplay", "Linux": "aplay", "Windows": "start"} # The commands to play a sound for each operating system
SOUND_FILE = "./.assets/Sounds/NotificationSound.wav" # The path to the sound file

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
   Parses the repository URL to extract domain, owner/organization, and project name.
   
   :param repo_url: The full repository URL
   :return: Tuple containing (domain, owner/organization, project name, repository path)
   """

   parsed_url = parse.urlparse(repo_url) # Parse the repository URL
   repo_path = parsed_url.path[1:] # Remove leading slash
   domain = parsed_url.netloc # Get the domain
   owner_name = repo_path.split("/")[-2] # Get the owner/organization name
   repo_name = repo_path.split("/")[-1] # Get the project name
   return domain, owner_name, repo_name, repo_path # Return the domain, owner/organization, project name, and repository path

def build_output_file_path(repo_urls):
	"""
	Builds the output file path.

	:param repo_urls: The list of repository URLs.
	:return: The output file path.
	"""

	output_filename = OUTPUT_DIR # Set the output file name
 
	if repo_urls and len(repo_urls) > 1: # If there are multiple repository URLs
		output_filename += "repositories_metrics.json" # Set the output file name to repositories_metrics.json
	else: # If there is only one repository URL
		domain, repo_owner, repo_name, repo_path = parse_repository_url(repo_urls[0]) # Parse the repository URL
		output_filename += f"{repo_owner}-{repo_name}.json"

	return output_filename # Return the output file path

def get_env_token(env_path=ENV_PATH, key=ENV_VARIABLE):
   """
   Verify if the .env file exists and if the desired key is present.

   :param env_path: Path to the .env file.
   :param key: The key to get in the .env file.
   :return: The value of the key if it exists.
   """

   # Verify if the .env file exists
   if not os.path.exists(env_path):
      print(f"{BackgroundColors.RED}The {BackgroundColors.GREEN}{env_path}{BackgroundColors.RED} file does not exist.{Style.RESET_ALL}") # Print an error message
      sys.exit(1) # Exit the program

   load_dotenv(env_path) # Load the .env file
   api_key = os.getenv(key) # Get the value of the key

   if not api_key: # If the key does not exist
      print(f"{BackgroundColors.RED}The {BackgroundColors.GREEN}{key}{BackgroundColors.RED} key does not exist in the {BackgroundColors.GREEN}{env_path}{BackgroundColors.RED} file.{Style.RESET_ALL}") # Print an error message
      sys.exit(1) # Exit the program

   return api_key # Return the value of the key

def get_number_of_contributors_github(repo):
   """
   Get the number of contributors.
   
   :param repo: GitHub repository object
   :return: Total number of contributors
   """
   
   contributors = repo.get_contributors() # Get the contributors
   return contributors.totalCount # Get the total number of contributors

def calculate_mttu_github(repo, now):
   """
   Calculate the Mean Time to Update (MTTU).
   
   :param repo: GitHub repository object
   :param now: Current date and time
   :return: Mean Time to Update (MTTU)
   """

   releases = repo.get_releases() # Get the releases
   if releases.totalCount > 0: # If there are releases
      first_release = releases.get_page(releases.totalCount // 30)[-1] # Get the first release
      days_since_first_release = (now - first_release.created_at).days # Calculate the days since the first release
      return days_since_first_release / releases.totalCount # Calculate the mean time to update
   return "n/a" # Set the mean time to update to "n/a"

def calculate_mttc_github(repo, now):
   """
   Calculate the Mean Time to Commit (MTTC).
   
   :param repo: GitHub repository object
   :param now: Current date and time
   :return: Mean Time to Commit (MTTC)
   """

   commits = repo.get_commits() # Get the commits
   if commits.totalCount > 0: # If there are commits
      first_commit = commits.get_page(commits.totalCount // 30)[-1] # Get the first commit
      days_since_first_commit = (now - first_commit.commit.author.date.replace(tzinfo=timezone.utc)).days # Calculate the days since the first commit
      return days_since_first_commit / commits.totalCount # Calculate the mean time to commit
   return "n/a" # Set the mean time to commit to "n/a"

def get_branch_protection_github(repo):
   """
   Get branch protection status.
   
   :param repo: GitHub repository object
   :return: Branch protection status
   """

   try: # Try to get the branch protection
      default_branch = repo.get_branch(repo.default_branch) # Get the default branch
      return default_branch.protected # Get the branch protection status
   except Exception: # If an exception occurs
      return "n/a" # Set the branch protection status to "n/a"

def get_inactive_period_github(repo, now):
   """
   Calculate the Inactive Period (IP).
   
   :param repo: GitHub repository object
   :param now: Current date and time
   :return: Inactive Period (IP)
   """

   try: # Try to get the inactive period
      latest_commit_date = repo.get_branch(repo.default_branch).commit.commit.author.date # Get the latest commit date
      return (now - latest_commit_date).days # Calculate the inactive period
   except Exception: # If an exception occurs
      return "n/a" # Set the inactive period to "n/a"

def process_github_repository(repo_path, github_token):
   """
   Processes a GitHub repository to extract its metadata.

   :param repo_path: GitHub repository path (org/repo)
   :param github_token: GitHub token for API access
   :return: Dictionary with repository metadata
   """

   github = Github(github_token) # Create a GitHub instance
   try: # Try to process the GitHub repository
      repo = github.get_repo(repo_path) # Get the GitHub repository
      now = datetime.now(timezone.utc) # Get the current date and time

      nc = get_number_of_contributors_github(repo) # Number of contributors (NC)
      mttu = calculate_mttu_github(repo, now) # Mean Time to Update (MTTU)
      mttc = calculate_mttc_github(repo, now) # Mean Time to Commit (MTTC)
      branch_protection = get_branch_protection_github(repo) # Branch protection (BP)
      ip = get_inactive_period_github(repo, now) # Inactive Period (IP)

      return { # Return the repository metadata dictionary
         "Repository Name": repo_path, # Add repository name as the first element
         "Number of Contributors": nc, # Return the number of contributors
         "MTTU": mttu, # Return the mean time to update
         "MTTC": mttc, # Return the mean time to commit
         "Branch Protection": branch_protection, # Return the branch protection status
         "Inactive Period": ip # Return the inactive period
      }
   except Exception as e: # If an exception occurs
      print(f"{BackgroundColors.RED}Error processing GitHub repository {BackgroundColors.GREEN}{repo_path}{BackgroundColors.RED}: {e}{Style.RESET_ALL}") # Output the error message
      return None # Return None

def create_gitlab_instance(domain):
   """
   Create a GitLab instance.
   
   :param domain: The GitLab domain (e.g., gitlab.com)
   :return: GitLab instance
   """

   return gitlab.Gitlab(f"https://{domain}") # Create a GitLab instance

def get_gitlab_project(gitlab_instance, repo_path):
   """
   Get the GitLab project.
   
   :param gitlab_instance: GitLab instance
   :param repo_path: The repository path (org/repo)
   :return: GitLab project object
   """

   return gitlab_instance.projects.get(repo_path) # Get the GitLab project

def get_default_branch_gitlab(project):
   """
   Get the default branch of the project.
   
   :param project: GitLab project object
   :return: Default branch
   """

   return next((branch for branch in project.branches.list() if branch.default), None) # Get the default branch

def get_number_of_contributors_gitlab(project):
   """
   Get the number of contributors (NC).
   
   :param project: GitLab project object
   :return: Number of contributors
   """

   return len(project.repository_contributors(get_all=True)) # Number of contributors (NC)

def get_branch_protection_gitlab(default_branch):
   """
   Get branch protection status (BP).
   
   :param default_branch: The default branch of the GitLab project
   :return: Branch protection status
   """

   return default_branch.protected # Return the branch protection status

def calculate_inactive_period_gitlab(default_branch, now):
   """
   Calculate the Inactive Period (IP).
   
   :param default_branch: The default branch of the GitLab project
   :param now: Current date and time
   :return: Inactive Period (IP)
   """

   latest_commit_date = datetime.strptime( # Get the latest commit date
      default_branch.commit["authored_date"], "%Y-%m-%dT%H:%M:%S.%f%z"
   ).replace(tzinfo=None) # Remove the timezone
   return (now - latest_commit_date).days # Calculate the inactive period

def process_gitlab_repository(domain, repo_path):
   """
   Processes a GitLab repository to extract its metadata.
   
   :param domain: The GitLab domain (e.g., gitlab.com)
   :param repo_path: The repository path (org/repo)
   :return: Dictionary with repository metadata
   """

   try: # Try to process the GitLab repository
      gitlab_instance = create_gitlab_instance(domain) # Create a GitLab instance
      project = get_gitlab_project(gitlab_instance, repo_path) # Get the GitLab project
      default_branch = get_default_branch_gitlab(project) # Get the default branch

      if not default_branch: # If the default branch is not found
         return None # Return None

      nc = get_number_of_contributors_gitlab(project) # Number of contributors (NC)
      branch_protection = get_branch_protection_gitlab(default_branch) # Branch protection (BP)

      now = datetime.now(timezone.utc) # Get the current date and time
      ip = calculate_inactive_period_gitlab(default_branch, now) # Inactive Period (IP)

      return { # Return the repository metadata dictionary
         "Repository Name": repo_path, # Add repository name as the first element
         "Number of Contributors": nc, # Return the number of contributors
         "MTTU": "n/a", # GitLab doesn't support releases as in GitHub
         "MTTC": "n/a", # GitLab doesn't directly provide this info
         "Branch Protection": branch_protection, # Return the branch protection status
         "Inactive Period": ip # Return the inactive period
      }
   except Exception as e: # If an exception occurs
      print(f"{BackgroundColors.RED}Error processing GitLab repository {BackgroundColors.GREEN}{repo_path}{BackgroundColors.RED}: {e}{Style.RESET_ALL}") # Output the error message
      return None # Return None

def convert_days_to_appropriate_time(days):
   """
   Converts the days to an appropriate time format.
   
   :param days: Number of days (can be a string)
   :return: String with the time format or an error message
   """
   
   # Check if days is a valid number (float or int)
   try: # Try to convert days to float
      days = float(days) # Convert days to float
   except ValueError:
      return days # Return the days as a string

   if days < 1: # If the days are less than 1
      return f"{days * 24:.2f} hours" # Return the hours
   elif days < 30: # If the days are less than 30
      whole_days = int(days) # Whole days
      hours = (days - whole_days) * 24 # Convert decimal part to hours
      hours_str = f", {hours:.2f} hour{'s' if hours != 1 else ''}" if hours > 0 else ''
      return f"{whole_days} day{'s' if whole_days != 1 else ''}{hours_str}" if whole_days > 0 else f"{hours:.2f} hours"
   elif days < 365: # If the days are less than 365
      months = int(days // 30) # Whole months
      leftover_days = days % 30 # Decimal part converted to days
      days_str = f", {leftover_days:.0f} day{'s' if leftover_days != 1 else ''}" if leftover_days > 0 else ''
      return f"{months} month{'s' if months != 1 else ''}{days_str}"
   else: # If the days are more than 365
      years = int(days // 365) # Whole years
      leftover_months = (days % 365) / 30 # Decimal part converted to months
      months = int(leftover_months)
      leftover_days = (leftover_months - months) * 30
      months_str = f", {months} month{'s' if months != 1 else ''}" if months > 0 else ''
      days_str = f", {leftover_days:.0f} day{'s' if leftover_days != 1 else ''}" if leftover_days > 0 else ''
      return f"{years} year{'s' if years != 1 else ''}{months_str}{days_str}"

def print_repository_metrics(metadata):
   """
   Prints the repository metadata.
   
   :param metadata: Dictionary containing repository metadata
   """

   print(f"{BackgroundColors.CYAN}{metadata['Repository Name']}{Style.RESET_ALL}", end=": ") # Output the repository name
   print(f"{BackgroundColors.GREEN}Number of Contributors: {BackgroundColors.CYAN}{metadata['Number of Contributors']}{Style.RESET_ALL}", end=", ") # Output the number of contributors
   print(f"{BackgroundColors.GREEN}MTTU: {BackgroundColors.CYAN}{BackgroundColors.CYAN}{convert_days_to_appropriate_time(metadata['MTTU'])}{Style.RESET_ALL}", end=", ") # Output the mean time to update
   print(f"{BackgroundColors.GREEN}MTTC: {BackgroundColors.CYAN}{convert_days_to_appropriate_time(metadata['MTTC'])}{Style.RESET_ALL}", end=", ") # Output the mean time to commit
   print(f"{BackgroundColors.GREEN}Branch Protection: {BackgroundColors.CYAN}{metadata['Branch Protection']}{Style.RESET_ALL}", end=", ") # Output the branch protection status
   print(f"{BackgroundColors.GREEN}Inactive Period: {BackgroundColors.CYAN}{convert_days_to_appropriate_time(metadata['Inactive Period'])}{Style.RESET_ALL}", end="\n\n") # Output the inactive period

def process_repository(repo_url, github_token):
   """
   Determines the repository hosting service (GitHub or GitLab) and processes the repository accordingly.
   
   :param repo_url: Full repository URL
   :param github_token: GitHub token for API access
   :return: Dictionary containing processed repository metadata
   """

   domain, owner_name, repo_name, repo_path = parse_repository_url(repo_url) # Parse the repository URL
   print(f"{BackgroundColors.GREEN}Processing {BackgroundColors.CYAN}{domain}/{repo_path}{BackgroundColors.GREEN}...{Style.RESET_ALL}") # Output the processing message

   if domain == "github.com": # If the domain is GitHub
      metrics = process_github_repository(repo_path, github_token) # Process the GitHub repository
   elif domain in ["salsa.debian.org", "gitlab.freedesktop.org"]: # If the domain is GitLab
      metrics = process_gitlab_repository(domain, repo_path) # Process the GitLab repository
   else: # If the domain is not supported
      print(f"{BackgroundColors.GREEN}Unsupported domain: {BackgroundColors.CYAN}{domain}{Style.RESET_ALL}") # Output the unsupported domain message
      return None # Return None

   print_repository_metrics(metrics) if metrics else None # Print the repository metadata
   
   return metrics # Return the metrics dictionary

def get_full_directory_path(relative_dir_path):
	"""
	Gets the full directory name given a relative directory path.

	:param relative_dir_path: The relative directory path.
	:return: The full directory path.

	"""
		
	return os.path.abspath(relative_dir_path) # Return the full directory path

def create_directory(full_directory_name):
   """
   Creates a directory.

   :param full_directory_name: Name of the directory to be created.
   :param relative_directory_name: Relative name of the directory to be created that will be shown in the terminal.
   :return: None
   """

   if os.path.isdir(full_directory_name): # Verify if the directory already exists
      return # Return if the directory already exists
   try: # Try to create the directory
      os.makedirs(full_directory_name) # Create the directory
   except OSError: # If the directory cannot be created
      print(f"{BackgroundColors.GREEN}The creation of the {BackgroundColors.CYAN}{full_directory_name}{BackgroundColors.GREEN} directory failed.{Style.RESET_ALL}")

def write_output(output_data, file_path):
   """
   Writes the output data to a JSON file.
   
   :param output_data: List of dictionaries containing repository metadata
   :param file_path: Path to the output JSON file
   """
   
   print(f"{BackgroundColors.GREEN}Writing output to {BackgroundColors.CYAN}{file_path}{BackgroundColors.GREEN}...{Style.RESET_ALL}") # Output the writing message

   with open(file_path, "w") as file: # Open the output file
      json.dump(output_data, file, indent=4) # Write the output data to the file
      
   print(f"{BackgroundColors.GREEN}Output written to {BackgroundColors.CYAN}{file_path}{BackgroundColors.GREEN}.{Style.RESET_ALL}") # Output the written message

def play_sound():
   """
   Plays a sound when the program finishes.

   :return: None
   """

   if os.path.exists(SOUND_FILE):
      if platform.system() in SOUND_COMMANDS: # If the platform.system() is in the SOUND_COMMANDS dictionary
         os.system(f"{SOUND_COMMANDS[platform.system()]} {SOUND_FILE}")
      else: # If the platform.system() is not in the SOUND_COMMANDS dictionary
         print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}platform.system(){BackgroundColors.RED} is not in the {BackgroundColors.CYAN}SOUND_COMMANDS dictionary{BackgroundColors.RED}. Please add it!{Style.RESET_ALL}")
   else: # If the sound file does not exist
      print(f"{BackgroundColors.RED}Sound file {BackgroundColors.CYAN}{SOUND_FILE}{BackgroundColors.RED} not found. Make sure the file exists.{Style.RESET_ALL}")

def main(repo_urls=None, github_token=None, finish_sound=False):
	"""
	Main function.

	:param repo_urls: list - Optional list of repository URLs passed as arguments.
	:param github_token: str - Optional GitHub token passed as an argument.
	:param finish_sound: bool - Optional flag to play a sound when the program finishes.
	:return: None
	"""

	print(f"{BackgroundColors.GREEN}Welcome to the {BackgroundColors.CYAN}AutoMetric{BackgroundColors.GREEN} program!{Style.RESET_ALL}") # Output the welcome message
	print(f"{BackgroundColors.GREEN}This project process the following metrics: {BackgroundColors.CYAN}Number of Contributors, Mean Time to Update (MTTU), Mean Time to Commit (MTTC), Branch Protection, and Inactive Period{BackgroundColors.GREEN} for GitHub and GitLab repositories.{Style.RESET_ALL}") # Output the metrics message

	repo_urls = repo_urls if repo_urls else read_input_file(INPUT_FILE) # Read repository URLs from input file if no args where passed
	output_file_path = build_output_file_path(repo_urls) # Build the output file path

	if len(repo_urls) > 1: # If there are multiple repository URLs
		print(f"{BackgroundColors.GREEN}Processing the repositories list and writing the output to {BackgroundColors.CYAN}{output_file_path}{BackgroundColors.GREEN}.{Style.RESET_ALL}", end="\n\n")
	else: # If there is only one repository URL
		print(f"{BackgroundColors.GREEN}Processing the {repo_urls} repository and writing the output to {BackgroundColors.CYAN}{output_file_path}{BackgroundColors.GREEN}.{Style.RESET_ALL}", end="\n\n")

	github_token = get_env_token() if not github_token else github_token # Verify the .env file and get the GitHub token

	metrics = [] # Initialize the output list
	for repo_url in repo_urls: # Iterate over the repository URLs
		repo_data = process_repository(repo_url, github_token) # Process the repository
		if repo_data: # If the repository data is not None
			metrics.append(repo_data) # Append the repository data to the output list

	create_directory(get_full_directory_path(OUTPUT_DIR)) # Create the output directory
	write_output(metrics, output_file_path) # Write the output to a file

	print(f"{BackgroundColors.GREEN}\nProgram finished.{Style.RESET_ALL}") # Output the end of the program message

	atexit.register(play_sound) if finish_sound else None # Register the function to play a sound when the program finishes

if __name__ == "__main__":
   """
   This is the standard boilerplate that calls the main() function.

   :return: None
   """

   parser = argparse.ArgumentParser(description="AutoMetric - Analyze repository metrics") # Create an argument parser
   parser.add_argument("--repo_urls", nargs="*", help="List of repository URLs to process", default=None) # Add an optional argument for repository URLs
   parser.add_argument("--github_token", help="GitHub Token to access private repositories", default=None) # Add an optional argument for the GitHub token
   parser.add_argument("--finish_sound", action="store_true", help="Play a sound when the program finishes", default=False) # Add an optional argument for playing a sound when the program finishes

   args = parser.parse_args() # Parse arguments

   main(repo_urls=args.repo_urls, github_token=args.github_token, finish_sound=args.finish_sound) # Call main with the arguments
