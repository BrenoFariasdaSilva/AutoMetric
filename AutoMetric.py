import argparse # Import the argparse module
import atexit # For playing a sound when the program finishes
import gitlab # Import the gitlab module
import json # Import the json module
import os # For running a command in the terminal
import platform # For getting the operating system name
import sys # Import the sys module
import time # Import the time module
from colorama import Style # For coloring the terminal
from datetime import datetime, timezone # Import the datetime class from the datetime module
from dotenv import load_dotenv # For loading environment variables from .env file
from github import Github # Import the Github class from the github package
from urllib import parse # Import the parse module from the urllib package

# Global variables
INPUT_FILE = "input.txt" # The input file with repository URLs
OUTPUT_DIR = "output/" # The output directory
FORMAT_METRICS = True # Format the metrics to the appropriate time format and not just days

# .Env Constants:
ENV_PATH = "./.env" # The path to the .env file
ENV_VARIABLE = "GITHUB_TOKEN" # The environment variable to load

# Time Constants:
TIME_UNITS = [60, 3600, 86400] # Seconds in a minute, seconds in an hour, seconds in a day

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

def delete_old_output_file(output_file_path):
   """
   Deletes the old output file if it exists.
   
   :param output_file_path: Path to the output file
   :return: None
   """

   if os.path.exists(output_file_path): # If the output file exists
      os.remove(output_file_path) # Remove the output file

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

def convert_days_to_appropriate_time(days):
   """
   Converts the days to an appropriate time format.
   
   :param days: Number of days (can be a string)
   :return: String with the time format or an error message
   """

   # Verify if the days is a string
   try: # Try to convert the days to a float
      days = float(days) # Convert days to float
   except ValueError: # If the days cannot be converted to a float
      return days  # Return the days as a string

   # Define time units in days
   time_units = [
      (365, "year", "years"),
      (30, "month", "months"),
      (1, "day", "days"),
      (1/24, "hour", "hours"),
   ]

   time_components = [] # Initialize the time components list

   # Handle time conversion based on the value of days
   for unit_value, singular, plural in time_units: # Iterate over the time units
      if days >= unit_value: # If days is greater than or equal to the unit value
         unit_count = int(days // unit_value) # Calculate the unit count
         time_components.append(f"{unit_count} {singular if unit_count == 1 else plural}") # Append the time component
         days %= unit_value # Update days to the remainder

   # Handle hours separately for cases where days < 1
   if days < 1 and len(time_components) == 0: # If days is less than 1 and there are no time components
      return f"{days * 24:.2f} hours" # Return hours if less than 1 day

   return ", ".join(time_components) # Join all time components for final output

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
      mttu = days_since_first_release / releases.totalCount # Calculate the mean time to update
      return convert_days_to_appropriate_time(mttu) if FORMAT_METRICS else mttu # Return the mean time to update
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
      first_commit = None # Get the first commit by iterating backward through commits if needed
      for commit in commits.reversed: # The reversed iterator retrieves the first commit
         first_commit = commit # Set the first commit
         break # We only need the first commit

      if first_commit is None: # If there are no commits
         return "n/a" # Set the mean time to commit to "n/a"

      days_since_first_commit = (now - first_commit.commit.author.date.replace(tzinfo=timezone.utc)).days # Calculate the days since the first commit
      mttc = days_since_first_commit / commits.totalCount # Calculate the mean time to commit
      return convert_days_to_appropriate_time(mttc) if FORMAT_METRICS else mttc # Return the mean time to commit
   return "n/a" # Set the mean time to commit to "n/a" if there are no commits

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

def print_repository_metrics(metadata):
   """
   Prints the repository metadata.
   
   :param metadata: Dictionary containing repository metadata
   """

   print(f"{BackgroundColors.CYAN}{metadata['Repository Name']}{Style.RESET_ALL}", end=": ") # Output the repository name
   print(f"{BackgroundColors.GREEN}Number of Contributors: {BackgroundColors.CYAN}{metadata['Number of Contributors']}{Style.RESET_ALL}", end=", ") # Output the number of contributors
   print(f"{BackgroundColors.GREEN}MTTU: {BackgroundColors.CYAN}{BackgroundColors.CYAN}{metadata['MTTU']}{Style.RESET_ALL}", end=", ") # Output the mean time to update
   print(f"{BackgroundColors.GREEN}MTTC: {BackgroundColors.CYAN}{metadata['MTTC']}{Style.RESET_ALL}", end=", ") # Output the mean time to commit
   print(f"{BackgroundColors.GREEN}Branch Protection: {BackgroundColors.CYAN}{metadata['Branch Protection']}{Style.RESET_ALL}", end=", ") # Output the branch protection status
   print(f"{BackgroundColors.GREEN}Inactive Period: {BackgroundColors.CYAN}{metadata['Inactive Period']}{Style.RESET_ALL}", end="\n\n") # Output the inactive period

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

def output_time(output_string, time):
   """
   Outputs time, considering the appropriate time unit.

   :param output_string: String to be outputted.
   :param time: Time to be outputted.
   :return: None
   """

   if float(time) < int(TIME_UNITS[0]): # If the time is less than 60 seconds
      time_unit = "seconds" # Set the time unit to seconds
      time_value = time # Set the time value to time
   elif float(time) < float(TIME_UNITS[1]): # If the time is less than 3600 seconds
      time_unit = "minutes" # Set the time unit to minutes
      time_value = time / TIME_UNITS[0] # Set the time value to time divided by 60
   elif float(time) < float(TIME_UNITS[2]): # If the time is less than 86400 seconds
      time_unit = "hours" # Set the time unit to hours
      time_value = time / TIME_UNITS[1] # Set the time value to time divided by 3600
   else: # If the time is greater than or equal to 86400 seconds
      time_unit = "days" # Set the time unit to days
      time_value = time / TIME_UNITS[2] # Set the time value to time divided by 86400

   rounded_time = round(time_value, 2) # Round the time value to two decimal places
   print(f"{BackgroundColors.GREEN}{output_string}{BackgroundColors.CYAN}{rounded_time} {time_unit}{BackgroundColors.GREEN}.{Style.RESET_ALL}")

def main(repo_urls=None, github_token=None, finish_sound=False):
   """
   Main function.

   :param repo_urls: list - Optional list of repository URLs passed as arguments.
   :param github_token: str - Optional GitHub token passed as an argument.
   :param finish_sound: bool - Optional flag to play a sound when the program finishes.
   :return: None
   """

   start_time = time.time() # Start the timer 

   print(f"{BackgroundColors.GREEN}Welcome to the {BackgroundColors.CYAN}AutoMetric{BackgroundColors.GREEN} program!{Style.RESET_ALL}") # Output the welcome message
   print(f"{BackgroundColors.GREEN}This project process the following metrics: {BackgroundColors.CYAN}Number of Contributors, Mean Time to Update (MTTU), Mean Time to Commit (MTTC), Branch Protection, and Inactive Period{BackgroundColors.GREEN} for GitHub and GitLab repositories.{Style.RESET_ALL}") # Output the metrics message

   repo_urls = repo_urls if repo_urls else read_input_file(INPUT_FILE) # Read repository URLs from input file if no args where passed
   output_file_path = build_output_file_path(repo_urls) # Build the output file path
   delete_old_output_file(output_file_path) # Delete the old output file if it exists

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

   output_time(f"\n{BackgroundColors.GREEN}Total execution time: ", (time.time() - start_time)) # Output the total execution time
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
