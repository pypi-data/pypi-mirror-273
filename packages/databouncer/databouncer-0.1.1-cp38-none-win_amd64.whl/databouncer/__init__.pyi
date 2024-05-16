import PIL.Image.Image

class DataBouncer(object):
    """Provides access to the main functionalities of the DataBouncer SDK.

    Offers methods to embed images and texts and make decisions about which frames to select.
    """

    @staticmethod
    def new_from_tar(tar_path: str) -> "DataBouncer":
        """
        Initialize DataBouncer.

        Args:
            tar_path:
                Path to the tar file containing the model.

        Raises:
            DataBouncerError:
                If an error occurs during the initialization process.

        Example:
            .. code-block:: python

                databouncer = DataBouncer.new_from_tar(tar_path="lightly_embedding_model.tar")
        """
        ...

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        Embeds a list of text strings.

        Processes a list of text strings, generating an embedding for each text.
        The embeddings are returned as a list of lists, where each inner list represents
        the embedding of a single text.

        Args:
            texts:
                A list of text strings to embed.

        Returns:
            A list of lists of floats, where each inner list represents the embedding of a single text.

        Raises:
            DataBouncerError:
                If an error occurs during the embedding process.

        Example:
            .. code-block:: python

                embeddings = databouncer.embed_texts(["cat", "dog"])
        """
        ...

    def embed_frame(self, frame: PIL.Image.Image) -> list[float]:
        """
        Embeds an RGB image.

        Args:
           frame:
                A PIL image to embed.

        Returns:
           An embedding (list of floats). The dimension of the embedding is determined by the model.

        Raises:
           DataBouncerError:
                If an error occurs during the embedding process.

        Example:
            .. code-block:: python

                from PIL.Image import Image

                with Image.open("cat.jpg") as frame:
                    embedding = databouncer.embed_frame(frame=frame)
        """
        ...

    def insert_into_embedding_database(self, embedding: list[float]) -> None:
        """
        Inserts an embedding into the embedding database.

        Embedding database is used by the diversity strategy.
        If an embedding is inserted into the database the strategy will not anymore select
        frames with embeddings similar to it. You should call ``insert_into_embedding_database``
        for frames marked by ``should_select`` with diversity strategy.

        Args:
            embedding:
                Embedding of a frame. Can be obtained using ``embed_frame``.

        Raises:
            DataBouncerError:
                If the database is full or the embedding has a different dimension
                than other embeddings in the database.
        """
        ...
    def clear_embedding_database(self) -> None:
        """
        Clears the embedding database.

        Removes all embeddings from the database.
        """
        ...

    @property
    def num_diversity_strategies(self) -> int:
        """The number of registered diversity strategies."""
        ...

    @property
    def num_similarity_strategies(self) -> int:
        """The number of registered similarity strategies."""
        ...

    def register_diversity_strategy(self, min_distance: float) -> None:
        """
        Registers a diversity strategy.

        A diversity strategy selects frames that are different from previously selected frames.
        The ``min_distance`` parameter must be between 0 and 1 and controls how different the new
        frame must be from the previously selected frames: Only frames with a distance greater
        than the ``min_distance`` will be selected. To remember selected frames across multiple
        calls, the user must fill the database with embeddings by calling ``insert_into_embedding_database``.

        Args:
            min_distance:
                Only frame embeddings with a distance greater than ``min_distance`` to all embeddings in
                the database will be selected. Must be between 0 and 1.
                A higher value will result in fewer frames being selected.

        Raises:
            DataBouncerError:
                If ``min_distance`` is not between 0 and 1.

        Example:
            .. code-block:: python

                # Register a diversity strategy.
                databouncer.register_diversity_strategy(min_distance=0.5)

                # Embed a frame.
                embedding = databouncer.embed_frame(frame=frame)

                # Check if the frame should be selected.
                select_info = databouncer.should_select(embedding)

                # Add to the embedding database if the image is selected.
                if select_info.diversity[0].should_select:
                    databouncer.insert_into_embedding_database(embedding)
        """
        ...

    def register_similarity_strategy(
        self, embedding_query: list[float], max_distance: float
    ) -> None:
        """
        Registers a similarity strategy.

        A similarity strategy selects frames that are similar to a query embedding.
        The ``max_distance`` parameter must be between 0 and 1 and controls how similar
        the embeddings must be for a frame to be selected: Only frames with a distance
        less than the ``max_distance`` will be selected.

        Args:
            query_embedding:
                Query embedding. Can be obtained using embed_texts.
            max_distance:
                Only frame embeddings with a distance less than ``max_distance`` to the query embedding
                will be selected.
                Must be between 0 and 1. A higher value will result in more frames being selected.

        Raises:
            DataBouncerError:
                If ``max_distance`` is not between 0 and 1.

        Example:
            .. code-block:: python

                # Embed query texts.
                query_embeddings = databouncer.embed_texts(["cat", "dog"])

                databouncer.register_similarity_strategy(query_embeddings[0], 0.3)
                databouncer.register_similarity_strategy(query_embeddings[1], 0.4)

                # Embed a frame.
                embedding = databouncer.embed_frame(frame=frame)

                # Check if the frame should be selected.
                select_info = databouncer.should_select(embedding)
                is_cat = select_info.similarity[0].should_select
                is_dog = select_info.similarity[1].should_select
        """
        ...

    def should_select(self, embedding: list[float]) -> SelectInfo:
        """
        Checks if a frame should be selected.

        Checks if a frame should be selected based on its embedding and
        the registered strategies. In particular, it iterates over all registered
        diversity and similarity strategies and creates a selection info object of for each strategy.
        The strategy selection info object contains the selection result (true or false) and
        metadata about the selection.

        Args:
            embedding:
                Embedding of a frame. Can be obtained using ``embed_frame``.

        Returns:
            A selection info object containing the selection result and metadata for each registered strategy.

        Raises:
            DataBouncerError:
                If an error occurs during the selection process.

        Example:
            .. code-block:: python

                # Register a diversity strategy.
                databouncer.register_diversity_strategy(min_distance=0.5)

                # Embed a frame.
                embedding = databouncer.embed_frame(frame=frame)

                # Check if the frame should be selected.
                select_info = databouncer.should_select(embedding)

                assert len(select_info.diversity) == 1 # One diversity strategy is registered.
                assert len(select_info.similarity) == 0 # No similarity strategy is registered.
                is_selected = select_info.diversity[0].selected
        """
        ...

class DataBouncerError(Exception):
    """Custom error type raised by DataBouncer SDK functions."""
    def __init__(self, message: str) -> None: ...
    def __str__(self) -> str: ...

class SelectInfo:
    """Selection information about a processed frame."""

    diversity: list[DiversitySelectInfo]
    """A list of diversity strategy selection information."""
    similarity: list[SimilaritySelectInfo]
    """A list of similarity strategy selection information."""

class DiversitySelectInfo:
    """The result of a diversity strategy."""

    min_distance: float
    """The minimum distance to the embeddings in the database for the frame to be selected."""
    should_select: bool
    """A boolean indicating whether the frame should be selected."""

class SimilaritySelectInfo:
    """The result of a similarity strategy."""

    distance: float
    """The distance to the query embedding for the frame to be selected."""
    should_select: bool
    """A boolean indicating whether the frame should be selected."""
