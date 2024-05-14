import requests
import json
import datetime


class AutoCortext:
    """
    A client for interacting with the AutoCortext API.

    This class provides methods to send messages and receive responses from the AutoCortext API.

    Attributes:
        org_id (str): The organization ID required for API requests.
        api_key (str): The API key used for secure communication with the API.
        base_url (str): The base URL for the API endpoints.
    """

    def __init__(self, org_id, api_key):
        """
        Initializes the AutoCortext client with necessary authentication credentials.

        Args:
            org_id (str): The organization ID for the API.
            api_key (str): The API key for accessing the API.

        Raises:
            ValueError: If either org_id or api_key is not provided.
        """
        if not org_id:
            raise ValueError("Organization ID must be provided and cannot be empty.")
        if not api_key:
            raise ValueError("API key must be provided and cannot be empty.")

        self.configured = False
        self.system = "Not specified"
        self.machine = "Not specified"
        self.verbosity = "concise"
        self.response_type = "Technician"
        self.history = [
            {
                "id": 1,
                "content": f"Auto Cortext: Hello sir/madam.\n\nToday's date is {datetime.datetime.now().date()}, and the local time is {datetime.datetime.now().time().strftime('%H:%M:%S')}. \n\nWhat machine are you having trouble with?",
                "role": "assistant",
            },
        ]
        self.base_url = "https://ascend-six.vercel.app/"
        self.org_id = org_id
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def config(
        self, verbosity=None, machine=None, system=None, response_type=None, env="prod"
    ):
        """
        Configures the AutoCortext client with machine name and verbosity level.

        This method allows you to set the name of the machine and system being troubleshooted, the
        verbosity level of the responses from the AutoCortext API, and the response type.

        Args:
            verbosity (str): The verbosity level of the responses. Must be either "concise" or "verbose".
            machine (str): The name of the machine or system being troubleshooted.
            system (str): The system or software being troubleshooted.
            response_type (str): The type of response to be given by the assistant. Must be either "Technician", "Engineer", or "Maintenance".
            env (str): The environment to use. Must be either "prod" or "dev".

        Returns:
            None

        Raises:
            ValueError: If the AutoCortext client is already configured.
            ValueError: If the machine name, system, verbosity, or response_type are not provided or are not strings.
            ValueError: If the verbosity level is not "concise" or "verbose".
            ValueError: If the response type is not "Technician", "Engineer", or "Maintenance".
        """
        if self.configured:
            raise ValueError("AutoCortext client is already configured.")

        if not machine:
            raise ValueError("Machine name must be provided and cannot be empty.")
        if not verbosity:
            raise ValueError("Verbosity must be provided and cannot be empty.")
        if not system:
            raise ValueError("System name must be provided and cannot be empty.")
        if not response_type:
            raise ValueError("Response type must be provided and cannot be empty.")
        if env not in ["prod", "dev"]:
            raise ValueError("Environment must be either 'prod' or 'dev'.")

        if not isinstance(machine, str):
            raise ValueError("Machine name must be a string.")
        if not isinstance(verbosity, str):
            raise ValueError("Verbosity must be a string.")
        if not isinstance(system, str):
            raise ValueError("System name must be a string.")
        if not isinstance(response_type, str):
            raise ValueError("Response type must be a string.")

        if verbosity not in ["concise", "verbose"]:
            raise ValueError("Verbosity must be either 'concise' or 'verbose'.")
        if response_type not in ["Technician", "Engineer", "Maintenance"]:
            raise ValueError(
                "Response type must be either 'Technician', 'Engineer', or 'Maintenance'."
            )

        self.machine = machine
        self.verbosity = verbosity
        self.system = system
        self.response_type = response_type
        self.base_url = (
            "https://ascend-six.vercel.app/"
            if env == "prod"
            else "https://ascend-git-develop-ascend-engineering.vercel.app/"
        )

        print(f"[autocortext_py] Machine set to {machine}.")
        print(f"[autocortext_py] Verbosity set to {verbosity}.")
        print(f"[autocortext_py] System set to {system}.")
        print(f"[autocortext_py] Response type set to {response_type}.")
        print(f"[autocortext_py] Environment set to {env}.")

        # add required prompts
        new_messages = [
            {
                "id": 2,
                "content": f"User: The user selected the {machine}.",
                "role": "user",
            },
            {
                "id": 3,
                "content": f"Auto Cortext: Great! What system in the {machine} are you having issues with?",
                "role": "assistant",
            },
            {
                "id": 4,
                "content": f"User: The user is having issues with the {system} system.",
                "role": "user",
            },
            {
                "id": 5,
                "content": f"Auto Cortext: OK, tell me about the problem you are experiencing with the {system} in the {machine}.",
            },
        ]

        self.history += new_messages
        self.configured = True

    def troubleshoot(self, message):
        """
        Sends a troubleshooting message to the API and returns the response.

        The method expects a message in the form of a string.

        Args:
            message (str): The message to be sent for troubleshooting.

        Returns:
            str: The response from the API, typically containing troubleshooting information.

        Raises:
            ValueError: If the message is neither a string nor a dictionary.
            JSONDecodeError: If the response from the API is not valid JSON.
        """
        if not isinstance(message, str):
            raise ValueError("Message must be a valid string.")

        # Add the message to the history (merge with existing history)
        max_id = max(msg["id"] for msg in self.history)
        new_msg = [
            {
                "id": max_id + 1,
                "content": f"User: {message}.",
                "role": "user",
            }
        ]
        self.history += new_msg

        print("[autocortext_py] Sending context to server. Please wait...")
        response = requests.post(
            f"{self.base_url}/api/read?companyId={self.org_id}",
            headers=self.headers,
            json={
                "messages": self.history,
                "verbosity": self.verbosity,
                "audience": self.response_type,
            },
        )

        if response.status_code == 200:
            try:
                print("[autocortext_py] Response received. Processing...")
                response_data = response.json()
                content = response_data.get("data", "No data found")

                # Add the response to the history
                formatted_response = {
                    "id": max_id + 1,
                    "content": "Auto Cortext: " + content,
                    "role": "assistant",
                }

                self.history.append(formatted_response)
                return content

            except json.JSONDecodeError:
                return "Invalid JSON response"
        else:
            return f"Error: {response.status_code} - {response.text}"

    def set_verbosity(self, mode):
        """
        Set the verbosity of the AutoCortext client.

        The verbosity can be either "concise" or "verbose". In "concise" mode, AutoCortext will keep
        the response short and sweet. In "verbose" mode, AutoCortext will provide more detailed responses.

        Args:
            mode (str): The mode to set the client to. Must be either "concise" or "verbose".

        Raises:
            ValueError: If the mode is not a string or not "concise" or "verbose".
        """
        if not isinstance(mode, str):
            raise ValueError("Mode must be a string.")

        if mode not in ["concise", "verbose"]:
            raise ValueError("Mode must be either 'concise' or 'verbose'.")

        print(f"[autocortext_py] Verbosity set to {mode}.")
        self.verbosity = mode

    def set_machine(self, machine):
        """
        Set the machine name for the AutoCortext client.

        This method allows you to specify the name of the machine or system that is being troubleshooted.

        Args:
            machine (str): The name of the machine or system being troubleshooted.

        Returns:
            None

        Raises:
            ValueError: If the machine name is not provided or is not a string.
        """
        if not machine:
            raise ValueError("Machine name must be provided and cannot be empty.")

        if not isinstance(machine, str):
            raise ValueError("Machine name must be a string.")

        print(f"[autocortext_py] Machine set to {machine}.")
        self.machine = machine

    def set_system(self, system):
        """
        Set the system for the AutoCortext client.

        This method allows you to specify the system that is being troubleshooted.

        Args:
            system (str): The system or software being troubleshooted.

        Returns:
            None

        Raises:
            ValueError: If the system name is not provided or is not a string.
        """
        if not system:
            raise ValueError("System name must be provided and cannot be empty.")

        if not isinstance(system, str):
            raise ValueError("System name must be a string.")

        print(f"[autocortext_py] System set to {system}.")
        self.system = system

    def set_response_type(self, response_type):
        """
        Set the response type for the AutoCortext client.

        This method allows you to specify the type of response to be given by AutoCortext.

        Args:
            response_type (str): The type of response to be given by AutoCortext. Must be either "Technician", "Engineer", or "Maintenance".

        Returns:
            None

        Raises:
            ValueError: If the response type is not provided or is not a string.
            ValueError: If the response type is not "Technician", "Engineer", or "Maintenance".
        """
        if not response_type:
            raise ValueError("Response type must be provided and cannot be empty.")

        if not isinstance(response_type, str):
            raise ValueError("Response type must be a string.")

        if response_type not in ["Technician", "Engineer", "Maintenance"]:
            raise ValueError(
                "Response type must be either 'Technician', 'Engineer', or 'Maintenance'."
            )

        print(f"[autocortext_py] Response type set to {response_type}.")
        self.response_type = response_type

        # update the response type in the history
        self.history[0]["context"] = self.audience_map[self.response_type]

    def save(self):
        """
        Save the history of messages exchanged with the AutoCortext API to a the remote server.

        This history will be viewable at https://ascend-six.vercel.app/dashboard/troubleshoot

        Args:
            None

        Returns:
            str: A message indicating the status of the save operation.
        """
        context = {
            "machine": self.machine,
            "messages": self.history,
            "companyId": self.org_id,
            "summarize": False,
        }

        print("[autocortext_py] Saving history to server. Please wait...")
        response = requests.post(
            f"{self.base_url}/api/history",
            headers=self.headers,
            json=context,
        )

        if response.status_code == 200:
            print("[autocortext_py] History saved successfully.")
            return "OK"
        else:
            return f"Error: {response.status_code} - {response.text}"

    def clear(self):
        """
        Clear the history of messages exchanged with the AutoCortext API, the verbosity mode, the machine name, and the system.

        Args:
            None

        Returns:
            None
        """
        self.configured = False
        self.system = "Not specified"
        self.machine = "Not specified"
        self.verbosity = "concise"
        self.base_url = "https://ascend-six.vercel.app/"
        self.history = [
            {
                "id": 1,
                "content": f"Auto Cortext: Hello sir/madam.\n\nToday's date is {datetime.datetime.now().date()}, and the local time is {datetime.datetime.now().time().strftime('%H:%M:%S')}. \n\nWhat machine are you having trouble with?",
                "role": "assistant",
            }
        ]
        print("[autocortext_py] History cleared.")
