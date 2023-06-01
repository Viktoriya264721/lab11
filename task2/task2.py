"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
import math
from math import log
import random
import time

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        count = 0
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            count += 1
            while not stack.isEmpty():
                node = stack.pop()
                if node.right != None:
                    stack.push(node.right)
                    count += 1
                if node.left != None:
                    stack.push(node.left)
                    count += 1
        return count

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            left_parent = top.left
            right_parent = top.right
            counter1 = -1
            counter2 = -1
            while left_parent is not None:
                counter1 += 1
                left_parent = left_parent.left
            while right_parent is not None:
                counter2 += 1
                right_parent = right_parent.right
            return max(counter1, counter2) + 1
        return height1(self._root)


    def range_find(self, low, hight):
        """
        Returns a list of the items in the tree, where low <= item <= high.
        :param low:
        :param high:
        :return:
        """
        result = []
        for i in range(low, hight + 1):
            if self.find(i) is not None:
                result.append(i)
        return result


    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        heightt = self.height()
        amount = self.__iter__()
        if heightt < 2 * (math.log(amount + 1) - 1):
            return True
        else:
            return False


    def new_tree(self, result):
        if not result:
            return None
        new_root = BSTNode(result[len(result) // 2])
        lst = [(new_root, 0, len(result) - 1)]
        while lst:
            node, first_el, last_el = lst.pop()
            mid = (first_el + last_el) // 2
            if mid > first_el:
                node.left = BSTNode(result[(first_el + mid - 1) // 2])
                lst.append((node.left, first_el, mid - 1))
            if mid < last_el:
                node.right = BSTNode(result[(mid + 1 + last_el) // 2])
                lst.append((node.right, mid + 1, last_el))
        return new_root


    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        inorder_list = list(self.inorder())
        self.clear()
        self._root = self.new_tree(inorder_list)
        return self

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        result = []
        for i in self.inorder():
            if i > item:
                result.append(i)
        if result == []:
            return None
        return min(result)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        result = []
        for i in self.inorder():
            if i < item:
                result.append(i)
        if result == []:
            return None
        return max(result)


    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read().splitlines()
        return content

    def first(self, content):
        words = random.choices(content, k=10000)
        start = time.time()
        for i in words:
            if i in content:
                pass
        end = time.time()
        difference = end - start
        return difference

    def second(self, content):
        words = random.choices(content, k=10000)
        tree = LinkedBST()
        for i in content[:1000]:
            tree.add(i)
        start = time.time()
        for i in words:
            tree.find(i)
        end = time.time()
        difference = end - start
        return difference

    def third(self, content):
        words = random.choices(content, k=10000)
        words_not_sorted = random.choices(content, k=1000)
        tree = LinkedBST()
        for i in words_not_sorted:
            tree.add(i)
        start = time.time()
        for i in words:
            tree.find(i)
        end = time.time()
        difference = end - start
        return difference

    def fourth(self, content):
        words = random.choices(content, k=10000)
        tree = LinkedBST()
        for i in content[:1000]:
            tree.add(i)
        new_tree = tree.rebalance()
        start = time.time()
        for i in words:
            new_tree.find(i)
        end = time.time()
        difference = end - start
        return difference

