from django.core.management.base import BaseCommand
from tracker.models import Phase, Chapter, Problem

ROADMAP = [
('1', 'Python + Complexity Foundations', 'Build speed and fluency before deep DSA.', [
('1.1','Python DSA Toolkit',['Lists, dicts, sets and tuples','enumerate, zip and comprehensions','Counter, defaultdict and deque']),
('1.2','Big-O & Problem Solving',['Time and space complexity','Input constraints and edge cases','Brute force to optimized thinking'])]),
('2','Hash Map & Hash Set', 'Master the highest-return interview pattern.', [
('2.1','Frequency & Lookup',['Two Sum','Valid Anagram','Group Anagrams','Top K Frequent Elements']),
('2.2','Prefix / Complement Thinking',['Contains Duplicate','Longest Consecutive Sequence','Subarray Sum Equals K'])]),
('3','Two Pointers & Sliding Window','Learn linear-time array and string patterns.',[
('3.1','Two Pointers',['Valid Palindrome','Two Sum II','3Sum','Container With Most Water']),
('3.2','Sliding Window',['Best Time to Buy and Sell Stock','Longest Substring Without Repeating Characters','Longest Repeating Character Replacement','Minimum Window Substring'])]),
('4','Stack, Queue & Binary Search','Build core linear and logarithmic patterns.',[
('4.1','Stack / Monotonic Stack',['Valid Parentheses','Min Stack','Daily Temperatures','Largest Rectangle in Histogram']),
('4.2','Binary Search',['Binary Search','Search a 2D Matrix','Find Minimum in Rotated Sorted Array','Search in Rotated Sorted Array'])]),
('5','Linked Lists','Pointer manipulation without losing references.',[
('5.1','Core Linked List',['Reverse Linked List','Merge Two Sorted Lists','Linked List Cycle','Remove Nth Node From End']),
('5.2','Fast / Slow Pointers',['Middle of Linked List','Reorder List','Palindrome Linked List'])]),
('6','Trees & Heaps','Recursive thinking, traversal and priority queues.',[
('6.1','Binary Trees',['Maximum Depth of Binary Tree','Invert Binary Tree','Binary Tree Level Order Traversal','Validate Binary Search Tree']),
('6.2','BST / Heap',['Kth Smallest Element in a BST','Lowest Common Ancestor of a BST','Kth Largest Element in a Stream','Merge K Sorted Lists'])]),
('7','Graphs','DFS, BFS, visited-state and topological thinking.',[
('7.1','DFS / BFS',['Number of Islands','Clone Graph','Rotting Oranges','Pacific Atlantic Water Flow']),
('7.2','Graph Algorithms',['Course Schedule','Graph Valid Tree','Number of Connected Components'])]),
('8','Backtracking','Systematically enumerate constrained choices.',[
('8.1','Combinations & Permutations',['Subsets','Combination Sum','Permutations','Letter Combinations of a Phone Number']),
('8.2','Constraint Search',['Word Search','N-Queens'])]),
('9','Dynamic Programming','Turn recursive states into reusable subproblems.',[
('9.1','1D DP',['Climbing Stairs','House Robber','Coin Change','Longest Increasing Subsequence']),
('9.2','2D DP',['Unique Paths','Longest Common Subsequence','Word Break','Edit Distance'])]),
('10','Greedy, Intervals & Interview Simulation','Finish with patterns and timed practice.',[
('10.1','Greedy / Intervals',['Maximum Subarray','Jump Game','Merge Intervals','Non-overlapping Intervals']),
('10.2','Mock Interview Sets',['Mixed Easy Set','Mixed Medium Set','Mixed Hard Set'])]),
]

EASY = 10
MEDIUM = 20
HARD = 30

def difficulty(title):
    hard_words = ['Minimum Window','Largest Rectangle','Edit Distance','N-Queens','Mixed Hard','Word Break','Merge K','Pacific Atlantic']
    medium_words = ['Top K','3Sum','Container','Longest','Replacement','Rotated','Remove Nth','Reorder','Level Order','Validate','Kth','Number of Islands','Course Schedule','Clone Graph','Combination Sum','Permutations','Word Search','Coin Change','House Robber','Subsets','Merge Intervals','Non-overlapping','Mixed Medium']
    if any(w.lower() in title.lower() for w in hard_words): return 'hard', HARD
    if any(w.lower() in title.lower() for w in medium_words): return 'medium', MEDIUM
    return 'easy', EASY

class Command(BaseCommand):
    help = 'Seed the interview preparation roadmap'
    def handle(self, *args, **options):
        if Phase.objects.exists():
            self.stdout.write(self.style.WARNING('Roadmap already exists; skipping seed.'))
            return
        for pi, (order, title, desc, chapters) in enumerate(ROADMAP, 1):
            phase = Phase.objects.create(order=pi, title=title, description=desc, target_days=6 if pi < 10 else 8)
            for ci, (ctitle, cdesc, problems) in enumerate(chapters, 1):
                chapter = Chapter.objects.create(phase=phase, order=ci, title=ctitle, description=cdesc)
                for ptitle in problems:
                    diff, points = difficulty(ptitle)
                    Problem.objects.create(chapter=chapter, title=ptitle, difficulty=diff, points=points)
        self.stdout.write(self.style.SUCCESS('Seeded 10 phases, 20 chapters and the starter problem set.'))
