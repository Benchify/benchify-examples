from typing import List, Dict

# Check if two users are following each other
def are_following_each_other(user1_following: List[str], user2_following: List[str], user1: str, user2: str) -> bool:
    """
    Check if two users are following each other.

    :param user1_following: List of usernames that user1 is following
    :param user2_following: List of usernames that user2 is following
    :param user1: Username of the first user
    :param user2: Username of the second user
    :return: True if both users are following each other, False otherwise
    """
    return user1 in user2_following and user2 in user1_following

# Rank users by follower count
def rank_users_by_followers(followers: Dict[str, List[str]]) -> List[str]:
    """
    Rank users by their follower count in descending order.

    :param followers: Dictionary where key is the username and value is the list of followers
    :return: List of usernames ranked by follower count
    """
    return sorted(followers.keys(), key=lambda user: len(followers[user]), reverse=True)

# Get mutual followers between two users
def get_mutual_followers(user1_followers: List[str], user2_followers: List[str]) -> List[str]:
    """
    Get the list of mutual followers between two users.

    :param user1_followers: List of followers of the first user
    :param user2_followers: List of followers of the second user
    :return: List of mutual followers
    """
    return list(set(user1_followers) & set(user2_followers))

# Get the list of users a user is not following back
def get_non_follow_backs(user_following: List[str], user_followers: List[str]) -> List[str]:
    """
    Get the list of users that a user is following but are not following back.

    :param user_following: List of usernames that the user is following
    :param user_followers: List of usernames that are following the user
    :return: List of usernames that are not following back
    """
    return [user for user in user_following if user not in user_followers]

# Get the list of users who are not following back the given user
def get_users_not_following_back(user_followers: List[str], user_following: List[str]) -> List[str]:
    """
    Get the list of users who are not following back the given user.

    :param user_followers: List of usernames that are following the user
    :param user_following: List of usernames that the user is following
    :return: List of usernames who are not following back the user
    """
    return [user for user in user_followers if user not in user_following]
