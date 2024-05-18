import json
import logging
import os
from pathlib import Path
from typing import Any

import httpx
import magic
from httpx import Response
from tqdm import tqdm

from knowledgeai.client import (
    LLM,
    AskResponse,
    DistanceStrategy,
    HttpMethod,
    IsoLanguage,
    Project,
    ProjectConfigKey,
    RetrievedDocument,
    Retriever,
    SearchType,
    SourceDocument,
)

log: logging.Logger = logging.getLogger(__name__)
limits = httpx.Limits(max_keepalive_connections=20, max_connections=None)


class KnowledgeAIClient:
    def __init__(self, url: str, api_key: str, timeout: int = 90) -> None:
        self.url: str = url
        self.api_key: str = api_key
        self.timeout = timeout

    @staticmethod
    def read_files_from_directory(directory: str) -> list[Path]:
        current_directory = Path(directory)
        files: list[Path] = [
            current_directory / file
            for file in os.listdir(directory)
            if Path.is_file(current_directory / file)
        ]
        return files

    def _api_call(
        self,
        method: HttpMethod,
        url: str,
        data: Any | None = None,
        params: Any | None = None,
        headers: dict[str, str] | None = None,
        form: bool = True,
    ) -> Response:
        headers_default: dict[str, str] = {
            "accept": "application/json",
            "Authorization": self.api_key,
            "x-apikey": self.api_key,
        }

        if form:
            headers_default["Content-Type"] = "application/x-www-form-urlencoded"

        with httpx.Client(
            limits=limits,
            base_url=self.url,
            headers=headers_default,
            timeout=self.timeout,
        ) as client:
            response: Response = client.request(
                method,
                url,
                data=data,
                params=params,
                headers=headers,
            )
            response.raise_for_status()

        return response

    def upload_directory(
        self, project_id: int, directory: str, roles: str = "user"
    ) -> None:
        """
        Convenience method to upload all files in a directory to the specified project.

        Args:
            project_id (str):
                The ID of the project to upload the documents to.
            directory (str):
                The path to the directory containing the files to upload.
            roles (str, optional):
                The roles to assign to the uploaded documents.
                Comma separated list, defaults to "user".

        Returns:
            None

        Raises:
            requests.exceptions.RequestException: If an error occurs while uploading
            the documents.

        Example:
          >>> client.upload_directory("project_id", "/path/to/directory", "admin,user")
        """
        files: list[Path] = self.read_files_from_directory(directory)
        self.index_documents(project_id, files, roles)

    def index_documents(
        self,
        project_id: int,
        files: list[Path],
        roles: str = "user",
        timeout: int = 300,
    ) -> None:
        """
        Uploads multiple documents to the specified project.

        Args:
            project_id (str): The ID of the project to upload the documents to.
            files (List[str]): A list of file paths to upload.
            roles (str, optional): The roles to assign to the uploaded documents.
                Comma separated list, defaults to "user".
            timeout (int, optional): set the timeout in seconds for the indexing. Use
                at least 300s for PDF documents.

        Returns:
            None

        Raises:
            requests.exceptions.RequestException: If an error occurs while uploading
            the documents.

        Example:
            >>> client.add_multiple_documents(
                    "project_id", ["/path/to/file1.txt", "/path/to/file2.txt"],
                    roles="user,admin"
                )
        """
        url: str = "/index/document"
        filesp = tqdm(files)

        headers: dict[str, str] = {
            "accept": "application/json",
            "Authorization": self.api_key,
            "x-apikey": self.api_key,
        }

        with httpx.Client(
            limits=limits, base_url=self.url, headers=headers, timeout=timeout
        ) as client:
            for file in filesp:
                log.debug("Uploading file: %s", file)
                upload_file = {
                    "file": (
                        file.name,
                        open(file, "rb"),  # noqa: SIM115, PTH123
                        magic.from_file(file, mime=True),
                    )
                }  # type ignore
                data = {"project_id": project_id, "roles": roles}

                response: Response = client.request(
                    HttpMethod.POST,
                    url,
                    data=data,
                    files=upload_file,
                )
                response.raise_for_status()

                log.debug(msg=response.content)

    def index_urls(
        self, project_id: int, index_urls: list[str], roles: str | None
    ) -> None:
        """
        Indexes the specified URL to the specified project.

        Args:
            project_id (str):
                The ID of the project to index the URL to.
            url (str):
                The URLs to index.
            roles (str, optional): The roles to assign to the indexed document.
                Comma separated list, defaults to "user".

        Returns:
            None

        Raises:
          requests.exceptions.RequestException: If an error occurs while indexing.

        Example:
          >>> client.index_url("project_id", "https://www.example.com", roles="user")
        """
        url = "/index/urls"
        data = {"project_id": project_id, "urls": index_urls, "roles": roles}
        self._api_call(HttpMethod.POST, url, data=data)

    def delete_document(self, project_id: int, document_id: int) -> None:
        """
        Deletes the document with the specified ID by making a DELETE request to the
        KnowledgeAI API. The `project_id` parameter specifies the ID of the project the
        document belongs to, and the `document_id` parameter specifies the ID of the
        document to delete.

        If the deletion is successful, no value is returned. If an error occurs during
        the API call, a `requests.exceptions.RequestException` is raised.

        Args:
            project_id (int):
                The ID of the project the document belongs to.
            document_id (int):
                The ID of the document to delete.

        Returns:
            None

        Raises:
            requests.exceptions.RequestException: If an error occurs.

        Example usage:
        ```
        client = KnowledgeAIClient()
        client.delete_document(project_id=1, document_id=1)
        ```
        """
        url: str = "/index/document"
        data = {"project_id": project_id, "document_id": document_id}
        self._api_call(HttpMethod.DELETE, url, params=data)
        log.info("Document %s deleted", document_id)

    def delete_all_documents(self, project_id: int) -> None:
        """
        Deletes all documents for the specified project.

        Args:
            project_id (int):
                The ID of the project to delete all documents for.

        Returns:
            None

        Raises:
            requests.exceptions.RequestException: If an error occurs.

        Example:
            >>> client.delete_all_documents(project_id=1)
        """
        url: str = "/index/document/all"
        data = {"project_id": project_id}
        self._api_call(HttpMethod.DELETE, url, data=data)
        log.info("All documents deleted for project %s", project_id)

    def list_projects(self) -> list[Project]:
        """
        Lists all projects.

        Returns:
            List[Project]: A list of projects.

        Raises:
            requests.exceptions.RequestException: If an error occurs.

        Example:
            >>> projects = client.list_projects()
            >>> for project in projects:
            ...     print(project.name)
        """
        url: str = "/project/"
        response: Response = self._api_call(HttpMethod.GET, url, form=False)

        return [Project(**project) for project in response.json()]

    def get_project(self, project_id: int, with_documents: bool = False) -> Project:
        """
        Gets the project with the specified ID.

        Args:
            project_id (str):
                The ID of the project to get.
            with_documents (bool, optional):
                Whether to include the documents in the response,

        Returns:
            Project: The project with the specified ID.

        Raises:
            requests.exceptions.RequestException: If an error occurs.

        Example:
            >>> project = client.get_project(1)
            >>> print(project.name)
        """
        url: str = "/project/" + str(project_id)
        data: dict[str, bool] = {"with_documents": with_documents}
        response: Response = self._api_call(HttpMethod.GET, url, params=data)

        project = response.json()
        return Project(**project)

    def create_project(
        self,
        project_name: str,
        prompt: str,
        language: IsoLanguage = IsoLanguage.ENGLISH,
        llm: LLM = LLM.OPENAI,
    ) -> Project:
        """
        Creates a new project with the specified name.

        Args:
            project_name (str):
                The name of the project to create.
            language (IsoLanguage, optional):
                The language of the project, defaults to IsoLanguage.ENGLISH.
            llm (LLM, optional):
                The language model to use, defaults to LLM.OPENAI.
            prompt (str, optional):
                The prompt to use for the project, defaults to None.

        Returns:
            Response: The created project.

        Raises:
            requests.exceptions.RequestException: If an error occurs.

        Example:
            >>> project = client.create_project("New Project")
            >>> print(project.name)
        """
        url: str = "/project/create"

        data: dict[str, str] = {
            "name": project_name,
            "language": language.value,
            "llm": llm.value,
        }

        if prompt:
            data["prompt"] = prompt

        response: Response = self._api_call(HttpMethod.POST, url, data=data)
        project = response.json()
        return Project(**project)

    def update_project(self, project: Project) -> Response:
        """Updates the specified project.

        Args:
            project (Project):
                The project to update. Does not update the configuration or
                the documents.

        Returns:
            Response: The updated project.

        Raises:
            requests.exceptions.RequestException: If an error occurs.

        Example:
            >>> project = client.get_project(1)
            >>> project.name = "New Project Name"
            >>> response = client.update_project(project)
        """

        url: str = "/project/" + str(project.id)
        data = {
            "project_id": project.id,
            "name": project.name,
            "language": project.language.value,
            "llm": project.llm.value,
            "prompt": project.prompt,
        }

        return self._api_call(HttpMethod.PUT, url, data=data)

    def update_project_configuration(
        self, project_id: int, key: ProjectConfigKey, value: str
    ) -> Project:
        """Updates the configuration of the specified project.

        Args:
            project_id (int): The ID of the project to update the configuration for.
            key (str): The key of the configuration to update.
            value (str): The value to update the configuration to.

        Returns:
            Project: The updated project.

        Raises:
            requests.exceptions.RequestException: If an error occurs.

        Example:
            >>> project = client.update_project_configuration(
                    1, ProjectConfigKey.WELCOME_MESSAGE, "value"
                )
        """

        url: str = "/project/" + str(project_id) + "/configuration/" + key.value
        data: dict[str, str] = {"value": value}
        response: Response = self._api_call(HttpMethod.PUT, url, data=data)

        return Project(**response.json())

    def delete_project(self, project_id: int) -> None:
        """Deletes the project with the specified ID.

        Args:
            project_id (int): The ID of the project to delete.

        Returns:
            None

        Raises:
            requests.exceptions.RequestException: If an error occurs.

        Example:
            >>> client.delete_project(1)
        """

        url: str = "/project/" + str(project_id)
        self._api_call(HttpMethod.DELETE, url)
        log.info("Project %s deleted", project_id)

    def ask(self, project_id: int, question: str) -> AskResponse:
        """Asks a question to the specified project.

        Args:
            project_id (int): The ID of the project to ask the question to.
            question (str): The question to ask.

        Returns:
            AskResponse: The response to the question.

        Raises:
            requests.exceptions.RequestException: If an error occurs.

        Example:
            >>> response = client.ask(1, "What is the capital of Germany?")
            >>> print(response.answer)
        """

        url: str = "/chat/ask"
        data = {
            "project_id": project_id,
            "question": question,
        }

        response: Response = self._api_call(HttpMethod.POST, url, data=data)
        content = json.loads(response.content)

        references: list[SourceDocument] = [
            SourceDocument(**reference) for reference in content["source_documents"]
        ]

        return AskResponse(
            question=content["question"],
            answer=content["answer"],
            source_paragraphs=content["source_paragraphs"],
            source_documents=references,
        )

    def retrieve(
        self,
        project_id: int,
        query: str,
        retriever_type: Retriever = Retriever.default,
        search_type: SearchType = SearchType.MMR,
        lambda_mult: float = 0.5,
        top_k: int = 20,
        top_n: int = 10,
        semantic_weight: float = 0.5,
        fulltext_weight: float = 0.5,
        distance_strategy: DistanceStrategy = DistanceStrategy.COSINE,
    ) -> list[RetrievedDocument]:
        """Retrieves documents for the specified project.

        Args:

            project_id (int):
                The ID of the project to retrieve documents from.
            query (str):
                The query to retrieve documents for.
            retrieval_type (Retriever, optional):
                The type of retrieval to use, defaults to Retriever.default.

        Returns:
            List[RetrievedDocument]: The retrieved documents, containing the splitted
                paragraph and a dictionary with metadata.

        Raises:
            requests.exceptions.RequestException: If an error occurs.

        Example:
            >>> references = client.retrieve(1, "What is the capital of Germany?")
            >>> for reference in references:
            ...     print(reference.content)
        """
        url: str = "/retrieve"
        data = {
            "project_id": project_id,
            "query": query,
            "retriever_type": retriever_type.value,
            "search_type": search_type.value,
            "lambda_mult": lambda_mult,
            "top_k": top_k,
            "top_n": top_n,
            "semantic_weight": semantic_weight,
            "fulltext_weight": fulltext_weight,
            "distance_strategy": distance_strategy.value,
        }

        response: Response = self._api_call(HttpMethod.POST, url, data=data)
        content = json.loads(response.content)

        references: list[RetrievedDocument] = [
            RetrievedDocument(**reference) for reference in content["documents"]
        ]

        return references
