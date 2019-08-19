from __future__ import annotations
from cenpilos.models import Posts
from cenpilos.forms import *
from datetime import datetime
from typing import *
from difflib import SequenceMatcher


class Post:
    """
    A class representing a Post for a specific user.

    === Attributes ===
    content: the content of the post
    user_id: the id of the current user.
    date: the datetime of when the post is posted.
    comments: a list of comments this post has
    likes: the number of likes this post has
    """
    content: Any
    date: datetime
    comments: List[Comment]
    likes: int
    userid: Any

    def __init__(self, content: Any, user_id: Any) -> None:
        """ Initializes this class with content as <content>, the <user_id> as the user_id attribute.
         and date as today's date. Sets the comments attributes to an empty list and likes to be 0.
        """

        self.content = content
        self.date = datetime.today()
        self.comments = []
        self.user_id = user_id
        self.likes = 0

    def update_likes(self, factor: int) -> None:
        """ Increment the likes attribute by <factor> """
        self.likes += factor

    def save(self) -> None:
        """ Saves the current post into the database. """

        # Saves the post only when there is no swear words.
        swearwords = self.swearword_filter()

        if not swearwords:
            ...

    def swearword_filter(self) -> bool:
        """
        Returns True iff the percentage of similarity is greater than 50 %.
        """

        swearwords = self.read_swearwords()

        for swearword in swearwords:
            for content in self.content:
                percentage = SequenceMatcher(None, content, swearword).ratio()

                if percentage >= 50.0:
                    return True

        return False

    @staticmethod
    def read_swearwords() -> List[Any]:
        """ Returns a list of all swear words. """

        lst = []
        with open("bad_words.txt", "r") as f:
            for line in f:
                line = line.split()  # DO NOT MODIFY bad_words.txt! If you do, this line will NOT WORK!
                lst.extend(line)

        return lst


class Comment:
    """ A class representing a comment for a specific post.

    === Attributes ===
    user_id: the id of the user that made the comment
    content: the actual content of the comment
    date: the date at which the post was posted

    """
