class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    # private method belonging to insert method - called by insert method
    def _insert_recursive(self, data, node):
        if data["id"] < node.data["id"]:
            if node.left is None:
                node.left = Node(data)
            else:
                self._insert_recursive(data, node.left)    # recursive call
        elif data["id"] > node.data["id"]:
            if node.right is None:
                node.right = Node(data)
            else:
                self._insert_recursive(data, node.right)    # recursive call
        else:
            return  # should not contain duplicates so just return here

    def insert(self, data):
        if self.root is None:  # tree is empty
            self.root = Node(data)  # sets the root node
        else:   # a non-empty tree requires recursive function to insert into tree
            self._insert_recursive(data, self.root)

    def _search_recursive(self, blog_post_id, node):
        if blog_post_id == node.data["id"]:
            return node.data

        # search left subtree
        if blog_post_id < node.data["id"] and node.left is not None:
            return self._search_recursive(blog_post_id, node.left)

        # search right subtree
        if blog_post_id > node.data["id"] and node.right is not None:
            return self._search_recursive(blog_post_id, node.right)

        return False    # post not found

    def search(self, blog_post_id):
        blog_post_id = int(blog_post_id)
        if self.root is None:
            return False
        return self._search_recursive(blog_post_id, self.root)




