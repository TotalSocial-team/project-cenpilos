"""
This class is a part of this program and should NOT under any circumstances be modified
or deleted!

"""
from cenpilos.models import Posts
from cenpilos.forms import *


class Post:
    """
    Posts the content to the newsfeed
    """

    def __init__(self, form: PostForm) -> None:
        """
        Initializes with a parameter called form
        :param form: Must be the data from the Post Form
        """
        self.post_content = form
        self.sear_words = list()    # list of all swear words -- initially empty

    def __str__(self) -> str:
        """
        Executes when the user types in str(<Post object>) or print(<Post object>)
        :return: a formatted string containing only the user's post
        """
        return str(self.post_content)

    def __repr__(self) -> str:
        """
        Executes when the user types in str(<Post object>) or print(<Post object>)
        :return: a formatted string containing only the user's post
        """
        return str(self.post_content)

    def save_post(self):
        """
        # TODO: Come up with a description for this function :)
        ASSUMES: the user has a space
        :return:
        """
        post = [word.split(' ') for word in self.post_content]

        # ADVANCED TECHNIQUE -- BEGINNERS MIGHT NOT UNDERSTAND THIS #
        def swear_word_checker() -> float:
            """
            Uses the post variable created above iterate through to do some tests
            :return: A percentage out of 100, indicating if the word is a swear word or not
            """
            percent = 0.0
            # TODO: put this section in a filter
            with open("bad_words.txt", "r") as f:
                for line in f:
                    line = line.split(',')      # DO NOT MODIFY bad_words.txt! If you do, this line will NOT WORK!
                    for i, p in post:
                        if len(p) == len(line):
                            if p == line:
                                percent = 100.0     # FOUND A SWEAR WORD

            return percent

