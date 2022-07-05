import unittest

from src.Models.trip import LinkedList

import random

class LinkedListTests(unittest.TestCase):
    def test_insert_basic(self):
        dll = LinkedList()
        dll.insert(1)
        dll.insert(2)
        self.assertEqual(len(dll), 2)
        self.assertEqual(dll[0], 2)
        self.assertEqual(dll[1], 1)
    
    def test_insert_comp(self):
        dll = LinkedList()
        dll.insert(3)
        dll.insert(2)
        dll.insert(1)
        dll.insert(4, 1)
        dll.insert(5, -2)
        dll.insert(6, -1)
        self.assertEqual(len(dll), 6)
        self.assertEqual(dll[0], 1)
        self.assertEqual(dll[1], 4)
        self.assertEqual(dll[2], 5)
        self.assertEqual(dll[3], 2)
        self.assertEqual(dll[4], 6)
        self.assertEqual(dll[5], 3)

    def test_insert_random(self):
        comp_list = list()
        linked = LinkedList()
        for i in range(random.randint(50, 100)):
            num = random.randint(1, 10000)
            comp_list.append(num)
            linked.insert(num)
        comp_list.reverse()
        
        idx = 0
        curr = linked._head
        while curr:
            self.assertEqual(curr, comp_list[idx])
            idx += 1
            curr = curr.next
    
    def test_insert_random_comprehensive(self):
        comp_list = list()
        linked = LinkedList()
        for i in range(random.randint(50, 100)):
            num = random.randint(1, 10000)
            index = random.randint(0, len(comp_list))
            comp_list.insert(index, num)
            linked.insert(num, index)
        
        idx = 0
        curr = linked._head
        while curr:
            self.assertEqual(curr, comp_list[idx])
            idx += 1
            curr = curr.next
